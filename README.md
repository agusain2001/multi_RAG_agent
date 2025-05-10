# RAG-Powered Multi-Agent Knowledge Assistant
- link of this application :- https://agusain2001-multi-rag-agent-app-qzjuoo.streamlit.app/  
- A question-answering system combining Retrieval-Augmented Generation (RAG) with tool-calling agents using Google Gemini and FAISS.

## Features

- Document retrieval from a custom knowledge base.
- Integrated Calculator and Dictionary tools.
- User-friendly Streamlit web interface.
- Powered by Google Gemini.
- Utilizes FAISS for efficient vector storage and similarity search.

## Installation

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- A Google API Key (a free tier is available from Google AI Studio)

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**For Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**For Linux/MacOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

Once your virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

---

### Configuration

#### Get Your Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/).
2. Sign in or create an account.
3. Create a new API key.

#### Set Your Google API Key

You need to set your Google API key as an environment variable. Choose one of the following methods:

**Option 1: Temporary (Command Line)**

* **Windows (Command Prompt):**

```bash
set GOOGLE_API_KEY=your-api-key
```

* **Windows (PowerShell):**

```powershell
$env:GOOGLE_API_KEY="your-api-key"
```

* **Linux/MacOS:**

```bash
export GOOGLE_API_KEY=your-api-key
```

Replace `your-api-key` with the actual key you obtained.

**Option 2: Permanent (.env file)**

1. Create a file named `.env` in the project root.
2. Add the following line:

```
GOOGLE_API_KEY=your-api-key
```

The application uses `python-dotenv` to automatically load this key.

---

### Usage

#### 1. Add Your Documents

Place your custom text documents into the `data/sample_docs/` directory. Currently, supported formats include `.txt` files.

#### 2. Run the Application

Navigate to the project's root directory in your terminal (ensure your virtual environment is active and the API key is set) and run:

```bash
streamlit run app.py
```

This will typically open the web interface in your default browser.

#### 3. Ask Questions in the Web Interface

Once running, interact via the web interface:

* **RAG Questions:** Ask based on your documents (e.g., "What is the company's return policy?").
* **Calculator:** Perform calculations (e.g., "Calculate 15% of 80").
* **Dictionary:** Get definitions (e.g., "Define quantum computing").

---

### Project Structure

```
├── data/
│   └── sample_docs/          # Add your custom documents here (e.g., .txt files)
├── src/
│   ├── data_ingestion.py     # Handles document loading and text chunking
│   ├── vector_store.py       # Manages FAISS index creation and retrieval
│   ├── llm_integration.py    # Integrates with Google Gemini for answer generation
│   ├── tools.py              # Defines callable tools like Calculator and Dictionary
│   └── agent.py              # Orchestrates the workflow between RAG, tools, and LLM
├── app.py                    # Main Streamlit web application interface
├── requirements.txt          # Lists all Python dependencies for the project
└── .env                      # Optional file for storing API keys (e.g., GOOGLE_API_KEY)
```

---

### Dependencies

#### Core Dependencies

* `langchain-community==0.2.1`
* `langchain-google-genai==0.1.2`
* `google-generativeai==0.3.2`
* `faiss-cpu==1.8.0`
* `streamlit==1.35.0`
* `python-dotenv==1.0.1`

#### Optional Dependencies (Windows)

If you encounter issues with document loading:

* `python-magic-bin==0.4.14`

This may help resolve issues related to file type identification.

---

### Troubleshooting

**Q: I'm getting API key errors.**

* A1: Double-check that the `GOOGLE_API_KEY` environment variable is correctly set.
* A2: Ensure `.env` file is in the project root and properly formatted.
* A3: Restart your terminal after setting the environment variable.
* A4: Verify the API key is enabled in your Google Cloud Console or AI Studio.

**Q: I'm encountering missing dependencies errors.**

* A: Ensure your virtual environment is active, then run:

```bash
pip install --upgrade -r requirements.txt
```

**Q: Streamlit is not working or not found.**

* A1: Upgrade pip and reinstall Streamlit:

```bash
python -m pip install --upgrade pip
pip install streamlit
```

* A2: Ensure you run the command from the root directory:

```bash
streamlit run app.py
```

**Q: Issues with document loading (e.g., "magic" related errors).**

* A1: Install unstructured with text support:

```bash
pip install "unstructured[text]"
```

* A2: On Windows, ensure `python-magic-bin` is installed:

```bash
pip install python-magic-bin
```
