from os import listdir
import pickle
import logging
import json
import requests
import numpy as np
import spacy
from halo import Halo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from luci.settings import LISA_URL


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


@Halo(text='Loading spacy', spinner='dots')
def load_spacy():
    return spacy.load('pt')


def request_text_vectors(texts):
    """
    Requests the vectorial array extracted from each token of each text
    in the inputed list. The request is sent to LISA API as text, expecting
    a list of float as response. The sentence is finally representend by
    the vectorial sum of all vectors from all tokens that belong to the sentence
    and the appended as a numpy array to a list that will be returned containing
    all the text vectors.

    param : texts : <list> of <str>;
    return: <list> of Numpy Array;
    """
    vectors = []

    for text in texts:
        data = f'''
        query{{
            inspectTokens(text: {json.dumps(text)}) {{
                vector
            }}
        }}
        '''
        request = requests.post(LISA_URL, json={'query': data})
        response = json.loads(request.text)

        sample = sum(
            [np.array(v['vector']) for v in response['data']['inspectTokens']]
        )
        vectors.append(sample)

    return vectors


def train_bot():
    """
    Train all Luci models.
    """
    logging.info('Training global intentions')
    samples = train_global_intentions()
    logging.info(f'done! Trained {samples} samples.')

    logging.info('Training myself intentions')
    samples = train_myself_intentions()
    logging.info(f'done! Trained {samples} samples.')

    logging.info('Training bad intentions')
    samples = train_bad_intentions()
    logging.info(f'done! Trained {samples} samples.')

    logging.info('Training good intentions')
    samples = train_good_intentions()
    logging.info(f'done! Trained {samples} samples.')

    logging.info('Training friends intentions')
    samples = train_about_my_friends_intentions()
    logging.info(f'done! Trained {samples} samples.')

    logging.info('Training parents intentions')
    samples = train_about_my_parents_intentions()
    logging.info(f'done! Trained {samples} samples.')

    logging.info('Training stuff i like intentions')
    samples = train_stuff_i_like_intentions()
    logging.info(f'done! Trained {samples} samples.')


def get_data_from_json(path):
    datasets = listdir(path)
    samples = []
    targets = []

    for dataset in datasets:
        with open(f'{path}{dataset}', 'r') as f:
            raw_data = json.load(f)
            for data in raw_data:
                samples.append(nlp(data['text']).vector)
                targets.append(data['intention'])

    return samples, targets


