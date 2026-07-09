import os
import json


def save_metadata(chunks, document_hash):

    folder = "backend/storage/metadata"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(
        folder,
        f"{document_hash}.json"
    )

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=4
        )

def load_metadata(document_hash):

    path = os.path.join(
        "backend",
        "storage",
        "metadata",
        f"{document_hash}.json"
    )

    with open(path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    return chunks