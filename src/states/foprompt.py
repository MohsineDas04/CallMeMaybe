from src.tools import decode, get_logits
from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


def run_fo_prompt(
    model_ins: Small_LLM_Model,
    encoded_prompt: list[int],
    needed_vocab_ids: list[int],
    output_list: list[int],
):
    full_output: list[int] = []
    for vocab in needed_vocab_ids:
        encoded_prompt.append(vocab)
        output_list.append(vocab)
