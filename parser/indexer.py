import json
import logging
import os

import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()


logging.basicConfig(level=logging.DEBUG)


class TextIndexer:
    def __init__(self, data=None, model_name="paraphrase-mpnet-base-v2"):

        self.data = data
        self.encoder = SentenceTransformer(model_name)
        self.model_name = model_name

    def generate_encodings(self, text_list):
        if not text_list:
            logging.warning("The text list is empty.")
            return np.array([])
        vectors = self.encoder.encode(text_list)
        return vectors

    def build_index(self):

        vectors = self.generate_encodings(self.data)
        vector_dimension = vectors.shape[1]
        self.index = faiss.IndexFlatL2(vector_dimension)
        faiss.normalize_L2(vectors)
        self.index.add(vectors)

    def save_index(self, file_path):
        faiss.write_index(self.index, file_path)
        # Also save the original text data
        data_file_path = os.path.join(file_path + "_paragraphs.json")
        with open(data_file_path, "w") as f:
            json.dump(self.data, f)

    def load_index(self, file_path):
        self.index = faiss.read_index(file_path)
        # Load the original text data
        data_file_path = file_path + "_paragraphs.json"
        if os.path.exists(data_file_path):
            with open(data_file_path, "r") as f:
                self.data = json.load(f)
        else:
            print(f"No data file found at {data_file_path}. Cannot query by text.")

    def search(self, search_text, top_k=2):
        search_vector = self.generate_encodings([search_text])
        faiss.normalize_L2(search_vector)
        k = self.index.ntotal if top_k is None else top_k
        distances, indices = self.index.search(search_vector, k)
        # Ensure indices are within bounds
        assert all(
            0 <= i < len(self.data) for i in indices[0]
        ), f"Invalid indices: {indices}"
        # Return the text corresponding to the indices
        return [self.data[i] for i in indices[0]]
