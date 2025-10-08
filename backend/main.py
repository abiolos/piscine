from flask import Flask, request, jsonify
from flask_cors import CORS   # 👈 ajoute cette ligne
from io import StringIO
import sys

from lexer import lexer
from parser import Parser
from interpreter import Interpreter

app = Flask(__name__)
CORS(app)  # 👈 autorise les requêtes depuis le frontend

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


@app.route('/')
def index():
    return "API du langage personnalisé en Python"


if __name__ == '__main__':
    app.run(debug=True)
