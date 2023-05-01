import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
import re
import os

class FaissIndexer:
    """
    A class to create, search and save/load a FAISS index for text search using Sentence Transformers.
    """

    def __init__(self, uploaded_files):
        """
        Initialize FaissIndexer class with a list of uploaded files.

        :param uploaded_files: List of file objects to be indexed
        """
        self.uploaded_files = uploaded_files
        self.model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v1')
        self.index = None
        self.paragraphs = []  # Change this line to store paragraphs instead of documents

    def build_index(self):
        """
        Builds the FAISS index using the uploaded files.
        """
        for uploaded_file in self.uploaded_files:
            input_filename = Path(uploaded_file.name)
            output_filename = input_filename.stem + ".json"
            with open(output_filename, 'r') as infile:
                data = json.load(infile)
                document_text = data["document_content"]
                paragraphs = re.split(r'\n\n|\.\s+(?=\S)', document_text)  # Split document into paragraphs
                self.paragraphs.extend(paragraphs)  # Add the paragraphs to self.paragraphs

        embeddings = self.model.encode(self.paragraphs)
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(np.array(embeddings).astype('float32'))

    def search_index(self, query_text, k=5):
        """
        Searches the FAISS index for the most similar paragraphs to the query_text.

        :param query_text: The query text to search for in the index
        :param k: The number of top results to return (default: 5)
        :return: A tuple containing distances and the matching paragraphs
        """
        query_embedding = self.model.encode([query_text])[0]
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), k)
        search_results = [self.paragraphs[i] for i in I[0]]  # Retrieve paragraph texts based on indices
        return D, search_results

    def save_index(self, index_name):
        """
        Saves the FAISS index and the associated paragraphs to files.

        :param index_name: The name of the index to be saved
        """
        index_filename = f"{index_name}.index"
        faiss.write_index(self.index, index_filename)
        with open(f"{index_name}_paragraphs.json", 'w') as outfile:
            json.dump(self.paragraphs, outfile)

    @classmethod
    def load_index(cls, index_name):
        """
        Loads a FAISS index and the associated paragraphs from files.

        :param index_name: The name of the index to be loaded
        :return: An instance of FaissIndexer class with the loaded index
        """
        index_filename = f"{index_name}.index"
        index = faiss.read_index(index_filename)
        with open(f"{index_name}_paragraphs.json", 'r') as infile:
            paragraphs = json.load(infile)
        indexer = cls(None)
        indexer.index = index
        indexer.paragraphs = paragraphs
        return indexer
