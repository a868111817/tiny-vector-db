from typing import List
from BCEmbedding import EmbeddingModel


def encode(sentences: List):
    # setting model
    model = EmbeddingModel(model_name_or_path="maidalun1020/bce-embedding-base_v1")

    # extract embeddings
    embeddings = model.encode(sentences)

    return embeddings


if __name__ == "__main__":
    # list of sentences
    sentences = ['sentence_0', 'sentence_1']

    embeddings = encode(sentences)
    print(embeddings)