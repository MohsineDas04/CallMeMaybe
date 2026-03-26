from src.tools import decode, get_logits
from llm_sdk.llm_sdk import Small_LLM_Model
from typing import Any
import numpy as np


def run_fr_prompt(
    model_ins: Small_LLM_Model,
    encoded_prompt: list[int],
    vocab: dict,
    output_list: list[int],
):
    full_output: list[int] = []
    runnable = True
    while runnable:
        logits = get_logits(model_ins, encoded_prompt)
        chosen = int(np.argmax(logits))
        decoded_chosen = decode(
            model_ins, [chosen]
        )  # This should be optimized before pushing !!!!
        if '"' in decoded_chosen:
            mask = np.full(logits.shape, -np.inf)
            if "?" in decoded_chosen:
                s_id = vocab['?",']
                mask[s_id] = logits[s_id]
                chosen = int(np.argmax(mask))
                runnable = False
            else:
                s_id = vocab['"']
                mask[s_id] = logits[s_id]
                chosen = int(np.argmax(mask))
                runnable = False
        encoded_prompt.append(chosen)
        output_list.append(chosen)
    logits = get_logits(model_ins, encoded_prompt)
    mask = np.full(logits.shape, -np.inf)
    mask[vocab['Ġ"']] = logits[vocab['Ġ"']]
    chosen = int(np.argmax(mask))
    encoded_prompt.append(chosen)
    output_list.append(chosen)
