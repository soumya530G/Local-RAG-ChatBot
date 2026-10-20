from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2:1b")

template = """
You are an expert in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n--------------------------az--------------------------\n\n")
    question = input("Enter your question (or 'exit' to quit): ")
    print("\n\n")
    if question == "exit":
        break
    reviews = retriever.invoke(question)
    result = chain.invoke({
        "reviews": reviews, "question": question
    })
    print(result)

