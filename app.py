from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import openai
from string import Template
import json
from sqlalchemy import text

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

table_info = """
col_name: id:, dtype: serial, description: The primary key of the table, increments automatically
col_name: ip_address, dtype: text, description: The IP address of the visitor
col_name: org_name, dtype: text, description: The organization name of the visitor
col_name: access_date, dtype: date, description: The date of the access by the visitor
col_name: access_time, dtype: time, description: The time of the access by the visitor
col_name: request, dtype: text, description: The type of HTTP request made by the visitor
col_name: page_url, dtype: text, description: The URL of the page visited by the visitor
col_name: referral_url, dtype: text, description: The URL of the page that referred the visitor to the current page
"""

analysis_system_message = """
You are a PostgreSQL expert. Given an analysis request, you return a syntactically correct PostgreSQL query to get the data necessary to answer the request.
    
When generating the PostgreSQL queries, follow the instructions below:
- Remember to aggregate when possible to return only the necessary number of rows.
- Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
- Pay attention to use only the column names you can see in the table given below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
- If the question involves "today", remember to use the CURRENT_DATE function.
- Always use the alias "value" for the numerical value in the query, whether it's a price or volume.
- Write the PostgreSQL query without formatting it in a code block.
- The table name is "egain_visitors".

Think step by step before writing the query plan.

Only return the PostgreSQL query, nothing else.
"""

request_prompt_template = Template(
"""
Request: $input

Use the following tables:
$table_info

"""
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from the server!"})

@app.route('/api/execute-query', methods=['POST'])
def execute_query():
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
            
        # Execute the raw SQL query
        result = db.session.execute(text(query))
        
        # Get column names
        columns = result.keys()
        
        # Convert results to list of dictionaries
        rows = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col] = row[i]
            rows.append(row_dict)
            
        return jsonify({
            'success': True,
            'results': rows,
            'columns': list(columns)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
            
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": analysis_system_message},
                {
                    "role": "user",
                    "content": request_prompt_template.substitute(
                        input=user_message, table_info=table_info
                    ),
                },
            ],
        )
        
        return jsonify({
            'response': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True) 