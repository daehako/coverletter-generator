import os
import glob
from chromadb import PersistentClient

async def ingest_data(directory, collection_name, chromadb_path):
    chroma_client = PersistentClient(path=chromadb_path)

    collection = chroma_client.create_collection(name=collection_name)

    # Enumerate files in the given directory and ingest each file as a single document
    for i, filename in enumerate(glob.glob(f"{directory}/**/*.txt", recursive=True)):
        print("Ingesting:", i, os.path.basename(filename))
        documents = []
        metadatas = []
        ids = []

        with open(filename, "r", encoding='utf-8') as f:
            data = f.read()
            documents.append(data)
            metadatas.append({"source": filename})
            ids.append(f"doc_{i}")
            

        collection.add(documents=documents, metadatas=metadatas, ids=ids)
if __name__ == "__main__":
    directory = 'cover_letter_docs'
    collection_name = 'cover_letter_guidelines'
    chromadb_path = 'chroma.db'

    import asyncio
    asyncio.run(ingest_data(directory, collection_name, chromadb_path))
