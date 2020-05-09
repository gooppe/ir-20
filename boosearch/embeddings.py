from typing import Iterable, List, Tuple

import torch
from boosearch.utils import iter_json
from tqdm import tqdm
from transformers import DistilBertModel, DistilBertTokenizer

PRETRAINED_WEIGHTS = "distilbert-base-uncased"


def load_distillbert() -> Tuple[DistilBertTokenizer, DistilBertModel]:
    model = DistilBertModel.from_pretrained(PRETRAINED_WEIGHTS)
    tokenizer = DistilBertTokenizer.from_pretrained(PRETRAINED_WEIGHTS)
    model.eval()

    return tokenizer, model


def export_embeddings_json(filename: str, emb_name: str, target_collumn: int):
    with open(filename, encoding="utf8") as file:
        total = sum(1 for line in file)

    data = iter_json(filename)
    data = (doc[target_collumn] for doc in data)
    data = tqdm(data, desc="Exporting embeddings", total=total)

    export_embeddings(data, emb_name)


@torch.no_grad()
def export_embeddings(docs: Iterable[str], filename: str):
    tokenizer, model = load_distillbert()
    embeddings = []
    for doc in docs:
        encoded_tensor = torch.tensor([tokenizer.encode(doc, max_length=512)])
        (features,) = model(encoded_tensor)
        embedding = features.sum(dim=1)
        embeddings.append(embedding)

    embeddings = torch.cat(embeddings)
    torch.save(embeddings, filename)


@torch.no_grad()
def most_common(
    query: str, doc_indexes: List[int], n: int, emb_dump: str
) -> List[int]:
    tokenizer, model = load_distillbert()
    embeddings = torch.load(emb_dump, map_location="cpu")
    doc_embeddings = embeddings[doc_indexes]

    encoded_tensor = torch.tensor([tokenizer.encode(query, max_length=512)])
    query_embedding = model(encoded_tensor)[0].sum(dim=1)
    simmmilarity = torch.cosine_similarity(query_embedding, doc_embeddings)
    _, top_idxs = torch.topk(
        simmmilarity, k=min(n, len(doc_indexes))
    )
    rescored_doc_indexes = [doc_indexes[i] for i in top_idxs]

    return rescored_doc_indexes
