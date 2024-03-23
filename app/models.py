"""
Simple example to demostrate huggingface hub model loading using langchain. Download the tar.gz file for each model
from hugging face and put them in S3, 
"""

from langchain.embeddings import (
    HuggingFaceInstructEmbeddings,
    HuggingFaceEmbeddings,
)


def hf_embedding_loader(name: str, model_dir: str):
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    
    model = HuggingFaceEmbeddings(
        model_name=name,
        cache_folder=model_dir,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return model


def intructor_embedding_loader(name: str, model_dir: str):
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    model = HuggingFaceInstructEmbeddings(
        model_name=name,
        cache_folder=model_dir,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return model


models = {
    "hkunlp_instructor-xl": {
        "location": "hf_hub",
        "repository": "hkunlp/instructor-xl",
        "loader": intructor_embedding_loader,
    },
    "hkunlp_instructor-large": {
        "location": "hf_hub",
        "repository": "hkunlp/instructor-large",
        "loader": intructor_embedding_loader,
    },

    "sentence-transformers_all-MiniLM-L6-v2":{
        "location": "hf_hub",
        "repository": "sentence-transformers/all-MiniLM-L6-v2",
        "loader": hf_embedding_loader
    }
}
