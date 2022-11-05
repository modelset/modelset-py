import json
import os
import sqlite3
from collections import defaultdict

import pandas as pd
from networkx.readwrite import json_graph

from modelset.downloader import DEFAULT_DIR_MODELSET


class Dataset:
    """
    Class that represents ModelSet dataset.
    """
    def __init__(self, root_folder, db_filename, dataset_name, modeltype, analysis):
        self.root_folder = root_folder
        self.db_filename = db_filename
        self.modeltype = modeltype

        self.repo_folder = root_folder + '/raw-data/' + dataset_name
        self.txt_files = root_folder + '/txt/' + dataset_name
        self.graph_files = root_folder + '/graph/' + dataset_name

        self.models = []
        self.selected_analysis = analysis.copy()

    def add_model(self, model):
        """Add a model to the dataset object

        Parameters
        ----------
        model : Model
            Model object that you want to add to the dataset
        """
        self.models.append(model)

    def to_df(self):
        """Dumps the dataset object to a pandas dataframe

        Returns
        -------
        DataFrame
            a pandas dataframe
        """
        columns = ['category', 'tags', 'language']
        dic_colums = {}
        # This is intentionally the first column so that the dataframe has id as first column,
        # and we are relying on this order (beware that it might change across implementations)
        dic_colums['id'] = {}
        for c in columns:
            dic_colums[c] = {}
        for i, m in enumerate(self.models):
            for c in m.metadata.keys():
                if c in columns:
                    dic_colums[c][str(i)] = '|'.join(m.metadata[c])
            dic_colums['id'][str(i)] = m.id
            if 'language' not in m.metadata.keys():
                dic_colums['language'][str(i)] = 'english'

            if 'stats' in self.selected_analysis:
                for k in m.stats.keys():
                    value = m.stats[k]
                    subdict = dic_colums.setdefault(k, {})
                    subdict[str(i)] = value

        df = pd.DataFrame.from_dict(dic_colums)
        # This shouldn't happen, but the thing is that there are a few NaNs, so we better remove the entries
        df = df[~df['category'].isna()]
        return df

    def to_normalized_df(self, min_occurrences_per_category=7, languages=['english'],
                         remove_categories=['dummy', 'unknown']):
        """Dumps the dataset object to a pandas dataframe and filters according to min_occurrences_per_category,
        languages, and specific categories.

        Parameters
        ----------
        min_occurrences_per_category : int
            Minimum occurrences per category
        languages : list
            List of languages to consider
        remove_categories: list
            List of categories to remove

        Returns
        -------
        DataFrame
            a pandas dataframe
        """
        df = self.to_df()
        df = df[df['language'].isin(languages)]
        counts = df.groupby(['category'], as_index=False).count()
        categories = list(counts[counts['id'] >= min_occurrences_per_category]['category'])

        for r in remove_categories:
            Dataset.remove_from_list(categories, r)

        df = df[df['category'].isin(categories)]
        return df

    def txt_file(self, model_id):
        """Get the path of a txt file associated to a model

        Parameters
        ----------
        model_id : str
            id of the model

        Returns
        -------
        str
            path of the txt file
        """
        return self.__artefact_file(model_id, self.txt_files, 'txt')

    def graph_file(self, model_id):
        """Get the path of a json graph file associated to a model

        Parameters
        ----------
        model_id : str
            id of the model

        Returns
        -------
        str
            path of the graph json file
        """
        return self.__artefact_file(model_id, self.graph_files, 'json')

    def __artefact_file(self, model_id, folder, extension):
        f = self.get_model_by_id(model_id).filename
        prefix = folder + '/'

        name = os.path.basename(f)
        name = os.path.splitext(name)[0]
        return prefix + f + '/' + name + '.' + extension

    def as_txt(self, model_id):
        """Get the content of a text file associated to a model

        Parameters
        ----------
        model_id : str
            id of the model

        Returns
        -------
        str
            content of the text file
        """
        f = self.txt_file(model_id)
        with open(f, 'r') as file:
            return file.read()

    def as_graph(self, model_id):
        """Get the nx graph associated to a model

        Parameters
        ----------
        model_id : str
            id of the model

        Returns
        -------
        Graph
            graph associated to a model
        """
        f = self.graph_file(model_id)
        with open(f) as json_file:
            data = json.load(json_file)
        g = json_graph.node_link_graph(data)
        return g

    def get_model_by_id(self, id):
        """Get the model object given its id

        Parameters
        ----------
        id : str
            id of the model

        Returns
        -------
        Model
            model object

        """
        for m in self.models:
            if m.id == id:
                return m
        raise Exception("Model not found: " + id)

    def model_file(self, model):
        """Returns the file name of the model associated to the given id or model object

        Parameters
        ----------
        model : Model or str
            model object

        Returns
        -------
        str
            file name
        """
        if isinstance(model, Model):
            return os.path.join(self.repo_folder, model.filename)
        else:
            m = self.get_model_by_id(model)
            return self.model_file(m)

    @staticmethod
    def remove_from_list(l, value):
        try:
            l.remove(value)
        except:
            pass


