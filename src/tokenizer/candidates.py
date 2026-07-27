from collections import Counter


STOP_WORDS = {

    "причина",
    "по",
    "услуге",
    "есть",
    "проблемы",
    "проблема",

}


class CandidateExtractor:


    def __init__(
        self, 
        normalizer,
        min_freq=20
    ):

        self.min_freq = min_freq
        self.normalizer = normalizer



    def extract(
    self,
    statistics
):

        # ----------------------------------
        # Первый проход:
        # объединяем одинаковые кандидаты
        # ----------------------------------

        aggregated = Counter()

        for phrase, freq in statistics.phrase_freq.items():

            if freq < self.min_freq:
                continue

            phrase = self.normalizer.normalize(
                phrase
            )

            if phrase is None:
                continue

            aggregated[phrase] += freq


        # ----------------------------------
        # Второй проход:
        # вычисляем score
        # ----------------------------------

        candidates = []

        for phrase, freq in aggregated.items():

            words = phrase.split()

            score = (
                freq *
                (len(words) ** 1.5)
            )

            candidates.append(
                (
                    phrase,
                    freq,
                    score
                )
            )


        candidates.sort(
            key=lambda x: x[2],
            reverse=True
        )

        return candidates