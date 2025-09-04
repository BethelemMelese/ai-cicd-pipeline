from flask import Flask, request, jsonify
from .operations import add, subtract, multiply, divide

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({"message": "Calculator API is running."})

@app.route('/add')
def add_route():
    try:
        a = float(request.args.get('a', ''))
        b = float(request.args.get('b', ''))
        return jsonify({"result": add(a, b)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/subtract')
def subtract_route():
    try:
        a = float(request.args.get('a', ''))
        b = float(request.args.get('b', ''))
        return jsonify({"result": subtract(a, b)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/multiply')
def multiply_route():
    try:
        a = float(request.args.get('a', ''))
        b = float(request.args.get('b', ''))
        return jsonify({"result": multiply(a, b)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/divide')
def divide_route():
    try:
        a = float(request.args.get('a', ''))
        b = float(request.args.get('b', ''))
        return jsonify({"result": divide(a, b)})
    except ZeroDivisionError as zde:
        return jsonify({"error": str(zde)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
