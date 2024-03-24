from typing import List, Dict, Any, Tuple


class DocReader(object):
    def __init__(self, docs: List[Dict[str, Any]]):
        self.docs = docs
        

    def __call__(self) -> List[Document]:
        """
        Read from self.docs and return langchain documents to be
        ingested by the indexing service.

        Returns:
            List[Document]: List of langchain documents.
        """
        raise NotImplementedError
