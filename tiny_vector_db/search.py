import argparse
import time
import numpy as np

from typing import List, Tuple
from embedding import encode
from utils import insert_sqlite_database, read_all_sqlite_database, list_to_dict, create_reverse_mapping
from scraper import get_articles
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


def insert(document_info_list: dict):
    """
    Insert a list of document information into the vector database.

    Args:
        document_info_list (dict): A dictionary containing document information.
            Each dictionary should have two keys:
            - 'document': a string representing the document content.
            - 'embedding': a list of floats representing the embedding (float vector) of the document.
    Returns:
        None
    """
    for key in document_info_list:
        embed = document_info_list[key]

        insert_sqlite_database(key, embed)


def search(query_embedding_list: List[list], limit: int, search_method: str) -> List[List[Tuple[float, str]]]:
    """
    Search for similar documents based on the provided query embedding list from a vector database
    and return a limited number of results.

    Args:
        query_embedding_list (List[list]): A list of lists containing query embedding vectors.
            Each inner list represents the embedding (float vector) of a query document.
        limit (int): The maximum number of similar documents to return.
        search_method: {'advanced', 'brute_force'}, default='brute_force'
            Algorithm used to compute.

    Returns:
        List[List[Tuple[float, str]]]: : A list of lists of tuples containing the similarity score
            and the corresponding document found in the database. Each inner list represents
            the results for a single query embedding list. Each tuple contains:
            - The similarity score (float).
            - The document (str).
    """
    # data: dict[Document, Embedding]
    data = read_all_sqlite_database()

    result = []

    # Nearest Neighbors
    if search_method == "advanced":
        # 開始測量
        start = time.time()

        reverse_data = create_reverse_mapping(data)

        embeddings = [embed for embed in data.values()]
        embeddings = np.array(embeddings)

        # 初始化Nearest Neighbors模型
        nbrs = NearestNeighbors(n_neighbors=limit, algorithm='auto', metric='cosine').fit(embeddings)

        # 使用模型找到最近的幾個embedding
        distances, indices = nbrs.kneighbors(np.array(query_embedding_list))

        # # 最近的幾個embedding以及它們的距離
        # print("最近的幾個embedding索引:", indices)
        # print("對應的距離:", distances)

        # 輸出最近的幾個embedding以及對應的鍵
        for q_idx in range(len(indices)):
            inner_list = []
            for i, idx in enumerate(indices[q_idx]):
                closest_embedding = embeddings[idx]
                # print(f"最近的第 {i+1} 個embedding:", closest_embedding)

                # 從反向映射中查找對應的鍵
                corresponding_key = reverse_data.get(tuple(closest_embedding))

                # 輸出距離（限制小數點後兩位）
                distance = float(distances[q_idx][i])
                # print("距離:", f"{1 - distance:.4f}")

                cos = 1 - distance

                inner_list.append((cos, corresponding_key))

            result.append(inner_list)

        # 結束測量
        end = time.time()

    # brute force
    elif search_method == "brute_force":

        # 開始測量
        start = time.time()
        
        for query_embedding in query_embedding_list:
            inner_list = []
            for doc, embed in data.items():
                cos = cosine_similarity([query_embedding], [embed])[0][0]
                inner_list.append((cos, doc))

            inner_list = sorted(inner_list, reverse=True, key= lambda tup: tup[0])
            inner_list = inner_list[:limit]

            result.append(inner_list)

        # 結束測量
        end = time.time()

    # 輸出結果
    print(f"search time: {end - start}s")

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--query_sentence", type=str, help="query sentence for vector database")
    parser.add_argument("--limit", type=int, help="The maximum number of similar documents to return.")
    parser.add_argument("--search_method", type=str, default="brute_force", help="The maximum number of similar documents to return.")

    args = parser.parse_args()

    # search
    querys = [args.query_sentence]
    querys_embed = encode(querys)

    results = search(querys_embed, args.limit, args.search_method)

    for results in zip(querys, results):
        print(f"Query sentence: {results[0]}")
        for pair in results[1]:
            print(f"- The similarity score: {pair[0]}, Document: {pair[1]}")





