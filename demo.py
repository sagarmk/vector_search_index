import json
import logging
import os
from parser.document_parser import PdfParser
from parser.indexer import TextIndexer

import faiss
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from parser.utils import configure_logger

log = configure_logger(__name__)

"""
This is a streamlit based application which works as a frontend for building vector search index
"""


def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


st.title("Single PDF Parser and Search")
st.write(
    "Upload one or more PDF files and click the button to parse them and dump the extracted data as JSON. "
    "Then, click the 'Build Index' button to create a Faiss index from the generated JSON files. "
    "Finally, enter a search query and click the 'Search' button to perform a search on the Faiss index."
)

uploaded_files = st.file_uploader(
    "Choose one or more PDF files", type="pdf", accept_multiple_files=True
)

index_name = os.getenv("INDEX_NAME")


if st.button("Parse"):

    if uploaded_files:
        pdf_parser = PdfParser(uploaded_files)
        pdf_parser.parse_pdf()

        output_filename = st.text_input("Output filename", value="output.json")
        if output_filename:
            pdf_parser.write_json(output_filename)
            st.success(f"Content written to {output_filename}")

        if st.button("Show parsed content"):
            st.write(
                {
                    "documents": pdf_parser.document_content,
                    "pages": pdf_parser.page_content,
                }
            )

if st.button("Build Index"):

    json_dir = os.getenv("JSON")
    json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]
    all_data = [
        read_json(os.path.join(json_dir, json_file)) for json_file in json_files
    ]

    all_texts = [doc["text"] for data in all_data for doc in data["documents"]]
    indexer = TextIndexer(all_texts)
    indexer.build_index()

    if indexer:
        indexer.save_index(index_name)
        st.markdown("**:blue[ Faiss index has been built and stored at: tmp.index]**")

if st.sidebar.button("View Index"):
    files_indexer = faiss.read_index(index_name)
    n_vectors = files_indexer.ntotal
    dimensionality = files_indexer.d
    st.sidebar.write(f"Total Vectors: {n_vectors}, Dimensionality: {dimensionality}")


single_index = [f for f in os.listdir(".") if f.endswith(".index")]
selected_index_file = st.selectbox("Select a FAISS Index:", single_index)


if selected_index_file:
    single_index = os.path.join(".", selected_index_file)
    load_faiss_index = TextIndexer()
    st.sidebar.write(selected_index_file)
    st.write(f"Sucessfully loaded index: **{os.path.basename(single_index)}**")
    load_faiss_index.load_index(single_index)

    query = st.text_input("Enter your query:")
    if st.button("Search"):
        res = load_faiss_index.search(query)
        logging.info(f" RESUULTS: {res}")

        for i, result in enumerate(res):
            st.write(f"Result {i+1}: {result}")
            if i < len(res) - 1:
                st.markdown("---")
