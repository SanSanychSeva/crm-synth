class Corpus:

    def __init__(self, texts):
        self.documents = list(texts)

    def __len__(self):
        return len(self.documents)

    def __iter__(self):
        return iter(self.documents)

    def get(self, index):
        return self.documents[index]