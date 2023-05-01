import re
import json
import fitz

class PdfParser:
    """
    A class to parse a PDF file and extract its content.

    Attributes
    ----------
    filename : str
        The name of the uploaded file.
    file_contents : bytes
        The contents of the uploaded file.
    document_content : list
        A list to store the content of the document.
    page_content : list
        A list to store the content of the pages.

    Methods
    -------
    parse_pdf():
        Parse the PDF file and extract its content.
    write_json(output_filename: str):
        Write the extracted content to a JSON file.
    """

    def __init__(self, uploaded_file):
        """
        Initializes the PdfParser object with the uploaded file.

        Parameters
        ----------
        uploaded_file : object
            The uploaded file object containing the name and content.
        """
        self.filename = uploaded_file.name
        self.file_contents = uploaded_file.getvalue()
        self.document_content = []
        self.page_content = []

    def parse_pdf(self):
        """
        Parse the PDF file and extract its content using the PyMuPDF (fitz) library.
        Extracts headers and paragraphs and appends them to the respective lists.
        """
        pdf_document = fitz.open(stream=self.file_contents, filetype="pdf")
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            paragraphs = re.split('\n\n', text)
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                if re.match('^\d+\.\d+\.\d+', paragraph):
                    self.page_content.append({"header": paragraph})
                elif re.match('^\d+\.\d+', paragraph):
                    self.page_content.append({"header": paragraph})
                else:
                    self.document_content.append(paragraph)

    def write_json(self, output_filename):
        """
        Write the extracted content to a JSON file.

        Parameters
        ----------
        output_filename : str
            The name of the output JSON file.
        """
        data = {"document_content": " ".join(self.document_content), "page_content": self.page_content}
        with open(output_filename, 'w') as outfile:
            json.dump(data, outfile)
