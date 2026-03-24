import json

with open("data/input/function_calling_tests.json") as funcs_tests:
    test_prompts = json.load(funcs_tests)


def load_prompts() -> list:

    return test_prompts
