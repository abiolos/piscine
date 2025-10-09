from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from io import StringIO
import sys
import os

from lexer import lexer
from parser import Parser
from interpreter import Interpreter

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '../frontend')

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_DIR, 'js'),
    static_url_path='/js'
)
# Autorise CORS pour les accès frontend
CORS(app, origins=["http://195.15.242.197:8080", "http://localhost:8080"])

# Route principale : sert index.html
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# Sert les fichiers CSS
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)

# API pour exécuter le code
@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')

    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        tree = parser.parse()
        # ici interpreter doit être instancié (exemple)
        interpreter = Interpreter()
        interpreter.eval(tree)

        output = mystdout.getvalue()
        return jsonify({"output": output, "env": interpreter.global_env})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        sys.stdout = old_stdout

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
