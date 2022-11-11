import sys
import unittest

sys.path.append("./src")


class DatasetTestCase(unittest.TestCase):
    """
    Tests of modelset-py. Before running these tests, the ModelSet dataset has to be in your computer i.e.,
    you should have executed 'python -m modelset.downloader' or 'python src/modelset/downloader.py'. Alternatively, it is possible to copy the source of the dataset (see sub-project modelset-dataset) in ~/.modelset directly.
    """
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

    def test_uml(self):
        from modelset import load
        dataset = load(modeltype='uml', selected_analysis=['stats'])
        dataset_normalized_df = dataset.to_normalized_df()
        print(dataset_normalized_df.describe())

    def test_ecore(self):
        from modelset import load
        dataset = load(modeltype='ecore', selected_analysis=['stats'])
        dataset_df = dataset.to_df()
        dataset_df = dataset_df[dataset_df.tags.notnull()]
        print(dataset_df['tags'])


if __name__ == '__main__':
    unittest.main()
