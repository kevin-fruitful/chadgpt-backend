from config.settings import OPENAI_API_KEY
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from models import Document
from services import DocumentService, CodebaseIndexService, ChatService
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings

app = Flask(__name__)
# app.config["CORS_HEADERS"] = "Content-Type"

# Allow CORS for your frontend origin
CORS(app, origins="*")

# Initialize the OpenAIEmbeddings and DeepLake database instances
embeddings = OpenAIEmbeddings()
deep_lake = DeepLake(dataset_path="mem://langchain",
                     read_only=True, embedding_function=embeddings)

# Initialize the DocumentService and CodebaseIndexService
document_service = DocumentService(deep_lake)
codebase_index_service = CodebaseIndexService(
    document_service, embeddings, deep_lake)

# Set up your DeepLake retriever instance (assuming you have already indexed your dataset)

retriever = deep_lake.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['maximal_marginal_relevance'] = True
retriever.search_kwargs['k'] = 20

# Initialize ChatService
chat_service = ChatService(retriever)
# Now you can use `chat_service.ask()` to interact with the ConversationalRetrievalChain

logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/api/index_codebase', methods=['POST'])
def index_codebase():
    data = request.json
    repo_url = data['git_url']
    use_existing_index = data.get('use_existing_index', False)

    codebase_index_service.index_codebase(repo_url, use_existing_index)

    return jsonify({"success": True, "message": "Codebase indexed successfully."})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data['question']
    chat_history = data.get('chat_history', [])

    answer, chat_history = chat_service.ask(question, chat_history)

    response = {
        'answer': answer,
        'chat_history': chat_history,
    }

    return jsonify(response)


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
    app.run(debug=True, port=8000)
