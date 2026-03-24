from llm_sdk.llm_sdk import Small_LLM_Model
from typing import List


def decode(model_ins: Small_LLM_Model, input_ids: List[int]) -> str:
    return model_ins.decode(input_ids)
