import sys
import unittest

MODELSET_HOME = "modelset"


class DatasetTestCase(unittest.TestCase):
    def test_graph(self):
        sys.path.append("../modelset-py/src")
        import modelset.dataset as ds
        dataset = ds.load(MODELSET_HOME, modeltype='ecore', selected_analysis=['stats'])
        dataset_normalized_df = dataset.to_normalized_df()
        ids = dataset_normalized_df['id']
        g = dataset.as_graph(ids[0])
        print(g)


if __name__ == '__main__':
    unittest.main()
