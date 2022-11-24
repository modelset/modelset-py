import sys
import unittest

sys.path.append("./src")


class TestW2V(unittest.TestCase):
    def test_load(self):
        from modelset import load_mde_word2vec
        vectors = load_mde_word2vec()
        for word in ['state', 'sql', 'transition',
                     'assignment', 'petri',
                     'father', 'name', 'epsilon',
                     'graph', 'classroom', 'transformation']:
            print(f'Most similar {word}: {vectors.most_similar(positive=[word])}')


if __name__ == '__main__':
    unittest.main()
