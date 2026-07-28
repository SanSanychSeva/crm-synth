from collections import OrderedDict

import pandas as pd
from scipy.sparse import lil_matrix


class VocabularyVectorizer:
    """
    Построение BoW-вектора по специализированному словарю.

    Особенность:
    иерархический режим (вариант B):

    Если в тексте есть:

        неисправность оборудования провайдера

    активируются одновременно:

        неисправность
        неисправность оборудования
        неисправность оборудования провайдера

    """

    def __init__(
        self,
        vocabulary_path
    ):

        self.vocabulary_path = vocabulary_path

        self.vocabulary = None

        self.tokens = None

        self.token_ids = None


        self._load_vocabulary()



    def _load_vocabulary(
        self
    ):

        df = pd.read_csv(
            self.vocabulary_path
        )


        # сохраняем порядок token_id

        df = df.sort_values(
            "token_id"
        )


        self.vocabulary = df


        self.tokens = (
            df["text"]
            .astype(str)
            .tolist()
        )


        self.token_ids = (
            df["token_id"]
            .astype(int)
            .tolist()
        )



    def transform(
        self,
        corpus
    ):

        documents = list(corpus)


        n_documents = len(
            documents
        )

        n_tokens = len(
            self.tokens
        )


        X = lil_matrix(
            (
                n_documents,
                n_tokens
            ),
            dtype=float
        )


        for doc_id, text in enumerate(documents):

            self._process_document(
                text,
                X,
                doc_id
            )


        return X.tocsr()



    def _process_document(
        self,
        text,
        matrix,
        doc_id
    ):

        text = str(text).lower()


        for token, token_id in zip(
            self.tokens,
            self.token_ids
        ):

            if token in text:

                matrix[
                    doc_id,
                    token_id
                ] = 1