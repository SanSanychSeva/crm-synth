from collections import Counter, defaultdict
import re


class Statistics:
    """
    Сбор статистики корпуса.

    Содержит:
    - символьные n-граммы
    - слова
    - document frequency
    - контекст слов
    """

    def __init__(
        self,
        min_n=2,
        max_n=8
    ):

        self.min_n = min_n
        self.max_n = max_n

        # character ngrams
        self.ngram_freq = Counter()

        self.ngram_document_freq = Counter()


        # words
        self.word_freq = Counter()

        self.word_document_freq = Counter()

        #phrases
        self.phrase_freq = Counter()


        # contexts
        self.left_context = defaultdict(
            Counter
        )

        self.right_context = defaultdict(
            Counter
        )


    def fit(self, corpus):

        for text in corpus:

            self._process_document(
                text
            )

        return self



    def _process_document(
        self,
        text
    ):

        # ---------- chars ----------

        seen_ngrams = set()

        for ngram in self._ngrams(text):

            self.ngram_freq[ngram] += 1

            seen_ngrams.add(
                ngram
            )


        for ngram in seen_ngrams:

            self.ngram_document_freq[ngram] += 1



        # ---------- words ----------

        words = self._words(
            text
        )


        seen_words = set()


        for index, word in enumerate(words):

            self.word_freq[word] += 1

            seen_words.add(
                word
            )

             # контекст

            if index > 0:

                self.left_context[word][
                    words[index - 1]
                ] += 1


            if index < len(words)-1:

                self.right_context[word][
                    words[index + 1]
                ] += 1


        for word in seen_words:

            self.word_document_freq[word] += 1

        # ---------- phrases ----------
        for n in [2,3]:
            for i in range(len(words)-n+1):
                phrase = " ".join(words[i:i+n])
                self.phrase_freq[phrase] += 1


    def _ngrams(
        self,
        text
    ):

        length = len(text)

        for n in range(
            self.min_n,
            self.max_n + 1
        ):

            for i in range(
                length - n + 1
            ):

                yield text[
                    i:i+n
                ]



    def _words(
        self,
        text
    ):

        return re.findall(
            r"[а-яА-Яa-zA-Z0-9\-]+",
            text.lower()
        )