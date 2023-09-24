import json
import logging
import os
import re

import fitz
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(level=logging.DEBUG)


class PdfParser:
    def __init__(self, uploaded_files):
        self.uploaded_files = uploaded_files
        self.document_content = []
        self.page_content = []

    def parse_pdf(self):
        for uploaded_file in self.uploaded_files:
            filename = uploaded_file.name
            file_contents = uploaded_file.getvalue()

            try:
                logging.debug(f"Parsing {filename}")
                pdf_document = fitz.open(stream=file_contents, filetype="pdf")
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    text = page.get_text()
                    paragraphs = re.split("\n\n", text)
                    for paragraph in paragraphs:
                        paragraph = paragraph.strip()
                        if not paragraph:
                            continue
                        if re.match("^\d+\.\d+\.\d+", paragraph):
                            self.page_content.append(
                                {"header": paragraph, "file": filename}
                            )
                        elif re.match("^\d+\.\d+", paragraph):
                            self.page_content.append(
                                {"header": paragraph, "file": filename}
                            )
                        else:
                            self.document_content.append(
                                {"text": paragraph, "file": filename}
                            )
                logging.debug(
                    f"Extracted text length for {filename}: {[f for f in self.document_content]}"
                )
            except (fitz.PyMuPDFError, ValueError) as e:
                logging.error(f"Failed to open or parse {filename}: {e}")
                raise ValueError(f"Failed to open or parse {filename}: {e}")

    def write_json(self, output_filename):
        json_dir = os.getenv("JSON")
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        data = {
            "documents": self.document_content,
            "pages": self.page_content,
        }
        output_filename = os.path.join(json_dir, output_filename)
        with open(output_filename, "w") as outfile:
            json.dump(data, outfile)
