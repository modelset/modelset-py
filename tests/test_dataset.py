import sys
import unittest

sys.path.append("../modelset-py/src")


class DatasetTestCase(unittest.TestCase):
    def test_graph(self):
        from modelset import load
        dataset = load(modeltype='ecore', selected_analysis=['stats'])
        dataset_normalized_df = dataset.to_normalized_df()
        ids = dataset_normalized_df['id']
        g = dataset.as_graph(ids[0])
        print(g)

    def test_docs(self):
        from modelset import load, Dataset, Model
        print(load.__doc__)
        print(Dataset.__doc__)
        print(Model.__doc__)


if __name__ == '__main__':
    unittest.main()
