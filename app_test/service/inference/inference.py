# service/inference/inference.py
from gensim.models import Word2Vec

class InferenceService:
    def __init__(self):
        self.model = Word2Vec.load('data/models/word2vec_model.bin')

    def predict(self, input_text: str):
        tokens = input_text.split()
        similar_words = self.model.wv.most_similar(tokens, topn=5)
        return similar_words
