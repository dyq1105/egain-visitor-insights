# eGain Visitor Insights

This is a demo / sample application that extracts insights on the eGain visitor data that was provided as part of the
project challenge.

## Features

In order to be flexible & scalable with respect to desired analytics, I integrated the application w/ OpenAI
GPT 4o so it can generate queries based on natural language (vs. fixed metric dashboard).

Features include:

- **Natural Language Interface**: Ask questions about visitor data in plain English
- **Predefined Questions**: Predefined common queries for quick access to popular metrics
- **SQL Transparency**: Display converted SQL language to increase confidence
- **Dynamic Results Table**: Automatically formatted table display for query results

In the future, the application could be extended to post-process results into more meaningful charts
and visuals.

## Predefined Queries

The application suports a few pre-defined quick-access queries the user can exercise:
- Top 5 organizations by number of visits
- Top 5 pages by number of visits
- Total visits per day
- Top 5 referral sources

## Technology Stack

I heavily used Cursor AI to to help w/ the development of this application and integrating the various
pieces. Most of these choice were decided by the AI tool, but the dependencies are kept to a minimal.

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Database system
- **OpenAI API**: For natural language processing
- **AWS**: Cloud server
- **IPinfo**: Map IP address to geography and organizations

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling
- **Bootstrap 5**: UI framework
- **JavaScript**: Client-side functionality

## Dependencies

### Python Dependencies
```
Flask==3.0.2
python-dotenv==1.0.1
psycopg2-binary==2.9.9
Flask-SQLAlchemy==3.1.1
openai==1.12.0
```

### Frontend Dependencies
```
Bootstrap 5.3.0
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/dyq1105/egain-visitor-insights.git
   cd egain-visitor-insights
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

5. **Set up the database**
   - Ensure PostgreSQL is installed and running
   - Create the database and tables using the provided SQL schema

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Using Quick Insights**
   - Click on any of the predefined query buttons
   - View results in the dynamic table below

2. **Custom Queries**
   - Type your question in the text area
   - Click "Submit" to execute the query
   - View the AI response and query results from the database

3. **Viewing Results**
   - Results are displayed in a dynamic table
   - URLs are automatically converted to clickable links
   - Empty values are shown as '-'

## Project Structure

```
egain-visitor-insights/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # Frontend JavaScript
└── templates/
    └── index.html        # Main HTML template
```

## Questions

For any questions, please contact me!
