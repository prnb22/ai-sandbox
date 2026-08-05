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
    def clean_text(self, text:str) -> str:
        """
        Remove null characters, extra spaces, line breaks,
        and unnecessary formatting.
        """
        text = text.replace("\x00", " ")
        text = re.sub(r"\s+"," ", text)
        return text.strip()
    
    def extract_md_headings(self, text:str)->list[str]:
        """
        Extract Markdown headings beginning with #, ##, or ###.
        """

        headings = []

        for line in text.splitlines():
            line = line.strip()

            if line.startswith("#"):
                heading = line.lstrip("#").strip()

                if heading:
                    headings.append(heading)
    
        return headings
    
    def extract_html_headings(self, soup: BeautifulSoup) -> list[str]:
        """
        Extract h1, h2, and h3 headings from HTML.
        """
        headings = []

        for tag in soup.find_all(["h1", "h2", "h3"]):
            heading = tag.get_text(strip=True)

            if heading: 
                headings.append(heading)

        return headings
    
    def load_txt(self, path:Path)-> list[dict]:
        """
        Load a plain text file.
        """

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        return [
            {
                "text": self.clean_text(text),

                "metadata": {
                    "source_file": path.name,
                    "file_type": ".txt",
                    "page_number": None,
                    "section_heading": None
                }
            }
        ]
    
    def load_pdf(self, path:Path) -> list[dict]:
        """
        Load a PDF page by page.
         Each PDF page becomes a separate record so that page
        numbers can later be used for citations.

        """

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
                            "source_path": str(path),
                            "file_type": ".pdf",
                            "page_number": page_no,
                            "section_heading": None
                        }
                    }
                )
        return records
    
    def load_markdown(self, path: Path) -> list[dict]:
        """
         Load a Markdown file and remove Markdown formatting.
        """

        md_text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        headings= self.extract_md_headings(md_text)

        html = markdown.markdown(md_text)

        soup= BeautifulSoup(html, "html.parser")
        text=soup.get_text(separator="\n")

        return [
            {
                "text": self.clean_text(text),

                "metadata": {
                    "source_file": path.name,
                    "file_type": ".md",
                    "page_number": None,
                    "section_heading": headings[0] if headings else None,
                    "all_headings": headings
                }
            }
        ]
    def load_html(self, path: Path) -> list[dict]:
        """
        Load an HTML file and remove HTML tags that are
        usually not useful for retrieval.
        """

        html = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(html, "html.parser")

        # Remove content that is normally not useful.
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        headings = self.extract_html_headings(soup)

        text = soup.get_text(separator="\n")

        return [
            {
                "text": self.clean_text(text),

                "metadata": {
                    "source_file": path.name,
                    "file_type": ".html",
                    "page_number": None,
                    "section_heading": headings[0] if headings else None,
                    "all_headings": headings
                }
            }
        ]
    

    def load_docx(self, path: Path) -> list[dict]:
        """
        Load paragraphs from a DOCX file.
        """
        document = docx.Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:
            clean_paragraph = self.clean_text(
                paragraph.text
            )

            if clean_paragraph:
                paragraphs.append(clean_paragraph)

        text = "\n".join(paragraphs)

        return [
            {
                "text": self.clean_text(text),
                "metadata": {
                    "source_file": path.name,
                    "file_type": ".docx",
                    "page_number": None,
                    "section_heading": None
                }
            }
        ]
    
    def load_document(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found:{file_path}")
        
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self.load_pdf(path)
        
        elif suffix == ".txt":
            return self.load_txt(path)
        
        elif suffix == ".md":
            return self.load_markdown(path)
        
        elif suffix == ".html":
            return self.load_html(path)

        else:
            raise ValueError(f"Unsupported file type: {suffix}")
        
# ===================================
# Testing
# ===================================
if __name__ == "__main__":

    loader = DocumentLoader()

    file_path = "data/raw/Sprint_2_complete.pdf"

    try:
        records = loader.load_document(file_path)

        print(f"Loaded records: {len(records)}")
        print("=" * 80)

        for record in records:
            print("Metadata:")
            print(record["metadata"])

            print("\nExtracted text preview:")
            print(record["text"][:300])

            print("-" * 80)

    except (
        FileNotFoundError,
        ValueError,
        fitz.FileDataError
    ) as error:
        print(f"Error: {error}")


    records = loader.load_document(file_path)


