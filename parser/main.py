import os
from parser.indexer import FaissIndexer
from parser.parse_document import PdfParser
from pathlib import Path

import streamlit as st

# Set the title and the instructions for the Streamlit app
st.title("Vector Document Search")
st.write(
    "Upload one or more PDF files and click the button to parse them and dump the extracted data as JSON. "
    "You can also build a FAISS index with the parsed JSON files and perform searches."
)

with st.sidebar:
    # Display the build index header and create a file uploader
    st.header("Build Index")
    uploaded_files = st.file_uploader(
        "Choose one or more PDF files", type="pdf", accept_multiple_files=True
    )

    # Initialize the indexer in the session state if not already present
    if "indexer" not in st.session_state:
        st.session_state.indexer = None

    # Provide a text input for the index name
    index_name = st.text_input("Enter a name for the new index:")

    # Build and save the index when the button is clicked
    if st.button("Build and Save Index"):
        if uploaded_files:
            if index_name:
                # Parse PDFs and write the output as JSON
                for uploaded_file in uploaded_files:
                    pdf_parser = PdfParser(uploaded_file)
                    pdf_parser.parse_pdf()
                    input_filename = Path(uploaded_file.name)
                    output_filename = input_filename.stem + ".json"
                    pdf_parser.write_json(output_filename)
                    st.success(
                        f"Extracted data from {input_filename} has been written to {output_filename}."
                    )

                # Build and save the FAISS index
                st.session_state.indexer = FaissIndexer(uploaded_files)
                st.session_state.indexer.build_index()
                st.session_state.indexer.save_index(index_name)
                st.success(f"Index has been built and saved as {index_name}.")
            else:
                st.error("Please enter a name for the index.")
        else:
            st.error("Please upload one or more PDF files.")

# Function to get existing FAISS indexes
def get_existing_indexes():
    """
    Get a list of existing FAISS indexes.

    Returns:
        list: A list of filenames of existing FAISS indexes, excluding the file extension.
    """
    return [filename[:-6] for filename in os.listdir() if filename.endswith(".index")]


# Retrieve existing indexes and display them in a dropdown menu
existing_indexes = get_existing_indexes()
selected_index = st.selectbox("Select an existing index:", existing_indexes)

# Load the selected index when the button is clicked
if st.button("Load Index"):
    st.session_state.indexer = FaissIndexer.load_index(selected_index)
    st.success(f"Index '{selected_index}' has been loaded.")

# Provide a text input for the query text
query_text = st.text_input("Enter a query text to search in the FAISS index")

# Perform the search when the button is clicked
if st.button("Search"):
    if query_text and st.session_state.indexer:
        D, search_results = st.session_state.indexer.search_index(query_text)
        st.write("Search results:")

        # Display the search results
        for i, result in enumerate(search_results):
            if len(result) > 50:
                st.write(result)
                if (
                    i < len(search_results) - 1
                ):  # Add a horizontal line if it's not the last result
                    st.markdown("---")
    else:
        if not query_text:
            st.error("Please enter a query text to search.")
        if not st.session_state.indexer:
            st.error("Please load an index before searching.")
