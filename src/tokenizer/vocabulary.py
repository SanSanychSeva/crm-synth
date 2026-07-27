class Vocabulary:

    def __init__(self):
        self.tokens = set()

    def add(self, token):
        self.tokens.add(token)

    def remove(self, token):
        self.tokens.discard(token)

    def __contains__(self, token):
        return token in self.tokens

    def __len__(self):
        return len(self.tokens)