from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

import json
import os
import dotenv
from uuid import uuid4

dotenv.load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=gemini_api_key
)

pc = Pinecone(api_key=pinecone_api_key)
index_name = "practice1"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )

index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)


docs = []
ids = {}
new_docs = []
new_ids = []

files = [
    "data/lesson_rag/files/future_of_ai.txt",
    "data/lesson_rag/files/intro.txt",
    "data/lesson_rag/files/machine_learning.txt",
    "data/lesson_rag/files/neural_networks.txt"
]

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    doc = Document(
        page_content=text,
        metadata={"path": file}
    )

    doc_id = str(uuid4())
    docs.append(doc)
    new_ids.append(doc_id)
    ids[file] = doc_id


huge_path = "data/lesson_rag/huge_file.txt"

with open(huge_path, "r", encoding="utf-8") as f:
    huge_text = f.read()

blocks = huge_text.split("\n\n")

for block in blocks:
    lines = block.strip().split("\n")
    if len(lines) < 2:
        continue

    title = lines[0].strip()
    content = "\n".join(lines[1:]).strip()

    doc = Document(
        page_content=content,
        metadata={
            "file": "huge_file.txt",
            "block": title
        }
    )

    doc_id = str(uuid4())
    docs.append(doc)
    new_ids.append(doc_id)
    ids[f"huge_file.txt::{title}"] = doc_id


vector_store.add_documents(
    documents=docs,
    ids=new_ids
)

with open("ids.json", "w", encoding="utf-8") as f:
    json.dump(ids, f, indent=2, ensure_ascii=False)

print("Database updated")
print("Total documents:", len(docs))
