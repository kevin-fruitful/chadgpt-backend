class Document:
    def __init__(self, id: int, title: str, content: str, vector: list[float]):
        self.id = id
        self.title = title
        self.content = content
        self.vector = vector

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "vector": self.vector,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            vector=data["vector"],
        )
