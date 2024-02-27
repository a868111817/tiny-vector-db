# Tiny Vector Database

Tiny Vector Database is a lightweight, efficient vector database designed for the processing and retrieval of vector data. With its straightforward API, you can easily integrate and use it within your applications.

## How to Use?

### Installation

There are several ways to install Tiny Vector Database:

#### Pip Installation

First, you can install dependencies using pip:

```bash
pip install -r requirements.txt
```

#### Poetry Installation

Alternatively, if you prefer poetry, you can use it to install:

```bash
poetry install
```

### Quick Start

Logging in to Hugging Face CLI
To use BCEmbedding, first log in to the Hugging Face CLI:

```bash!
huggingface-cli login
```

Then, enter your Hugging Face token when prompted.

Here's how you can incorporate the new sections on ingesting news data and searching query sentences into your README, presented in a clear and structured manner:

### Ingesting News Data into the Database

To ingest news data from a specified URL into the database, use the following command:

```bash
python .\tiny_vector_db\ingest.py --url "https://www.ithome.com.tw/latest" --amount 30
```

Parameters:
- `url`: The URL from which to scrape news.
    - Default: "https://www.ithome.com.tw/latest"
- `amount`: The number of news articles to ingest.
    - Default: 30

### Searching Query Sentences

To search for sentences within your ingested news data, use the command below:

```bash
python .\tiny_vector_db\search.py --query_sentence "Google Gemini Nano模型將可執行於聯發科晶片組，首支援中階手機" --limit 3 --search_method "brute_force"
```

Parameters:
- `query_sentence`: The sentence you want to query.
- `limit`: The maximum number of similar documents to return.
- `search_method`: The algorithm used for computing the search.
    - Default: 'brute_force'
    - Options:
        - `advanced`: Uses Nearest Neighbors in sklearn to boost search efficiency.
        - `brute_force`: A straightforward method that compares the query with all documents.

Expected Output:

```plaintext
search time: 0.1376481056213379s
Query sentence: Google Gemini Nano模型將可執行於聯發科晶片組，首支援中階手機
- The similarity score: 0.9999999999998153, Document: Google Gemini Nano模型將可執行於聯發科晶片組，首支援中階手機
- The similarity score: 0.7072117607759829, Document: 企業用Gemini Pro模型API上架，Google更要打造從端到雲全套GAI工具鏈
- The similarity score: 0.6845499050457537, Document: Google公布開源AI模型Gemma，支援多種框架、可跑在筆電上
```

## Analysis: Comparing Search Methods

In our analysis, we utilized a dataset comprising 1,000 entries to evaluate the performance difference between two search methods: the advanced method and the brute force method. Our goal was to identify which method provides a faster search time under the same conditions.

The evaluation was based on the average time taken over five trials, along with the standard deviation to measure consistency and variability in the results.

### Performance Results

The table below summarizes the search times (in seconds) for both methods, highlighting the efficiency of each:

| Method       | Average Time (s) | Standard Deviation |
|--------------|------------------|--------------------|
| Advanced     | 0.069            | 0.0672             |
| Brute Force  | 0.1444           | 0.0067             |

### Observations

From the data, it's evident that the **Advanced** method significantly outperforms the **Brute Force** method in terms of search speed, demonstrating nearly twice as fast performance. Additionally, the advanced method shows a higher variance in search time, suggesting that its performance might be influenced by the nature of the data or the query specifics. In contrast, the brute force method exhibits a lower standard deviation, indicating more consistent but slower performance across different queries.


## Discussion

### 當我們的使用情境不止需要 parse 30 篇文章時，要如何快速的 scale up 整個 parsing process？

要快速擴展整個 parsing 過程，首先可以考慮使用並行處理技術。透過將大量文章分配到不同的處理單元（如multi-thread、multi-process或分散式系統）上進行同時處理，可以降低整體處理時間。

### 當我們的 DB 當中有上千萬上億筆 documents 時，要如何更近一步提升 vector database 的搜索效率？

對於包含大量文件的向量資料庫，提升搜索效率可以從以下幾個方面著手：

1. Indexing: 使用有效率的index結構，如KD tree等，可以在多維空間中更快地進行近似最近鄰搜索。
2. 量化技術：通過向量量化技術，將高維向量壓縮成較低維的表達，降低計算複雜度並提高搜索速度。
3. Caching：對於頻繁查詢的向量，可以使用cache技術來存儲近期的搜索結果，減少重複計算的需要。

---
