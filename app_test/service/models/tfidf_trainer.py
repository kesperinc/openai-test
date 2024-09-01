# service/models/tfidf_trainer.py

from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDFTrainer:
    def __init__(self, text_processor):
        self.text_processor = text_processor
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

    def train(self):
        # TF-IDF training logic
        pass

    def find_similar_words(self, word, top_n=10):
        # Find similar words logic
        pass

