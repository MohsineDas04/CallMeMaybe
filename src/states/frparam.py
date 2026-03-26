from src.tools import decode, get_logits
from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


def run_fr_param(
    model_ins: Small_LLM_Model,
    encoded_prompt: list[int],
    closing_tokens: list[int],
    output_list: list[int],
    needed_chars: list[int],
):
    runnable: bool = True
    while runnable:
        logits = get_logits(model_ins, encoded_prompt)
        token = int(np.argmax(logits))
        if token in closing_tokens:
            for tok in needed_chars:
                encoded_prompt.append(tok)
                output_list.append(tok)
                runnable = False
        if runnable is False:
            continue
        encoded_prompt.append(token)
        output_list.append(token)


# this will 100% work
