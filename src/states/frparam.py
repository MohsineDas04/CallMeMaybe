from src.tools import decode, get_logits
from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


def run_fr_param(
    model_ins: Small_LLM_Model,
    encoded_prompt: list[int],
    closing_tokens: list[int],
    output_list: list[int],
    needed_chars: list[int],
    vocab: dict,
):
    runnable: bool = True
    brace_deltas = {
        vid: token_str.count("{") - token_str.count("}")
        for token_str, vid in vocab.items()
        if "{" in token_str or "}" in token_str
    }
    brace_depth = 2
    while runnable:
        logits = get_logits(model_ins, encoded_prompt)
        token = int(np.argmax(logits))

        # 1. ALWAYS append the token first! (No swallowed quotes or braces)
        encoded_prompt.append(token)
        output_list.append(token)

        # 2. Update the depth IF the token contains a brace
        if token in brace_deltas:
            brace_depth += brace_deltas[token]

            # 3. Check if we just closed the final parameters object
            if brace_depth <= 0:
                runnable = (
                    False  # The loop will break gracefully on the next pass
                )


# this will 100% work
