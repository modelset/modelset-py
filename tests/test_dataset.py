import sys
import unittest

sys.path.append("./src")
from modelset import load, Dataset, Model

dataset_ecore = load(modeltype='ecore', selected_analysis=['stats'])
dataset_uml = load(modeltype='uml', selected_analysis=['stats'])


class DatasetTestCase(unittest.TestCase):
    """
    Tests of modelset-py. Before running these tests, the ModelSet dataset has to be in your computer i.e.,
    you should have executed 'python -m modelset.downloader' or 'python src/modelset/downloader.py'. Alternatively,
    it is possible to copy the source of the dataset (see subproject modelset-dataset) in ~/.modelset directly.
    """

    def test_graph(self):
        dataset_normalized_df = dataset_ecore.to_normalized_df()
        ids = dataset_normalized_df['id']
        g = dataset_ecore.as_graph(ids[0])
        print(g)

    def test_docs(self):
        print(load.__doc__)
        print(Dataset.__doc__)
        print(Model.__doc__)

    def test_uml(self):
        dataset_normalized_df = dataset_ecore.to_normalized_df()
        print(dataset_normalized_df.describe())

    def test_ecore(self):
        dataset_df = dataset_ecore.to_df()
        dataset_df = dataset_df[dataset_df.tags.notnull()]
        print(dataset_df['tags'])

    def test_duplication(self):
        duplication_ecore = dataset_ecore.get_duplicates()
        print(f'Representatives ecore: {len(duplication_ecore)}')
        duplication_uml = dataset_ecore.get_duplicates()
        print(f'Representatives uml: {len(duplication_uml)}')


if __name__ == '__main__':
    unittest.main()
