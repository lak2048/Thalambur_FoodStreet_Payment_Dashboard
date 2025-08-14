# To run this, you first need to install Flask:
# pip install Flask

from flask import Flask, render_template
import csv
import os

# Initialize the Flask application
app = Flask(__name__)

DATA_FILE = "shops_data.csv"

def get_shops_data():
    """Reads shop data from the CSV file and returns it as a list of dictionaries."""
    if not os.path.exists(DATA_FILE):
        return []
    
    shops = []
    try:
        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Robust sorting based on the integer part of the shop number
            sorted_rows = sorted(list(reader), key=lambda r: int(''.join(filter(str.isdigit, r.get('shop_num', '0'))) or 0))
            for row in sorted_rows:
                shops.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return shops

# Define the main route for the web application
@app.route('/')
def dashboard():
    """This function runs when someone visits the main page."""
    shops_data = get_shops_data()
    
    # The 'render_template' function will take the HTML file and the data,
    # and combine them to create the final web page.
    return render_template('dashboard.html', shops=shops_data)

# This allows you to run the server by running "python app.py"
if __name__ == '__main__':
    # 'host="0.0.0.0"' makes it accessible on your local network
    app.run(host='0.0.0.0', port=5000, debug=False)

