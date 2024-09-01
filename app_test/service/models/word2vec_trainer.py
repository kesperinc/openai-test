# service/models/word2vec_trainer.py
from gensim.models import Word2Vec

class Word2VecTrainer:
    def __init__(self, file_list):
        self.file_list = file_list

    def train(self):
        sentences = []
        for file in self.file_list:
            with open(file, 'r', encoding='utf-8') as f:
                sentences += [line.split() for line in f.readlines()]

        model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)
        model.save('data/models/word2vec_model.bin')
