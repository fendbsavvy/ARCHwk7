import re
import ast
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

app = Flask(__name__)

# Removed Hard-coded password and load environtmet variable
PASSWORD=os.getenv('PASSWORD')

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

# Fix command injection vulnerability
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip):
    	return jsonify({"error": "Invalid IP address"}), 400
    
    # Fix unsafe command execution
    result = subprocess.check_output(["ping", "-c", "1", ip], shell=False)
    return result

# Fix Insecure use of eval
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    if not expression:
       return jsonify({"error": "You must enter an expression"}), 400
    
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
       return jsonify({"error": "Invalid Expression Entered"}), 400

    try:
       # Fix Dangerous use of eval
       result = ast.literal_eval(expression)
    
       return str(result)
    except Exception as e:
      return jsonify({"error": f"Failed:{e}"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
