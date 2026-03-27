# **Constrained LLM Function Calling Engine**

A Python-based framework designed to execute structured function calling with small Large Language Models (LLMs). This project utilizes **constrained token-level decoding** to guarantee that the LLM outputs perfectly formatted, parseable JSON function calls without relying on the model's instruction-following capabilities alone.

## **🚀 Features**

* **State-Machine Guided Generation**: The engine transitions between "Forced" (FO) and "Free" (FR) states. It forces the structural JSON syntax tokens and only allows the LLM to freely generate the actual values.  
* **Guaranteed JSON Output**: By hijacking the logits and forcing exact tokens (like {"name": "), the system is immune to common LLM formatting errors, dropped braces, or hallucinated keys.  
* **Pydantic Data Models**: Uses Pydantic to strictly type and validate function definitions and parameter schemas.  
* **Modular Architecture**: Cleanly separated into engine (orchestration), states (generation phases), layers (I/O and instantiation), and tools (LLM wrappers).

## **📂 Project Structure**

.  
├── data/  
│   └── input/  
│       ├── functions\_definition.json   \# JSON schema of available functions  
│       └── function\_calling\_tests.json \# Test prompts/tasks for the LLM  
├── output/                             \# Generated automatically  
│   └── function\_calling\_results.json   \# The final parsed JSON results  
└── src/  
    ├── \_\_main\_\_.py                     \# Main execution pipeline  
    ├── engine/                         \# Core prompter and orchestration  
    ├── layers/                         \# Data loading and model instantiation  
    ├── models/                         \# Pydantic schema definitions  
    ├── states/                         \# Token generation state handlers  
    └── tools/                          \# Encoders, decoders, and logits tools

## **🧠 How It Works: The Decoding States**

To ensure perfect JSON syntax, the prompter.py engine breaks down the response generation into discrete phases:

1. **foprompt (Forced Prompt)**: Forces the model to generate the opening JSON syntax and the prompt key: {"prompt": ".  
2. **frprompt (Free Prompt)**: Allows the model to generate the task text freely, waiting for the closing quote ",.  
3. **foname (Forced Name)**: Forces the JSON key for the function name: "name": ".  
4. **frname (Free Name)**: Allows the model to predict the target function name freely using logits.  
5. **foparam (Forced Parameters)**: Forces the syntax for the parameter dictionary: "parameters": {.  
6. **frparam (Free Parameters)**: Allows the model to generate the parameters, actively tracking brace-depth ({ vs }) to know exactly when the JSON object is safely closed.

## **📋 Prerequisites**

* **Python 3.8+**  
* **Dependencies**:  
  uv sync  
* **LLM SDK**: This project requires the proprietary/custom llm\_sdk module (specifically llm\_sdk.llm\_sdk.Small\_LLM\_Model) to interact with the base model, encode/decode tokens, and fetch raw logits.

## **⚙️ Setup & Usage**

1. **Prepare Input Data**: Ensure your input files are placed correctly in the data/input/ directory relative to your working directory.  
   *functions\_definition.json example*:  
   \[  
     {  
       "name": "get\_weather",  
       "description": "Get current weather in a location",  
       "parameters": {"location": {"type": "string"}},  
       "returns": {"type": "string"}  
     }  
   \]

   *function\_calling\_tests.json example*:  
   \[  
     {"prompt": "What is the weather like in Paris today?"}  
   \]

2. **Run the Engine**:  
   Execute the module from the root of your project:  
   uv run python \-Bm src

3. **View Results**:  
   Once the run is complete, the structured outputs will be safely serialized and saved to output/function\_calling\_results.json. The engine handles escaping nested quotes and ensures safe JSON loading before saving.

## **🛠️ Development & Extending**

* **Adding New States**: To add new forced/free generation steps (e.g., forcing a reasoning/Chain-of-Thought step before the function call), define the new states in src/states/ and register them in src/data/states.json and src/tools/get\_next\_state.py.  
* **Updating Prompts**: Modify src/engine/prompter.py to change the system prompt format injected via encode().

## **⚠️ Error Handling**

The main execution loop is wrapped in a robust try-except block. If the target model hallucinates invalid syntax that escapes the brace-depth checker, or if the llm\_sdk fails to load vocabularies, the traceback will be caught and printed safely to the console without crashing background processes.