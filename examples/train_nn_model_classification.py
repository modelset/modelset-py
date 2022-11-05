import sys
from argparse import ArgumentParser

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

sys.path.append("./src")

from modelset import load


def main(args):
    # load dataset and generate dataframe
    dataset = load(modeltype=args.model_type, selected_analysis=['stats'])
    modelset_df = dataset.to_normalized_df()

    # get ids and categories
    ids = modelset_df['id']
    labels = modelset_df['category']

    # train test split
    train_X, test_X, train_y, test_y = train_test_split(ids, labels, test_size=0.2, random_state=42)

    # get txt filenames
    train_filenames = [dataset.txt_file(id) for id in train_X]
    test_filenames = [dataset.txt_file(id) for id in test_X]

    # extract features
    vectorizer = TfidfVectorizer(input='filename', min_df=2)
    X = vectorizer.fit_transform(train_filenames)
    T = vectorizer.transform(test_filenames)

    # training phase
    clf = MLPClassifier(solver='adam', learning_rate_init=0.01,
                        hidden_layer_sizes=(64,), random_state=1,
                        verbose=True)
    clf.fit(X, train_y)

    # evaluation over test set
    predict_test = clf.predict(T)
    test_report = classification_report(test_y, predict_test, output_dict=True, zero_division=0)
    print("Test accuracy: ", test_report['accuracy'])


if __name__ == '__main__':
    parser = ArgumentParser(description='Train a NN with TF-IDF')
    parser.add_argument('--model_type', default='ecore', choices=['ecore', 'uml'])
    args = parser.parse_args()
    main(args)
