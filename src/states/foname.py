from llm_sdk.llm_sdk import Small_LLM_Model


def run_fo_name(
    model_ins: Small_LLM_Model,
    encoded_prompt: list[int],
    needed_vocab_ids: list[int],
    output_list: list[int],
) -> None:
    for vocab in needed_vocab_ids:
        encoded_prompt.append(vocab)
        output_list.append(vocab)
