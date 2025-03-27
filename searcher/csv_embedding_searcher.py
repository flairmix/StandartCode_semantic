import os
import time
import pickle
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util


class CSVEmbeddingSearcher:
    def __init__(
        self,
        csv_path: str,
        embedding_column: str,
        model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        # model_name: str = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
    ):
        self.csv_path = csv_path
        self.embedding_column = embedding_column
        self.model_name = model_name
        self.cache_path = csv_path.replace(".csv", "_cached.pkl")

        # Загружаем модель отдельно (не кэшируем в pickle)
        start_load = time.time()
        self.model = SentenceTransformer(self.model_name)
        self.model_load_time = time.time() - start_load

        # Пытаемся загрузить кэш
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "rb") as f:
                self.df = pickle.load(f)
        else:
            self.df = pd.read_csv(self.csv_path, sep=";", header=0)

            self._create_embedding_column()

            with open(self.cache_path, "wb") as f:
                pickle.dump(self.df, f)

    def _create_embedding_column(self):
        if self.embedding_column not in self.df.columns:
            raise ValueError(f"Столбец '{self.embedding_column}' не найден в колонках CSV.")

        embeddings_list = []
        start_time = time.time()

        for _, row in self.df.iterrows():
            text_value = str(row[self.embedding_column])
            emb = self.model.encode(text_value, convert_to_numpy=True, normalize_embeddings=True)
            embeddings_list.append(emb)

        self.df["embedding_vector"] = embeddings_list
        self.embedding_build_time = time.time() - start_time

    def search_nearest(self, query: str, top_k: int = 5):
        query_emb = self.model.encode(query, convert_to_tensor=True)
        all_emb = np.vstack(self.df["embedding_vector"].values)
        similarities = util.pytorch_cos_sim(query_emb, all_emb)[0].cpu().numpy()
        sorted_indices = np.argsort(-similarities)
        top_indices = sorted_indices[:top_k]

        results = []
        for idx in top_indices:
            sim_score = float(similarities[idx])
            row_data = self.df.iloc[idx].to_dict()

            results.append({
                "index": idx,
                "similarity": sim_score,
                "Наименование": row_data.get("Наименование"),
                "Подкласс 2": row_data.get("Подкласс 2"),
            })

        return results

    # def get_stats(self):
    #     return {
    #         "model_name": self.model_name,
    #         "model_load_time": self.model_load_time,
    #         "embedding_build_time": getattr(self, "embedding_build_time", None),
    #         "data_shape": self.df.shape
    #     }
