from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import lexer
from parser import Parser
from interpreter import Interpreter
import sys
import io

app = Flask(__name__)
CORS(app)
interpreter = Interpreter()

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        tokens = lexer(code)
        tree = Parser(tokens).parse()
        interpreter.eval(tree)
        output = redirected_output.getvalue()
        return jsonify({"output": output, "env": interpreter.global_env})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        sys.stdout = old_stdout

if __name__ == "__main__":
    app.run(debug=True)
