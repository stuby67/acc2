# Flask SQL Chatbot

This project is a chatbot interface that converts English questions into SQL queries using Google Generative AI. The chatbot interacts with an SQLite database and returns 
the results of the queries. 
The project is implemented using Flask Framework.

# Features

 Converts natural language questions into SQL queries.
 Executes the SQL queries to an SQLite database.
 Displays the results of the queries in chat.


# Requirements

  Python 3.9
  
  Flask
  
  SQLite3
  
  Google Generative AI API
  

# Setup
  Clone the repository.
  
  Visit https://ai.google.dev/gemini-api/docs/api-key and get a gemini api key. Keep the key safe and private.
  
  Copy the api key. Open the file app.py present in the folder. Paste the api key in the "your_api" in genai.configure
  
  Open the folder in Code Editor(VS code)
  
  Then install the requirement.txt file using pip install -r requirement.txt.
  
  Execute the sql.py file to create a sqlite3 database.(IF YOU WANT you can modify the SQL code to make chatbot work for other application usage-if you change the database, 
  you also need to change the prompt present in app.py accordingly and update database tables. Offer a few shot learning and the chatbot is ready to use for OTHER CASES )
 
  In the terminal, type the command : 
  
        set FLASK_APP=app.py
        
        set FLASK_ENV=development        
        
        flask run
        
  Open the port on which the app is running. Chatbot appears at the right bottom of the screen.        




# Usage
To use the chatbot, type a question in natural language and the chatbot will convert it to an SQL query, execute it, and display the results. 
If an error occurs, it will prompt you to rephrase the query.

# Example Questions

"How many sales records are there?"
"Show all sales records for the product with ID 1."
"List the salesid and qty for orders placed by the customer with ID 3."
"What is the total quantity sold for the product with ID 5?"

# Handling Errors

Following errors can occur: API error, BlankResponse, InvalidColumn, Result fetch error, Ajax Route error
all errors are handled properly

If an error occurs during the question processing or SQL query execution, the chatbot will respond with "Please rephrase the query."
Provide paraphrased query
eg: sales foodies(ERROR)
    list the sales of foodies company (CORRECT)


This README file provides a guide on to setup, run and use the project. 
Adjust the content as needed to match your specific project details.
        
