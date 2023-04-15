import os
import shutil
from git import Repo
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from models import Document
from services import DocumentService
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


class CodebaseIndexService:
    def __init__(self, document_service: DocumentService, embeddings: OpenAIEmbeddings, vectordb: Chroma):
        self.document_service = document_service
        self.embeddings = embeddings
        self.vectordb = vectordb

    def index_codebase(self, repo_url: str, use_existing_index: bool):
        if not use_existing_index:
            repo_path = './cloned_repo'  # todo update this path
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            Repo.clone_from(repo_url, repo_path)

            docs = []
            for dirpath, _, filenames in os.walk(repo_path):
                for file in filenames:
                    try:
                        loader = TextLoader(os.path.join(
                            dirpath, file), encoding='utf-8')
                        docs.extend(loader.load_and_split())
                    except Exception as e:
                        pass

            text_splitter = CharacterTextSplitter(
                chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(docs)

            self.vectordb.from_documents(texts, self.embeddings)

            # for text in texts:
            #     title = os.path.basename(text[0])
            #     content = text[1]
            #     embedding = self.embeddings(content)
            #     document = Document(
            #         title=title, content=content, vector=embedding)
            #     self.vectordb.add(document, embedding)

            # for text in texts:
            #     document = Document(text)
            #     embedding = self.embeddings(text)
            #     self.vectordb.add(document, embedding)
