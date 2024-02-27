import sqlite3
import array


from typing import List
from embedding import encode


def create_sqlite_talbe(db: str = "embed.db", table: str = "VectorTable") -> None:
    """_summary_

    Args:
        db (str, optional): _description_. Defaults to "embed.db".
        table (str, optional): _description_. Defaults to "VectorTable".
    """
    # 建立資料庫連接
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # 創建表格
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table} (
        id INTEGER PRIMARY KEY,
        Document TEXT,
        Embedding BLOB
    )
    ''')

    conn.commit()
    conn.close()


def insert_sqlite_database(document: str, embedding: List[float], db: str = "embed.db", table: str = "VectorTable"):
    """_summary_

    Args:
        document (str): _description_
        embedding (List[float]): _description_
        db (str, optional): _description_. Defaults to "embed.db".
        table (str, optional): _description_. Defaults to "VectorTable".
    """
    # 建立資料庫連接
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # 將浮點數列表轉換為二進位數據
    blob_data = array.array('f', embedding).tobytes()

    # 插入數據
    cursor.execute('INSERT INTO VectorTable (Document, Embedding) VALUES (?,?)', (document,blob_data,))

    conn.commit()
    conn.close()


def read_all_sqlite_database(db: str = "embed.db", table: str = "VectorTable") -> dict:
    """_summary_

    Args:
        db (str, optional): _description_. Defaults to "embed.db".
        table (str, optional): _description_. Defaults to "VectorTable".

    Returns:
        dict: _description_
    """
    # 建立資料庫連接
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # 從資料庫讀取所有記錄
    cursor.execute('SELECT id, Document ,Embedding FROM VectorTable')

    # 獲取所有結果
    all_records = cursor.fetchall()

    # 初始化一個字典來儲存嵌入向量
    result = {}

    # 轉換每個用戶的嵌入向量
    for record in all_records:
        id, doc, blob_data = record

        # 將BLOB數據轉換回浮點數列表
        embedding = array.array('f')
        embedding.frombytes(blob_data)

        result[doc] = embedding.tolist()

    # # 顯示結果
    # for doc, embedding in result.items():
    #     print(f'Document: {doc}, Embedding: {embedding}')

    # 關閉連接
    conn.close()

    return result


def list_to_dict(documents: List[str], embeddings: List[List[float]]):
    result = {}

    for i in range(len(documents)):
        result[documents[i]] = embeddings[i]

    return result


def create_reverse_mapping(dictionary):
    reverse_mapping = {}
    for key, value in dictionary.items():
        value_tuple = tuple(value)  # 將列表轉換為元組
        if value_tuple not in reverse_mapping:
            reverse_mapping[value_tuple] = key
        # 如果值重複，則將對應的鍵存為列表
        else:
            if not isinstance(reverse_mapping[value_tuple], list):
                reverse_mapping[value_tuple] = [reverse_mapping[value_tuple]]
            reverse_mapping[value_tuple].append(key)
    return reverse_mapping


if __name__ == "__main__":
    pass