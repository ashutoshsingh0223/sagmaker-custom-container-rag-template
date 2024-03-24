import os
from pathlib import Path
from models import models


def model_fn(model_dir: str) -> str:
    """
    Args:
        model_dir (str): _description_
    """
    model_id = os.listdir(model_dir)[0]
    model_details = models[model_id]

    loader = model_details["loader"]
    model = loader(name=model_details["repository"], model_dir=model_dir)

    return model
