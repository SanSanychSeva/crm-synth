class Corpus:

    def __init__(self, texts):
        self.texts = list(texts)

    def __len__(self):
        return len(self.texts)

    def __iter__(self):
        return iter(self.texts)