class Model:
    """
    Class that represents a model of the dataset.
    It is composed of the id, model filename, dataset and metadata.
    """
    def __init__(self, id, filename, dataset, metadata):
        self.id = id
        self.filename = filename
        self.metadata = metadata
        self.dataset = dataset
        self.stats = {}

    def model_file(self):
        """Returns the file name of the model object

        Returns
        -------
        str
            file name

        """
        return self.dataset.model_file(self)

    def add_stats(self, type, value):
        """Adds stats to the model

        Parameters
        ----------
        type : str
            name of the stat

        value : int
            value of the stat
        """
        self.stats[type] = value


def split_metadata(str):
    """Splits a string with metadata information coming from the ModelSet DB into a map
       of the form { key: value-list }

    >>> split_metadata('category: a, tags: b, tags: c, type: d')
    defaultdict(<class 'list'>, {'category': ['a'], 'tags': ['b', 'c'], 'type': ['d']})
    
    >>> split_metadata('category: a, tags: b, , tags: c, type: d')
    defaultdict(<class 'list'>, {'category': ['a'], 'tags': ['b', 'c'], 'type': ['d']})
    """
    parts = str.split(',')
    labels = defaultdict(list)
    for p in parts:
        p = p.strip()
        if len(p) == 0:
            continue
        (key, value) = p.split(':', 1)
        labels[key].append(value.strip())
    return labels


def load(root_folder=DEFAULT_DIR_MODELSET, modeltype='ecore', selected_analysis=[]):
    """Loads the dataset from the provided folder. 
    Parameters
    ----------   
    root_folder : str
       The folder that contains the modelset distribution (check that it includes a folder named datasets)
    modeltype: str, optional
       The type of models of the dataset. Possible values are 'ecore' and 'uml'
    selected_analysis: list
       Analysis elements to include in the dataset. Available options: 'stats', 'smells'
    
    Returns
    -------
    Dataset
       A Dataset object
    """

    if modeltype == 'ecore':
        file = root_folder + '/datasets/dataset.ecore/data/ecore.db'
        analysis = root_folder + '/datasets/dataset.ecore/data/analysis.db'
        dataset_name = 'repo-ecore-all'
        # repo = root_folder + '/raw-data/repo-ecore-all'
        # txt_files = root_folder + '/txt/repo-ecore-all'
    elif modeltype == 'uml':
        file = root_folder + '/datasets/dataset.genmymodel/data/genmymodel.db'
        analysis = root_folder + '/datasets/dataset.genmymodel/data/analysis.db'
        dataset_name = 'repo-genmymodel-uml'
        # repo = root_folder + '/raw-data/repo-genmymodel-uml'
        # txt_files = root_folder + '/txt/repo-genmymodel-uml'
    else:
        raise Exception('Dataset type ' + modeltype + ' not supported')

    conn_ds = sqlite3.connect(file)
    conn_analysis = sqlite3.connect(analysis)
    cur = conn_ds.cursor()
    cur_analysis = conn_analysis.cursor()

    fetchall = cur.execute('select mo.id, mo.filename, mm.metadata from models mo join metadata mm on mo.id = mm.id')
    dataset = Dataset(root_folder, file, dataset_name, modeltype, selected_analysis)
    for m in fetchall:
        id = m[0]
        model = Model(id, m[1], dataset, split_metadata(m[2]))
        dataset.add_model(model)

        if 'stats' in selected_analysis:
            stats = cur_analysis.execute('select type, count from stats where id = ?', [id])
            for s in stats:
                type = s[0]
                count = s[1]
                model.add_stats(type, count)

    conn_ds.close()
    conn_analysis.close()
    return dataset


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
