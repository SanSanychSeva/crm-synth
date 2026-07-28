from __future__ import annotations

from dataclasses import dataclass, asdict

import pandas as pd


# ==========================================================
# Vocabulary Entry
# ==========================================================

@dataclass(slots=True)
class VocabularyEntry:

    text: str

    freq: int

    score: float

    parent_count: int = 0

    child_count: int = 0

    redundancy: float = 0.0

    rank: float = 0.0


# ==========================================================
# Vocabulary Builder
# ==========================================================

class VocabularyBuilder:
    """
    Построение итогового словаря.

    На вход получает результат CandidateExtractor:

        [
            (phrase, freq, score),
            ...
        ]

    На выходе возвращает список VocabularyEntry.
    """

    def __init__(
        self,
        redundancy_threshold=0.95,
    ):

        self.redundancy_threshold = redundancy_threshold

    # ------------------------------------------------------

    def build(self, candidates):

        vocabulary = [

            VocabularyEntry(
                text=text,
                freq=freq,
                score=score,
            )

            for text, freq, score in candidates
        ]

        self.analyze_nesting(vocabulary)

        self.analyze_redundancy(vocabulary)

        self.rank_candidates(vocabulary)

        vocabulary.sort(
            key=lambda x: x.rank,
            reverse=True,
        )

        return vocabulary

    # ------------------------------------------------------

    def analyze_nesting(
        self,
        vocabulary,
    ):

        texts = [
            v.text
            for v in vocabulary
        ]

        for v in vocabulary:

            parents = 0
            children = 0

            for other in texts:

                if other == v.text:
                    continue

                if other.startswith(
                    v.text + " "
                ):
                    children += 1

                elif v.text.startswith(
                    other + " "
                ):
                    parents += 1

            v.parent_count = parents
            v.child_count = children

    # ------------------------------------------------------

    def analyze_redundancy(
        self,
        vocabulary,
    ):

        lookup = {
            v.text: v
            for v in vocabulary
        }

        for v in vocabulary:

            words = v.text.split()

            if len(words) == 1:
                continue

            redundancy = 0.0

            for i in range(
                1,
                len(words)
            ):

                parent = " ".join(
                    words[:i]
                )

                if parent not in lookup:
                    continue

                parent_freq = lookup[parent].freq

                if parent_freq == 0:
                    continue

                redundancy = max(
                    redundancy,
                    v.freq / parent_freq,
                )

            v.redundancy = redundancy

    # ------------------------------------------------------

    def rank_candidates(
        self,
        vocabulary,
    ):

        for v in vocabulary:

            child_bonus = (
                1.0 +
                0.05 * v.child_count
            )

            redundancy_penalty = 1.0

            if (
                v.redundancy >
                self.redundancy_threshold
            ):

                redundancy_penalty = 0.8

            v.rank = (
                v.score *
                child_bonus *
                redundancy_penalty
            )

    # ------------------------------------------------------

    def to_dataframe(
        self,
        vocabulary,
    ):

        return pd.DataFrame(

            [
                asdict(v)
                for v in vocabulary
            ]

        )[
            [
                "text",
                "freq",
                "score",
                "parent_count",
                "child_count",
                "redundancy",
                "rank",
            ]
        ]