"""
This module exports the function in charge of loading Word2Vec4MDE word embeddings. This word embeddings needs to be loaded with gensim and can be used to enhance ML models. 
"""
import os

from gensim.models import KeyedVectors

from modelset.downloader import DEFAULT_DIR_MODELSET, WORD2VEC_NAME_KV


def load_mde_word2vec(vectors_file=os.path.join(DEFAULT_DIR_MODELSET, WORD2VEC_NAME_KV)):
    return KeyedVectors.load(vectors_file)
