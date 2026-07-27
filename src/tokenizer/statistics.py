class TokenStatistics:

    def __init__(self):

        self.freq = Counter()

        self.doc_freq = Counter()

        self.left = defaultdict(Counter)

        self.right = defaultdict(Counter)