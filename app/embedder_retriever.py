"""
This class implements the indexing service as `embed_documents`.
It also implements a search method  which is a combination of 
`embedder` and `retriever`.
"""

import re

from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import ElasticVectorSearch

import inference


class EmbedderRetriever(object):
    def __init__(
        self,
        model_cache_dir,
        elastic_host,
        environment,
        **kwargs,
    ):
        self.model_cache_dir = model_cache_dir
        self.client = client
        self.project = project
        self.elastic_host = elastic_host

        self.es_index = "temp-index"
        self.chunk_size = kwargs.get("chunk_size", 700)
        self.retrieve_top = kwargs.get("chunk_size", 5)

        self.embeddings = inference.model_fn(model_dir=self.model_cache_dir)
       
        
        self.vectordb = ElasticVectorSearch(self.elastic_host, self.es_index,
                                            self.embeddings)

    def embed_documents(self, documents):
        """
        Indexing Service
        Args:
          documents(List[Document]): List of langchain documents.
        """
        text_splitter = TokenTextSplitter(chunk_size=700, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        texts = [d.page_content for d in docs]
        metadatas = [d.metadata for d in docs]
        self.vectordb.add_texts(texts, metadatas=metadatas)

    def search(self, query):
       docs = self.vectordb.similarity_search(query)
       return [doc.page_content for doc in docs]
