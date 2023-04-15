from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        # You can return any data here. Replace the data variable with your data.
        data = {"key": "value"}
        return jsonify(data)
    elif request.method == 'POST':
        # You can access the POSTed data using request.json
        received_data = request.json
        # Process the received data and return a response
        return jsonify({"status": "success", "received_data": received_data})


if __name__ == '__main__':
    app.run(debug=True)
