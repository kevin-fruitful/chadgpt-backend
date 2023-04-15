from typing import List
from document import Document
from langchain.vectorstores import DeepLake


class DocumentService:
    def __init__(self, deep_lake: DeepLake):
        self.deep_lake = deep_lake

    def store_document(self, document: Document):
        # Store the document's vector in the DeepLake database
        self.deep_lake.insert(document.id, document.vector)

    def search_documents(self, query_vector: list[float], top_k: int = 10) -> List[Document]:
        # Search for the most similar documents in the DeepLake database
        search_results = self.deep_lake.search(query_vector, top_k=top_k)

        # Retrieve the document metadata (e.g., title, content) for each result
        documents = []
        for result in search_results:
            document_id = result["id"]
            document_vector = result["vector"]

            # Retrieve the document metadata from your own storage system
            # For example, from a relational database or a file system
            title, content = self._get_document_metadata(document_id)

            document = Document(
                id=document_id,
                title=title,
                content=content,
                vector=document_vector
            )
            documents.append(document)

        return documents

    def _get_document_metadata(self, document_id: int):
        # Implement this method to retrieve document metadata from your own storage system
        # For example, from a relational database or a file system
        raise NotImplementedError(
            "Retrieve document metadata from your storage system")
