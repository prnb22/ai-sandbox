from pathlib import Path
import re
import fitz 
from bs4 import BeautifulSoup
import markdown
import docx

class DocumentLoader:
    """
    Multi-format document loader for hybrid RAG pipeline

    Supported:
    - PDF
    - TXT
    - Markdown(.md)
    - HTML
    - DOCX
    Output:
    [
    {
        "text": "..",
        "metadata": {
            "source_file": "...",
            "file_type": "...",
            "page_number":"...",
            "section_heading: ""
        }
    }
    ]
    """
    def claen_text(self, text:str) -> str:
        """
        remove extra spaces, line breaks, weired formatting
        """
        text = text.replace("\x00", " ")
        text = re.sub(r"\s+"," ", text)
        return text.strip()
    
    def extract_md_headings(self, text:str):
        headings = []

        for line in text.splitlines():
            line = line.strip()

            if line.startswith("#"):
                heading = line.lstrip("#").strip()

                if heading:
                    headings.append(heading)
    
        return headings
    
    def extract_html_headings(self, soup):
        headings = []

        for tag in soup.find_all(["h1", "h2", "h3"]):
            heading = tag.get_text(strip=True)

            if heading: 
                headings.append(heading)

        return headings
    
    def load_text(self, path:path):

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return [
            {
                "text": self.claen_text(text),

                "metadata": {
                    "source_file": path.name,
                    "file_type": ".txt",
                    "page_number": None,
                    "section_heading": None
                }
            }
        ]
    
    def load_pdf(self, path:Path):

        records = []

        with fitz.open(path) as pdf:

            for page_no, page in enumerate(pdf, start=1):

                text = page.get_text("text")

                text = self.clean_text(text)

                if not text: 
                    continue

                records.append(
                    {
                        "text": text,

                        "metadata": {
                            "source_file": path.name,
                            "file_type": ".pdf",
                            "page_number": page_no,
                            "section_heading": None
                        }
                    }
                )
        return records



