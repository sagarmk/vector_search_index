import re
import json
import fitz

class PdfParser:
    def __init__(self, uploaded_file):
        self.filename = uploaded_file.name
        self.file_contents = uploaded_file.getvalue()
        self.document_content = []
        self.page_content = []

    def parse_pdf(self):
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
        data = {"document_content": " ".join(self.document_content), "page_content": self.page_content}
        with open(output_filename, 'w') as outfile:
            json.dump(data, outfile)
