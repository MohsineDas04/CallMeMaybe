from llm_sdk.llm_sdk import Small_LLM_Model
from typing import List


def encode(model_ins: Small_LLM_Model, prompt: str) -> List:
    return model_ins.encode(prompt).tolist()[0]
