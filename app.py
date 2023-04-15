from config.settings import OPENAI_API_KEY
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from models import Document
from services import DocumentService, CodebaseIndexService, ChatService
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

app = Flask(__name__)
# app.config["CORS_HEADERS"] = "Content-Type"

# Allow CORS for your frontend origin
CORS(app, origins="*")

# Initialize Pinecone
# pinecone.deinit()
pinecone.init()


# Initialize the OpenAIEmbeddings and DeepLake database instances
embeddings = OpenAIEmbeddings()


# Initialize the DocumentService and CodebaseIndexService
document_service = DocumentService(deep_lake)
# Set up your Pinecone instance
pinecone_vector_store = Pinecone(document_service,
                                 namespace="langchain", embedding_function=embeddings, index_name="chad-gpt-ethTokyo")
deep_lake = DeepLake(vectorstore=pinecone_vector_store, read_only=False,
                     embedding_function=embeddings)
codebase_index_service = CodebaseIndexService(
    document_service, embeddings, deep_lake)


retriever = deep_lake.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['maximal_marginal_relevance'] = True
retriever.search_kwargs['k'] = 20

# Initialize ChatService
chat_service = ChatService(retriever)

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

    # After initializing deep_lake, add the following line:
    print("Dataset size:", len(deep_lake))
    data = request.json
    question = data['question']
    chat_history = data.get('chat_history', [])

    answer, chat_history = chat_service.ask(question, chat_history)

    response = {
        'answer': answer,
        'chat_history': chat_history,
    }

    return jsonify(response)


@app.teardown_appcontext
def shutdown_pinecone(exception=None):
    pinecone.deinit()


if __name__ == '__main__':
    app.run(debug=True, port=8000)
