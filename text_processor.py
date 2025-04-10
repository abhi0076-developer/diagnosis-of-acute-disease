import chromadb
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
import json

loader = DirectoryLoader('datasets/', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
documents = loader.load()
print("Documents Loaded")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
texts = text_splitter.split_documents(documents)

embeddings = SentenceTransformerEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
print("Embedder Loaded")

store = Chroma.from_documents(texts, embeddings, collection_name="vector_db")
print("Vector DB created")

prompt_template = PromptTemplate(
    template="""Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    You are a medical assistant chatbot designed to identify diseases based on symptoms. Follow these rules:

    Based on the user's query, provide the name of the disease if it's clear.

    If the disease is not critical, provide simple diagnostic steps or next actions.
        """,
    input_variables=["context", "question"],
)

#If unsure of the disease or if symptoms suggest a critical condition, respond with:
#"I recommend consulting a doctor for an accurate diagnosis and appropriate treatment."
llm = OpenAI(temperature=0.3, api_key="") # Enter your API Key here of OpenAI
print("LLM Loaded")

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=store.as_retriever(),
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template},
    verbose=True
)

shared_file_path = "shared_data/shared_data.json"

with open(shared_file_path, "r") as f:
    shared_data = json.load(f)

print("Data received from app1:", shared_data)

query = shared_data.get("translated_text")
response = chain(query)
print("\nAnswer:")
print(response['result'])

data_to_share = {"response":response['result']}
with open(shared_file_path, "w") as f:
    json.dump(data_to_share,f)
print("Data written to ",shared_file_path)