@Halo(text='Training global intentions', spinner='dots')
def train_global_intentions():
    """
    Train a Logistic Regression model to recognize Luci global intentions.
    """
    model = LogisticRegression(max_iter=1000)
    path = 'core/training/json/intentions/global_intentions/'
    samples, targets = get_data_from_json(path)

    model.fit(samples, targets)
    with open('luci/models/global_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    # returns the number o data samples learned
    return len(targets)


@Halo(text='Training myself intentions', spinner='dots')
def train_myself_intentions():
    """
    Train a KNeighborsClassifier model to recognize Luci global intentions.
    """
    model = KNeighborsClassifier(leaf_size=25, p=1)
    path = 'core/training/json/intentions/about_myself/'
    samples, targets = get_data_from_json(path)

    model.fit(samples, targets)
    with open('luci/models/myself_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    return len(targets)


@Halo(text='Training bad intentions', spinner='dots')
def train_bad_intentions():
    """
    Train a LineraRegression model to recognize bad intentions.
    """
    model = LogisticRegression(max_iter=1000)
    path = 'core/training/json/intentions/bad_intentions/'
    samples, targets = get_data_from_json(path)

    model.fit(samples, targets)
    with open('luci/models/bad_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    return len(targets)


@Halo(text='Training good intentions', spinner='dots')
def train_good_intentions():
    """
    Train a Logistic Regression model to recognize good intentions.
    """
    model = LogisticRegression(max_iter=1000, solver='liblinear')
    path = 'core/training/json/intentions/good_intentions/'
    samples, targets = get_data_from_json(path)

    model.fit(samples, targets)
    with open('luci/models/good_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    return len(targets)


@Halo(text='Training friends intentions', spinner='dots')
def train_about_my_friends_intentions():
    """
    Train a Logistic Regression model to recognize friendship intentions.
    """
    model = LogisticRegression(max_iter=1000)
    path = 'core/training/json/intentions/about_friends/'
    samples, targets = get_data_from_json(path)
    
    model.fit(samples, targets)
    with open('luci/models/friends_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    return len(targets)


@Halo(text='Training parents intentions', spinner='dots')
def train_about_my_parents_intentions():
    """
    Train a Logistic Regression model to recognize parentship intentions.
    """
    model = LogisticRegression(max_iter=1000)
    path = 'core/training/json/intentions/about_parents/'
    samples, targets = get_data_from_json(path)

    model.fit(samples, targets)
    with open('luci/models/parents_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    return len(targets)


@Halo(text='Training stuff i like intentions', spinner='dots')
def train_stuff_i_like_intentions():
    """
    Train a Logistic Regression model to recognize stuff Luci likes intentions.
    """
    model = LogisticRegression(max_iter=1000)
    path = 'core/training/json/intentions/stuff_i_like/'
    samples, targets = get_data_from_json(path)

    model.fit(samples, targets)
    with open('luci/models/stuff_i_like_intentions', 'wb') as fpath:
        pickle.dump(model, fpath)

    return len(targets)


def no_free_lunch():
    """
    Tests the score for different models. A model will not fit on every data
    samples but certainly, some will show better performance.

    param: data : <list> os np.Array;
    param: targets :np.Array
    """
    path = 'core/training/json/intentions/'
    dirs = listdir(path)
    for dir_ in dirs:
        data, targets = get_data_from_json(f'{path}{dir_}/')

        logging.info(f'Testing training data on {dir_}')
        logging.info('_'*50)

        X_train, X_test , y_train, y_test = train_test_split(
            data, targets, random_state=0
        )

        for model in [
            LogisticRegression,
            DecisionTreeClassifier,
            KNeighborsClassifier,
            GaussianNB,
            RandomForestClassifier
        ]:
            try:
                cls = model(max_iter=1000)
            except:
                cls = model()

            cls.fit(X_train, y_train)

            # test prediction
            y_pred = cls.predict(X_test)

            # scores
            precision_score = metrics.precision_score(
                y_test, y_pred, average='weighted', labels=np.unique(y_pred)
            )
            f1_score = metrics.f1_score(
                y_test, y_pred, average="weighted", labels=np.unique(y_pred)
            )

            logging.info(f'{model.__name__:22} test set score: {np.mean(y_pred == y_test):.2f}')
            logging.info(f'Precision score: {precision_score}')
            logging.info(f'f1 score: {f1_score}')
        
        logging.info(f'Number of Test Samples: {len(X_train)}')
        logging.info(f'Total Samples: {len(targets)}')

        logging.info('_'*50)


    # from sklearn.neural_network import MLPClassifier
    # nn = MLPClassifier(
    #     hidden_layer_sizes=(10, ),
    #     activation='relu',
    #     solver='adam',
    #     alpha=0.0001,
    #     batch_size='auto',
    #     learning_rate='constant',
    #     learning_rate_init=0.001,
    #     power_t=0.5,
    #     max_iter=1000,
    #     shuffle=True,
    #     random_state=None,
    #     tol=0.0001,
    #     verbose=False,
    #     warm_start=False,
    #     momentum=0.9,
    #     nesterovs_momentum=True,
    #     early_stopping=False,
    #     validation_fraction=0.1,
    #     beta_1=0.9,
    #     beta_2=0.999,
    #     epsilon=1e-08,
    #     n_iter_no_change=10,
    #     max_fun=15000
    # )
    # nn.fit(X_train, y_train)
    # pred = nn.predict(X_test)
    # print(f"test set score: {np.mean(pred == y_test):.2f}")
    # print(metrics.precision_score(y_test, pred, average='weighted'))


logging.info('Loading spacy...')
nlp = load_spacy()
logging.info('... done!')
