from copy import deepcopy
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentChunker:
    """
    Splits normalized document records into smaller chunks.

    Input format:

    [
        {
            "text": "document or page text",
            "metadata": {
                "source_file": "sample.pdf",
                "file_type": ".pdf",
                "page_number": 1,
                "section_heading": None
            }
        }
    ]

    output format:

    [
        {
            "text": "smaller chunk text",
            "metadata": {
                "source_file": "sample.pdf",
                "file_type": ".pdf",
                "page_number": 1,
                "section_heading": None,
                "chunk_index": 0,
                "chunking_strategy": "recursive",
                "character_count": 800
            }
        }
    ]

    """
    SUPPORTED_STRATEGIES = {
        "fixed",
        "recursive"
    }

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ):
        """
        Initialize the chunker.

        Args:
            chunk_size:
                Maximum number of characters in one chunk.

            chunk_overlap:
                Number of characters repeated between neighboring chunks.
        """

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def fixed_size_split(self, text: str) -> list[str]:
        """
        Split text into fixed-size character chunks.
        Example:

        chunk_size = 10
        chunk_overlap = 2

        Text:
        abcdefghijklmnop

        Chunks:
        abcdefghij
        ijklmnop

        The characters 'ij' appear in both chunks because of overlap.
        """

        if not text or not text.strip():
            return []

        chunks = []

        start = 0
        text_length = len(text)
        step_size = self.chunk_size - self.chunk_overlap

        while start < text_length:
            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += step_size

        return chunks

    def recursive_split(self, text: str) -> list[str]:
        """
        Split text while trying to preserve natural boundaries.

        It attempts separators in this order:

        1. Paragraph boundary
        2. Line boundary
        3. Sentence-like boundary
        4. Word boundary
        5. Individual characters
        """ 
        if not text or not text.strip():
            return []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
            length_function=len
        )

        chunks = splitter.split_text(text)

        return [
            chunk.strip()
            for chunk in chunks
            if chunk.strip()
        ]

    def split_text(
        self,
        text: str,
        strategy: str
    ) -> list[str]:
        """
        Select and run one chunking strategy.
        """
        strategy = strategy.lower().strip()

        if strategy not in self.SUPPORTED_STRATEGIES:
            raise ValueError(
                f"Unsupported chunking strategy: {strategy}. "
                f"Supported strategies: "
                f"{sorted(self.SUPPORTED_STRATEGIES)}"
            )
        if strategy == "fixed":
            return self.fixed_size_split(text)
        return self.recursive_split(text)

    def chunk_records(
        self,
        records: list[dict[str, Any]],
        strategy: str = "recursive"
    ) -> list[dict[str, Any]]:
        """
        Chunk every record returned by DocumentLoader.

        Metadata from the original record is copied into every chunk.
        """
        chunked_records = []
        global_chunk_index = 0

        for record_index, record in enumerate(records):
            text = record.get("text", "")
            metadata = record.get("metadata", {})

            if not isinstance(text, str):
                raise TypeError(
                    f"Record {record_index} has invalid text. "
                    "Expected a string."
                )

            if not isinstance(metadata, dict):
                raise TypeError(
                    f"Record {record_index} has invalid metadata. "
                    "Expected a dictionary."
                )
            
            text_chunks = self.split_text(
                text=text,
                strategy=strategy
            )

            for page_chunk_index, chunk_text in enumerate(text_chunks):
                chunk_metadata = deepcopy(metadata)
                chunk_metadata.update(
                    {
                        "record_index": record_index,
                        "chunk_index": global_chunk_index,
                        "page_chunk_index": page_chunk_index,
                        "chunking_strategy": strategy,
                        "character_count": len(chunk_text)
                    }
                )
                chunked_records.append(
                    {
                        "text": chunk_text,
                        "metadata": chunk_metadata
                    }
                )
                global_chunk_index += 1
        return chunked_records  

if __name__ == "__main__":
    from document_loader import DocumentLoader

    loader = DocumentLoader()

    records = loader.load_document(
        "data/raw/juthi_bio2.pdf"
       )
    chunker = DocumentChunker(
        chunk_size=800,
        chunk_overlap=150
        )

    chunks = chunker.chunk_records(
        records=records,
        strategy="recursive"
    )
    print(f"Original records: {len(records)}")
    print(f"Created chunks: {len(chunks)}")
    print("=" * 80)

    for chunk in chunks[:5]:
        print("Metadata:")
        print(chunk["metadata"])

        print("\nChunk preview:")
        print(chunk["text"][:300])

        print("-" * 80)