from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Route for the main portfolio page
@app.route('/')
def home():
    return render_template('index.html')

# Route to serve the additional HTML pages in static/assets/html_pages/
@app.route('/static/assets/html_pages/<path:filename>')
def serve_docs(filename):
    return send_from_directory(os.path.join('static', 'assets', 'html_pages'), filename)

if __name__ == '__main__':
    app.run(debug=True)
