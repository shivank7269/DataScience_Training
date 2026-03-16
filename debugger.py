from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

from transformers import pipeline

print("Loading pdf...")
reader = PdfReader("Dataset/Introduction_to_Data_Science.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

print("Document Loaded")

# Splitting document

print("Splitting document into chunks")

def chunk_text(text):
    chunk_size = 200
    overlap = 50

    chunks=[]
    start = 0

    while start < len(text):
        end = start+chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap
    return chunks

chunks = chunk_text(text)
print("Total Chunks Created :",len(chunks))

# Embed Data

print("Loading Embedding Model ...")
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding Model Loaded")

# create vector db

client = chromadb.Client()
collection = client.create_collection("pdf_collection")

# store chunks in vector
for i,chunk in enumerate(chunks):
    embedding = embedding_model.encode(chunk).tolist()
    collection.add(
        documents = [chunk],
        embeddings = [embedding],
        ids = [str(i)]
    )

print("All chunks stored successfully")

# retrieve the data

def retrieve(query,k=3):
    query_embedding = embedding_model.encode(query).tolist()

    result = collection.query(
        query_embeddings = [query_embedding],
        n_results=k
    )
    return result["documents"][0]

# load the llm
print("Loading llm")
qa_pipeline = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)
print("LLM LOADED SUCCESSFULLY")

# answer question

def answer_question(query):
    context_docs = retrieve(query)
    context = " ".join(context_docs)

    prompt = f"""
You are an AI assistant.
Answer using ONLY the context below.

Context:
{context}

Question:
{query}

If the answer is not present say "Not found in document".

Answer:
"""

    response = qa_pipeline(
        prompt,
        max_new_tokens=120,
        temperature=0.5,
        do_sample=True
    )

    return response[0]["generated_text"].replace(prompt, "").strip()

# QUestion ANSWER
print("\n==============================")
print("RAG Chatbot Ready")
print("Type 'exit' to stop")
print("==============================\n")

while True:

    question = input("Ask a question | type 'exit' to quit: ")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    answer = answer_question(question)

    print("\nAnswer:\n", answer)
