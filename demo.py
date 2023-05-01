import re
import json
import PyPDF2
import streamlit as st
from pathlib import Path
import faiss
from src.parse_document import PdfParser
from src.indexer import FaissIndexer


"""
This is a streamlit based application which works as a frontend for building vector search index
"""

# Create a Streamlit app
st.title("PDF Parser and Search")
st.write("Upload one or more PDF files and click the button to parse them and dump the extracted data as JSON. "
         "Then, click the 'Build Index' button to create a Faiss index from the generated JSON files. "
         "Finally, enter a search query and click the 'Search' button to perform a search on the Faiss index.")

# Create a file uploader for multiple files
uploaded_files = st.file_uploader("Choose one or more PDF files", type="pdf", accept_multiple_files=True)

# Create a button to start parsing
if st.button("Parse"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            
            # Create a PdfParser object for each uploaded file
            pdf_parser = PdfParser(uploaded_file)

            # Parse the PDF file
            pdf_parser.parse_pdf()

            # Write the extracted data to a JSON file with the same name as the PDF file
            input_filename = Path(uploaded_file.name)
            output_filename = input_filename.stem + ".json"
            pdf_parser.write_json(output_filename)

            # Display a success message
            st.success(f"Extracted data from {input_filename} has been written to {output_filename}.")
    else:
        # Display an error message if no file was uploaded
        st.error("Please upload one or more PDF files.")

# Create a button to build the Faiss index
if st.button("Build Index"):
    # Define the list of JSON files to index
    json_files = [str(Path(file.name).stem) + '.json' for file in uploaded_files]

    # Create a Faiss indexer object and build the index
    indexer = FaissIndexer(json_files)
    indexer.build_index()

    if indexer:
        indexer.save_index('./tmp.index')
        st.markdown("**:blue[ Faiss index has been built and stored at: tmp.index]**")



# Create a search query input box and search button
query = st.text_input("Enter a search query:")
if st.button("Search"):
    # Search the index using the query
    indexer = FaissIndexer.load_index('./tmp.index')  # Load the index and assign it to the indexer variable

    if indexer:  # Check if index was successfully loaded
        st.markdown('**:blue[Loaded index from: tmp.index]**')
        D, I, search_results = indexer.search_index(query)  # Get distances, indices, and search results

        # Display the search results
        for i, result in enumerate(search_results):
            st.write(f"Result {i+1}: {result}")
            if i < len(search_results) - 1:  # Add a horizontal line if it's not the last result
                   
                    st.markdown("---")
            # Display additional details about the search result if needed
    else:
        st.error("Failed to load index. Please make sure the index has been built.")
