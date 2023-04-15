from flask import Flask, jsonify, requests
from models import Document
from services import DocumentService, CodebaseIndexService
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings

app = Flask(__name__)

# Initialize the OpenAIEmbeddings and DeepLake instances
embeddings = OpenAIEmbeddings()
deep_lake = DeepLake()

# Initialize the DocumentService and CodebaseIndexService
document_service = DocumentService(deep_lake)
codebase_index_service = CodebaseIndexService(
    document_service, embeddings, deep_lake)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/index_codebase', methods=['POST'])
def index_codebase():
    data = requests.json
    repo_url = data['repo_url']
    use_existing_index = data.get('use_existing_index', False)

    codebase_index_service.index_codebase(repo_url, use_existing_index)

    return jsonify({"success": True, "message": "Codebase indexed successfully."})


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if requests.method == 'GET':
        # You can return any data here. Replace the data variable with your data.
        data = {"key": "value"}
        return jsonify(data)
    elif requests.method == 'POST':
        # You can access the POSTed data using request.json
        received_data = requests.json
        # Process the received data and return a response
        return jsonify({"status": "success", "received_data": received_data})


if __name__ == '__main__':
    app.run(debug=True)
