import os

from gensim.models import KeyedVectors

from modelset.downloader import DEFAULT_DIR_MODELSET, WORD2VEC_NAME_KV


def load_mde_word2vec(vectors_file=os.path.join(DEFAULT_DIR_MODELSET, WORD2VEC_NAME_KV)):
    return KeyedVectors.load(vectors_file)
