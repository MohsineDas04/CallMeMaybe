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
        logits = get_logits(model_ins, encoded_prompt)
        mask = np.full(logits.shape, -np.inf)
        mask[vocab] = logits[vocab]
        encoded_prompt.append(int(np.argmax(mask)))
        output_list.append(int(np.argmax(mask)))
