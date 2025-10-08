from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from io import StringIO
import sys
import os

from lexer import lexer
from parser import Parser
from interpreter import Interpreter

# 🧭 Configuration des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '../frontend')

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_DIR, 'js'),
    static_url_path='/js'
)
CORS(app)

# 🚀 Route principale : sert index.html
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# 🎨 Sert les fichiers CSS
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)

# 🧠 API pour exécuter le code
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

        interpreter = Interpreter()
        interpreter.eval(tree)

        output = mystdout.getvalue()
        response = {'output': output.strip(), 'env': interpreter.env}

    except Exception as e:
        response = {'error': str(e)}

    finally:
        sys.stdout = old_stdout

    return jsonify(response)


if __name__ == '__main__':
    print("🚀 Serveur lancé sur http://127.0.0.1:5000")
    app.run(debug=True)
