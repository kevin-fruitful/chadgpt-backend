from config.settings import OPENAI_API_KEY
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from services import DocumentService, CodebaseIndexService, ChatService
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.vectorstores import Chroma
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

app = Flask(__name__)
# app.config["CORS_HEADERS"] = "Content-Type"

# Allow CORS for your frontend origin
CORS(app, origins="*")

# Initialize the OpenAIEmbeddings and DeepLake database instances
embeddings = OpenAIEmbeddings()

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = 'db'
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

loader = TextLoader('./memory/hi.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

seed_data = './memory'  # todo update this path


if os.path.exists(persist_directory):
    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=embeddings)
else:
    vectordb = Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embeddings)

# Initialize the DocumentService and CodebaseIndexService
document_service = DocumentService(vectordb)

codebase_index_service = CodebaseIndexService(
    document_service, embeddings, vectordb)


retriever = vectordb.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['maximal_marginal_relevance'] = True
retriever.search_kwargs['k'] = 14

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

    codebase_index_service.index_codebase(
        repo_url, use_existing_index)

    return jsonify({"success": True, "message": "Codebase indexed successfully."})


@app.route('/api/chat', methods=['POST'])
def chat():

    # After initializing vectordb, add the following line:
    data = request.json
    question = data['question']
    chat_history = data.get('chat_history', [])

    answer, chat_history = chat_service.ask(question, chat_history)

    response = {
        'answer': answer,
        'chat_history': chat_history,
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
