from src.engine import send_prompt
from src.layers import model_instantiate, load_available_funcs, load_prompts
import time
import json
import traceback
import os


def main():
    start = time.time()
    model_ins = model_instantiate()
    av_funcs = load_available_funcs()
    prompts = load_prompts()
    outputs = []
    for pr in prompts:
        outputs.append(send_prompt(model_ins, pr["prompt"], av_funcs))
    end = time.time()
    os.makedirs("output", exist_ok=True)
    parsed_outputs = []
    for out in outputs:
        safe_json_string = out.replace("\\", "\\\\").replace('\\\\"', '\\"')
        parsed_outputs.append(json.loads(safe_json_string))
    with open("output/function_calling_results.json", "w") as fcs:
        json.dump(parsed_outputs, fcs, indent=4)
        print("everything is saved to 'output/function_calling_results.json'")
    print(f"time it took : {(end - start)/60}")


try:
    main()
except (Exception, KeyboardInterrupt) as e:
    print(f"catched a {type(e).__name__}\n{e}")
    print(f"traceback:\n{traceback.print_exc()}")
