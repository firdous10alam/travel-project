# app.py
from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin

# Create a Flask application instance
app = Flask(__name__)
CORS(app)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for search_tokyo and apply CORS
@app.route('/search_tokyo')
@cross_origin()
def search_tokyo():
    # Your endpoint logic here
    return jsonify(message='Search results for Tokyo')

# Additional routes can be defined here
# e.g., @app.route('/about')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
