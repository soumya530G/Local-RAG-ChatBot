# Local Restaurant Review Chatbot

A small, CPU-friendly retrieval-augmented generation (RAG) chatbot that answers questions about restaurant reviews using local Ollama models. It retrieves a handful of relevant reviews from a CSV with ChromaDB, then gives those reviews and the question to a local language model.

## How It Works

1. `vector.py` loads `realistic_restaurant_reviews.csv` with pandas.
2. Each review's title and text are embedded with Ollama's `mxbai-embed-large` model and stored in a persistent ChromaDB collection.
3. The user's question is used to retrieve the five most relevant reviews.
4. `main.py` sends those reviews and the question to Ollama's `llama3.2:1b` model, then prints the answer in the terminal.

## Requirements

- Python 3.14 or later, as declared in `pyproject.toml`
- [Ollama](https://ollama.com/) installed and running locally
- The project dependencies from `requirements.txt`

Download both models before running the chatbot:

```bash
ollama pull llama3.2:1b
ollama pull mxbai-embed-large
```

## Run

From the project directory, install the Python dependencies and start the chatbot:

```bash
python -m pip install -r requirements.txt
python main.py
```

Type a question about the restaurant's reviews at the prompt. Enter `exit` to quit. The CSV is expected to have `Title`, `Date`, `Rating`, and `Review` columns.

The vector store is saved in `chroma_langchain_db/`. The current code builds the index only when this directory does not exist; if you change the CSV and want to rebuild the index, remove that directory before starting the application again.

## Notes

## Train of thought

### Ollama

I want to learn how to run an AI agent locally on my computer. I have limited hardware (just an innocent PC with its CPU), and I do not want to spend anything - yeah, I'm cheap like that.

Enter: Ollama.

Ollama is a free, open-source tool that lets people run LLMs directly on their own computer. The prompts and data stay on my machine, so everything is private. It works without internet once the models are downloaded, with no recurring cloud API costs. And I can run many PC-compatible AI models!

Great, I got an AI agent running on my PC.

### LangChain

Now, Ollama works for temporary low-key conversations, but I want more. I want it to read private files (such as CSVs) or have a memory. Let me look it up:

"How to run local LLM with memory"

> An LLM on its own is like a brain with no memory, no private data access, and no way to use tools. LangChain provides the modular building blocks to bridge those gaps.

Awesome! Let's see how I can use these two together:

"How to use ollama with langchain"

Great, I've installed all the dependencies. Let's use it!

### Embedding model

Alright, but I see a problem. If I search a CSV by keyword, that's not enough. A person could be talking about crispy pizza crust without using those words at all, like "the base of the food was really crunchy." We need to match on intent.

There's one more issue: if my input files grow big, I cannot possibly fit all of them into my poor local LLM's context window. It's not mukbang-compatible.

"How to make a local LLM model work with intent and not just a simple word lookup and only get relevant rows"

Okay, so apparently an embedding model can be used here. It converts sentences into numbers, so I can find sentences that match the query's intent and retrieve relevant rows from the CSV.

### ChromaDB

Great, now where do I store these embeddings that my model made? I can store embeddings in a file, but a plain file cannot search by nearness efficiently since we'd have to compare the question against every row ourselves. Let's look it up:

"how to save embedding model's output"

> For large-scale retrieval, search, or scaling, store embeddings alongside their metadata directly in a vector store or document store. A vector DB adds that indexed nearest-neighbor search.

> For a CPU-only mini PC or desktop running Ollama, the best vector databases are ChromaDB, FAISS, or a lightweight turn-key app like AnythingLLM.

Hmm... why should I choose ChromaDB?

> It works best with the Python library. Zero-overhead, zero-config configuration that saves straight to a local file folder.

Awesome, here's how to use ChromaDB with LangChain: [LangChain integration with Chroma](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma).

### Pandas

The basic flow:

> `read_csv` loads the whole file into memory -> pandas turns each row into a document (one review = one unit of meaning) -> the document is sent to Chroma -> Chroma calls the embedding model internally, turns the text into numbers, and stores them.

### Misc

Now, we cannot overload our model with too much refined data, so let's set a limit of `k = 5`.

A prompt template and chain combine the reviews and the question, then hand them to the model.

`os.path.exists` checks whether embeddings have already been built, so they are not rebuilt on every run.

### Limitations

Retrieval would fail on questions like "what's the average rating?" This is where pandas or a tool-using agent can help us save face.
