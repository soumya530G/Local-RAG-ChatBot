## Local RAG ChatBot

## Train of thought

### Ollama
I want to learn how to run AI Agent locally on my computer since I have limited hardware (just an innocent pc with it's cpu) and I do not want to spend anything - yeah I'm cheap like that

Enter: Ollama

Ollama is a free open-source tool that lets people run LLMs directly on your own computer. The prompts and data stay on your own machine so everything's private. It works without internet once downloaded, entirely free, no recurring cloud API costs. And I can run many AI-models, all PC-compatible!!


Great, I got an AI agent running on my pc. 

### Langchain
Now, ollama works for temporary lowkey conversations but I want more. I want it to read the private files (such as csv) or have a memory. Let me look it up 
"How to run local LLM with memory"

> An LLM on its own is like a brain with no memory, no private data access, and no way to use tools. LangChain provides the modular building blocks to bridge those gaps.

Awesome!! Let's see how I can use these two together now

"How to use ollama with langchain"

Great, I've installed all the dependencies. Let's use it!!

### Embedding Model

Alright, but I see a problem. If I search CSV by keyword, that's not enough. A person could be talking about crispy pizza crust w/o containing those words at all!! like "the base of the food was really crunchy" so we need to match on intent. There's one more issue, since context window is limited if my input files grows big, I cannot possibly fit all of it into my poor local llm, it's not mukbang compatible. 

"How to make a local llm model work with intent and not just a simple word lookup and only get relevant rows"

okay so apparently an embedding model can be used here. It converts sentences into numbers so I can get relevant sentences matching the query intent and filter from different rows in the provided input csv. 

### ChromaDB

Great, now where do I store these embeddings that my model made. I can now store embeddings in a file but a plain file cannot perform a search by nearness efficiently since we'd be comparing question against every row ourselves. Let's look it up
"how to save embedding model's output"

> For large-scale retrieval, search, or scaling, store embeddings alongside their metadata directly in a vector store or document store. A vector DB adds that indexed nearest-neighbor search. 

> For a CPU-only mini PC or desktop running Ollama, the best vector databases are ChromaDB, FAISS, or a lightweight turn-key app like AnythingLLM


Hmm..why should I choose chromaDB?

> it works best with python library. Zero-overhead, zero-config configuration that saves straight to a local file folder.

Awesome, how to use chromadb with langchain [langchain integration with chroma](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma)

### Pandas

The basic flow
> read_csv loads the whole file into memory -> pandas row by row turns each into a document (one review = one unit of meaning) -> Document is then sent to chroma -> chroma calls the embedding model internally and turns each one into numbers and stores them. 

### Misc

Now, we cannot overload our model with too much refined data so let's set a limit of k = 5

Prompt template and chain: reviews and questions get combined and handed to the model

os.path.exists: checks whether or not embeddings are built once, not on every run

### Limitations

Retrieval would fail on questions like averages, this is where pandas or a tool-using agent can help us save face. 


