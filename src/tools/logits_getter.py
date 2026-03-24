from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


def get_logits(model_ins: Small_LLM_Model, input_ids: list[int]):
    logits = model_ins.get_logits_from_input_ids(input_ids)
    return np.array(logits)
