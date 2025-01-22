from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import google.generativeai as genai
import logging
import sqlite3
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure key

# Configure Google Generative AI
genai.configure(api_key="your_google_gen_ai_api_key_here")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Dummy in-memory database for user credentials (replace with a database for production)
USERS = {"admin": "password123", "gstexpert": "gst@expert"}

TRANSACTIONS_FILE = 'transactions.json'

def read_transactions():
    try:
        with open(TRANSACTIONS_FILE, 'r') as file:
            transactions = json.load(file)
        return transactions
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if the file doesn't exist or is empty

def write_transactions(transactions):
    try:
        with open(TRANSACTIONS_FILE, 'w') as file:
            json.dump(transactions, file, indent=4)
    except Exception as e:
        app.logger.error(f"Error writing to JSON file: {e}")

def get_gemini_response(question):
    try:
        # Use the Gemini model to process the question
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"You are an expert in Goods and Services Tax (GST). Your role is to provide clear, "
            f"professional, and actionable guidance related to GST queries. "
            f"Answer the following question in a clean, formatted manner without using unnecessary symbols or characters:\n\n"
            f"Question: {question}\n\n"
            f"Response:"
        )
        response = model.generate_content([prompt])
        if response and hasattr(response, 'text') and response.text.strip():
            return response.text.strip()
        else:
            logging.error("Empty or invalid response from Generative AI.")
            return "Sorry, I couldn't understand your query. Please try rephrasing or provide more details."
    except Exception as e:
        logging.error(f"Error generating response from Generative AI: {e}")
        return "An error occurred while processing your request. Please try again later."

def fetch_latest_news():
    try:
        # Hardcoded latest news
        news = [
            {
                "title": "GST Collections Hit All-Time High in January 2025",
                "link": "https://example.com/gst-collections-jan-2025",
                "snippet": "India's GST collections have reached an all-time high, reflecting economic recovery and better compliance."
            },
            {
                "title": "Government Plans Major GST Overhaul",
                "link": "https://example.com/gst-overhaul-plans",
                "snippet": "A significant restructuring of the GST framework is on the cards, aimed at reducing compliance burden for businesses."
            },
            {
                "title": "E-Invoicing Mandatory for Businesses Above ₹5 Crore",
                "link": "https://example.com/e-invoicing-mandate",
                "snippet": "The government has made e-invoicing compulsory for businesses with an annual turnover above ₹5 crore starting April 2025."
            },
            {
                "title": "GST Council Discusses Rate Rationalization",
                "link": "https://example.com/gst-rate-discussion",
                "snippet": "The GST Council is deliberating on rationalizing tax rates to simplify the system and boost revenues."
            },
            {
                "title": "Key Amendments in GST Law to Be Effective Soon",
                "link": "https://example.com/gst-law-amendments",
                "snippet": "Upcoming amendments in GST laws will address input tax credit concerns and enhance tax compliance measures."
            },
        ]
        return news
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return [{"title": "Unable to fetch news. Please try again later.", "link": "#", "snippet": ""}]

@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/ask_ajax', methods=['POST'])
def ask_ajax():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        if not question:
            return jsonify({"response": "Please provide a valid question."})
        response = get_gemini_response(question)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error in ask_ajax route: {e}")
        return jsonify({"response": "An unexpected error occurred. Please try again later."})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS:
            return render_template('signup.html', error="Username already exists. Please try another.")
        USERS[username] = password
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session.get('user'))

@app.route('/news')
def news():
    news_data = fetch_latest_news()
    return render_template('news.html', news=news_data)
@app.route('/transactions', methods=['GET','POST'])
def transactions():
    if request.method == 'POST':
        try:
            # Extract form data
            transaction_type = request.form.get('transaction_type')
            party_name = request.form.get('party_name')
            description = request.form.get('description')
            quantity = request.form.get('quantity')
            total_value = request.form.get('total_value')
            payment_detail = request.form.get('payment_detail')

            # Log the received data
            app.logger.info(f"Form data received: {transaction_type}, {party_name}, {description}, {quantity}, {total_value}, {payment_detail}")

            # Store the transaction in a JSON file (or database as needed)
            transactions = read_transactions()
            transactions.append({
                "transaction_type": transaction_type,
                "party_name": party_name,
                "description": description,
                "quantity": quantity,
                "total_value": total_value,
                "payment_detail": payment_detail
            })
            write_transactions(transactions)
            flash("Transaction added successfully!", "success")
            
        except Exception as e:
                app.logger.error(f"Error inserting transaction: {e}")
                flash("Error adding transaction. Please try again.", "danger")

        return redirect(url_for('ledgers'))

    return render_template('transactions.html')
@app.route('/ledgers')
def ledgers():
    # Read transactions from the JSON file
    transactions = read_transactions()

    return render_template('ledgers.html', data=transactions)

if __name__ == '__main__':
    
    app.run(debug=True)
