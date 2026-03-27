# **CallMeMaybe: Function Calling & LLM Evaluation Engine**

Welcome to **CallMeMaybe**, a highly modular, state-driven Python engine designed specifically for testing, evaluating, and managing Large Language Model (LLM) function calling workflows.

This project uses a sophisticated state-machine architecture to parse, encode, and decode LLM interactions. It relies on a local, proprietary SDK (llm\_sdk) and is built to be run exclusively using [**uv**](https://www.google.com/search?q=https://docs.astral.sh/uv/)—a blazingly fast Python dependency manager—orchestrated elegantly via a **Makefile**.

## **📑 Table of Contents**

1. [Deep Dive: Project File Structure](https://www.google.com/search?q=%231--deep-dive-project-file-structure)  
2. [Prerequisites](https://www.google.com/search?q=%232--prerequisites)  
3. [Step 1: Clone the Repository](https://www.google.com/search?q=%233--step-1-clone-the-repository)  
4. [Step 2: Unzip the Local SDK (CRITICAL)](https://www.google.com/search?q=%234--step-2-unzip-the-local-sdk-critical)  
5. [Step 3: Environment Installation](https://www.google.com/search?q=%235--step-3-environment-installation)  
6. [Step 4: Running the Engine](https://www.google.com/search?q=%236--step-4-running-the-engine)  
7. [Developer Tools (Makefile Reference)](https://www.google.com/search?q=%237--developer-tools-makefile-reference)

## **1\. 📂 Deep Dive: Project File Structure**

To understand how CallMeMaybe works, you must understand its modular layout. Every component is isolated by its specific responsibility. Below is the complete, exact structure of the project and its src/ subsystem.

CallMeMaybe/  
├── Makefile                      \# Command orchestrator (install, run, lint, clean)  
├── pyproject.toml                \# Project metadata and dependencies  
├── uv.lock                       \# Deterministic lockfile managed by uv  
├── .python-version               \# Specifies required Python version  
├── .gitignore                    \# Git ignore rules  
├── llm\_sdk.zip                   \# ZIPPED LOCAL DEPENDENCY (Must be extracted\!)  
├── data/  
│   └── input/  
│       ├── function\_calling\_tests.json  \# Input test prompts/cases  
│       └── functions\_definition.json    \# JSON schema of available LLM tools  
├── output/  
│   └── function\_calling\_results.json    \# Generated logs and execution results  
└── src/  
    ├── \_\_main\_\_.py               \# Application entry point  
    ├── data/  
    │   └── states.json           \# State machine transition configurations  
    ├── engine/  
    │   ├── \_\_init\_\_.py  
    │   └── prompter.py           \# Handles assembly and injection of prompts  
    ├── layers/  
    │   ├── \_\_init\_\_.py  
    │   ├── functions\_loader.py   \# Parses tool/function schemas  
    │   ├── instantiator.py       \# Factory module bringing data/models into memory  
    │   ├── prompts\_loader.py     \# Parses the function calling tests  
    │   └── vocabulary\_fetcher.py \# Interfaces with tokenizer for constrained decoding  
    ├── models/  
    │   ├── \_\_init\_\_.py  
    │   └── functions\_data.py     \# Pydantic/Dataclass schemas for strict typing  
    ├── states/  
    │   ├── \_\_init\_\_.py  
    │   ├── foname.py             \# Logic for: Function Output Name  
    │   ├── foparam.py            \# Logic for: Function Output Parameters  
    │   ├── foprompt.py           \# Logic for: Function Output Prompt (General Text)  
    │   ├── frname.py             \# Logic for: Function Request Name  
    │   ├── frparam.py            \# Logic for: Function Request Parameters  
    │   └── frprompt.py           \# Logic for: Initial Function Request Prompt  
    └── tools/  
        ├── \_\_init\_\_.py  
        ├── decoder.py            \# Translates tokens \-\> human-readable text/JSON  
        ├── encoder.py            \# Converts text/JSON \-\> tokenized formats  
        ├── get\_next\_state.py     \# Routing logic for state machine transitions  
        └── logits\_getter.py      \# Fetches/manipulates raw LLM probability arrays

### **🧠 Source Code Highlights (src/)**

* **src/\_\_main\_\_.py**: When you execute the project, this initializes the loaders, sets up the engine, and triggers the core evaluation loop.  
* **src/states/**: The state-machine layer. It processes LLM function calling incrementally, governing what happens at each specific phase (e.g., extracting a tool name vs. parsing a parameter payload).  
* **src/tools/**: Core utilities required to manipulate tokens, restrict outputs (logits\_getter.py), and navigate the state machine (get\_next\_state.py).

## **2\. ⚡ Prerequisites**

To run this project perfectly, you need exactly two things installed globally:

1. **uv**: The modern Python package manager.  
   * **macOS / Linux:** curl \-LsSf https://astral.sh/uv/install.sh | sh  
   * **Windows:** powershell \-ExecutionPolicy ByPass \-c "irm https://astral.sh/uv/install.ps1 | iex"  
2. **make**: Used to execute the Makefile commands.  
   * Pre-installed on macOS/Linux. On Windows, use Git Bash, WSL, or install via Chocolatey (choco install make).

## **3\. 🚀 Step 1: Clone the Repository**

Begin by getting the project files onto your local machine:

git clone \<repository\_url\> CallMeMaybe  
cd CallMeMaybe

*(Ensure your terminal is now at the root folder, where Makefile and pyproject.toml live).*

## **4\. ⚠️ Step 2: Unzip the Local SDK (CRITICAL)**

The core logic of this engine depends on llm\_sdk, which is bundled as a .zip file. **If you skip this step, the installation will permanently fail.**

You must extract llm\_sdk.zip directly into your project root.

### **Command Line Extraction (Recommended):**

* **macOS / Linux:**  
  unzip llm\_sdk.zip

* **Windows (PowerShell):**  
  Expand-Archive \-Path "llm\_sdk.zip" \-DestinationPath "." \-Force

### **Visual Verification Check:**

After extraction, your project root MUST contain the llm\_sdk/ directory alongside the original zip file:

CallMeMaybe/  
├── Makefile  
├── pyproject.toml  
├── llm\_sdk.zip  
├── llm\_sdk/               \<-- THIS UNZIPPED FOLDER MUST EXIST HERE  
│   ├── pyproject.toml  
│   ├── uv.lock  
│   └── llm\_sdk/  
│       └── \_\_init\_\_.py  
└── src/

## **5\. 🛠️ Step 3: Environment Installation**

We use the Makefile to orchestrate the installation via uv.

Run the following command:

make install

**What happens underneath?**

The Makefile executes uv sync. uv will:

1. Read .python-version and download the perfect, isolated Python interpreter.  
2. Link the unzipped llm\_sdk/ directory locally.  
3. Install all dependencies from pyproject.toml into a hidden, hyper-fast virtual environment (.venv).

## **6\. 🎯 Step 4: Running the Engine**

Because uv handles environment boundaries automatically, you never need to run source .venv/bin/activate. You simply use the Makefile.

Run the project:

make run

*(Alternatively, just typing make or make all does the exact same thing).*

**What happens underneath?**

The Makefile runs uv run python \-Bm src. It targets the src/\_\_main\_\_.py file, bypasses compiled byte-code cache checks (-B), and starts the engine. Results are logged directly to output/function\_calling\_results.json.

## **7\. 🧰 Developer Tools (Makefile Reference)**

The provided Makefile includes a suite of commands designed to keep development clean and heavily typed.

### **🧹 make clean**

Cleans up the project environment by:

* Deleting the entire output/ directory (results from previous runs).  
* Finding and deleting all \_\_pycache\_\_ folders recursively.  
* Finding and deleting all .pyc compiled python files.

### **🔎 make lint**

Runs basic code quality checks:

* Executes flake8 to check for PEP-8 styling violations.  
* Executes mypy to check for basic typing errors, ignoring missing imports but disallowing untyped definitions.

### **🛡️ make lint-strict**

Runs aggressive type validation:

* Executes flake8.  
* Executes mypy . \--strict, enforcing absolute type safety across the entire codebase. No untyped code is allowed to pass.

### **🐛 make debug**

Triggers the interactive Python debugger on the entry point:

* Runs pdb3 src/\_\_main\_\_.py. Use this to step through the state machine logic line-by-line.

*Powered by uv. Orchestrated by make. Engineered for Perfection.*