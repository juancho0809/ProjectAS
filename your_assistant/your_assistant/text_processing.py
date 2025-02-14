"""
This module has some functionalities regarding text processing.

Author: Juan Diego Lozada - Nicolas Romero
"""

import sys
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.llms import LlamaCpp
from langchain_huggingface import HuggingFaceEmbeddings
import os


def load_pdf_data(path: str) -> str:
    """
    This method takes all PDF files in a directory and loads them into a text string.

    Args:
        path (str): The path to the directory containing the PDF files.

    Returns:
        A text string containing the content of the PDF files.
    """
    loader = PyPDFDirectoryLoader(path)
    return loader.load()


def split_chunks(data: str) -> list:
    """
    This method splits a text string into chunks of 10000 characters
    with an overlap of 20 characters.

    Args:
        data (str): The text string to split into chunks.

    Returns:
        A list of strings containing the chunks.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
    chunks = splitter.split_documents(data)
    print(f"Number of chunks: {len(chunks)}")
    return chunks


def get_embeddings() -> list:
    """
    This method gets semantic embeddings for a list of text chunks.

    Returns:
        A list of embeddings for the text chunks.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def get_chunk_embeddings(chunks: list, embeddings: list) -> list:
    """
    This method gets the embeddings for a list of text chunks.

    Args:
        chunks (list): A list of text chunks.
        embeddings (list): A list of embeddings for the text chunks.

    Returns:
        A list of embeddings for the text chunks.
    """
    return FAISS.from_documents(chunks, embedding=embeddings)


def load_llm():
    """
    This method loads the LLM model, in this case, one of the FOSS Mistral family.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "mistral-7b-instruct-v0.2.Q3_K_M.gguf")
    # Download from: https://Shuggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/blob/main/mistral-7b-instruct-v0.2.Q3_K_M.gguf
    llm = LlamaCpp(
        # The path to the model file
        
        streaming=True,
        model_path=file_path,
        temperature=0.75,
        top_p=1,
        verbose=True,
        n_ctx=4096,
    )
    return llm


def agent_answer(question: str, llm: object, vector_store: object):
    """
    This method gets the answer to a question from the LLM model.

    Args:
        question (str): The question to ask the LLM model.
        llm (object): The LLM model.

    Returns:
        A string with the answer to the question.
    """
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
    )
    return qa.run(question)


def main():
    """This is the infinite loop to make questions to the Anime Assistant."""

    print("Welcome to the Anime Assistant!\n")
    current_dir = os.path.dirname(os.path.realpath(__file__))

# Definir la ruta del archivo en la carpeta pdfs
    pdfs_dir = os.path.join(current_dir, "pdfs")
    llm = load_llm()
    chunks = split_chunks(load_pdf_data(pdfs_dir))
    embeddings = get_embeddings()
    vector_store = get_chunk_embeddings(chunks, embeddings)

    while True:
        user_input = input("Make your question: ")
        if user_input == "exit":
            print("Thanks. Goodbye!")
            sys.exit()
        if user_input == "":
            continue

        result = agent_answer(question=user_input, llm=llm, vector_store=vector_store)
        print(result)


if __name__ == "__main__":
    main()
