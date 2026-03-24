from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any
import json


def get_vocabulary(model_ins: Small_LLM_Model) -> Any:
    vocab_path = model_ins.get_path_to_vocab_file()
    with open(vocab_path, "r") as vf:
        vocabs: dict = json.load(vf)
    return vocabs
