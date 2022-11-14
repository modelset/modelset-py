import sys
from argparse import ArgumentParser

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC

sys.path.append("./src")
from modelset import load


def main(args):
    # load dataset and generate dataframe
    dataset = load(modeltype=args.model_type, selected_analysis=[])
    modelset_df = dataset.to_normalized_df()
    modelset_df = modelset_df[modelset_df.tags.notnull()]

    # get ids and tags
    ids = list(modelset_df['id'])
    tags = [t.split('|') for t in modelset_df['tags']]

    # one hot encoding for tags
    unique_tags = list(np.unique([t2 for t in tags for t2 in t]))
    tags_onehot = np.zeros((len(tags), len(unique_tags)))
    for i, ts in enumerate(tags):
        for t in ts:
            tags_onehot[i, unique_tags.index(t)] = 1

    # remove tags that have a low number o models
    models_per_tag = np.sum(tags_onehot, axis=0)
    to_remove = []
    for i, c in enumerate(models_per_tag):
        if c < 4:
            to_remove.append(i)
    tags_onehot = np.delete(tags_onehot, to_remove, axis=1)
    unique_tags = np.delete(unique_tags, to_remove)

    # train test split
    train_X, test_X, train_y, test_y = train_test_split(ids, tags_onehot, test_size=0.2, random_state=42)

    # get txt filenames
    train_filenames = [dataset.txt_file(id) for id in train_X]
    test_filenames = [dataset.txt_file(id) for id in test_X]

    # extract features
    vectorizer = TfidfVectorizer(input='filename', min_df=2)
    X = vectorizer.fit_transform(train_filenames)
    T = vectorizer.transform(test_filenames)

    # training phase
    clf = MultiOutputClassifier(SVC(random_state=42)).fit(X, train_y)

    # evaluation over test set
    predict_test = clf.predict(T)
    cm = multilabel_confusion_matrix(test_y, predict_test)
    for i, t in enumerate(unique_tags):
        print(f'Tag {t}')
        print(cm[i])


if __name__ == '__main__':
    parser = ArgumentParser(description='Train a SVM with TF-IDF')
    parser.add_argument('--model_type', default='ecore', choices=['ecore', 'uml'])
    args = parser.parse_args()
    main(args)
