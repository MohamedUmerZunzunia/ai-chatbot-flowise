from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=30,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    documents = []

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "page": page["page"]
                    }
                )
            )

    return documents