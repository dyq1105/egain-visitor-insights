document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatResponse = document.getElementById('chatResponse');
    const responseText = document.getElementById('responseText');
    const queryResultsHeader = document.getElementById('queryResultsHeader');
    const queryResultsBody = document.getElementById('queryResultsBody');
    const userMessageInput = document.getElementById('userMessage');

    // Function to create table headers from column names
    function createTableHeaders(columns) {
        return `<tr>${columns.map(col => `<th>${col}</th>`).join('')}</tr>`;
    }

    // Function to create table row from data
    function createTableRow(data, columns) {
        return `<tr>${columns.map(col => {
            const value = data[col];
            if (typeof value === 'string' && (value.startsWith('http://') || value.startsWith('https://'))) {
                return `<td><a href="${value}" target="_blank">View</a></td>`;
            }
            return `<td>${value || '-'}</td>`;
        }).join('')}</tr>`;
    }

    // Function to populate query results table
    function populateQueryResults(results, columns) {
        if (!results || results.length === 0) {
            queryResultsHeader.innerHTML = '';
            queryResultsBody.innerHTML = '<tr><td colspan="100%" class="text-center">No results found</td></tr>';
            return;
        }
        
        // Create and set headers
        queryResultsHeader.innerHTML = createTableHeaders(columns);
        
        // Create and set rows
        queryResultsBody.innerHTML = results.map(row => createTableRow(row, columns)).join('');
    }

    // Function to execute SQL query
    async function executeQuery(query) {
        try {
            const response = await fetch('/api/execute-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            const data = await response.json();
            
            if (data.success) {
                populateQueryResults(data.results, data.columns);
                return data.results;
            } else {
                throw new Error(data.error || 'Failed to execute query');
            }
        } catch (error) {
            console.error('Error executing query:', error);
            queryResultsHeader.innerHTML = '';
            queryResultsBody.innerHTML = `<tr><td colspan="100%" class="text-center text-danger">Error: ${error.message}</td></tr>`;
            throw error;
        }
    }

    // Function to handle question submission
    async function handleQuestion(question) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: question }),
            });

            if (response.ok) {
                const data = await response.json();
                responseText.textContent = data.response;
                chatResponse.classList.remove('d-none');

                await executeQuery(data.response);
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error:', error);
            responseText.textContent = 'Error: ' + error.message;
            chatResponse.classList.remove('d-none');
        }
    }

    // Handle predefined question buttons
    document.querySelectorAll('.predefined-question').forEach(button => {
        button.addEventListener('click', (e) => {
            const question = e.target.dataset.question;
            userMessageInput.value = question;
            handleQuestion(question);
        });
    });

    // Handle chat form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userMessage = userMessageInput.value;
        if (!userMessage.trim()) return;

        await handleQuestion(userMessage);
    });
}); 