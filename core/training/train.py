import pickle
import logging
import json
import requests
import numpy as np
import spacy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from core.training.training_data import global_intent_samples, myself_intent_samples
from luci.settings import LISA_URL

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
nlp = spacy.load('pt')


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
    train_global_intentions()
    train_myself_intentions()


def train_global_intentions():
    """
    Train a Logistic Regression model to recognize Luci global intentions.
    The chosen model shows better performance with a precision score of
    0.9376693766937669 (93%) accuracy on test data.
    """
    logging.info('Training global intentions')
    model = LogisticRegression()
    samples = [nlp(sample['text']).vector for sample in global_intent_samples]

    targets = np.array(
        [sample['intention'] for sample in global_intent_samples]
    )

    model.fit(samples, targets)
    pickle.dump(model, open('luci/models/global_intentions', 'wb'))
    logging.info('done')


def train_myself_intentions():
    """
    Train a K-Neighbors model to recognize Luci global intentions.
    The chosen model shows better performance with a precision score of
    0.8843537414965985 (88%) accuracy on test data.
    """
    logging.info('Training myself intentions')
    model = KNeighborsClassifier()
    samples = [nlp(sample['text']).vector for sample in myself_intent_samples]

    targets = np.array(
        [sample['intention'] for sample in myself_intent_samples]
    )

    model.fit(samples, targets)
    pickle.dump(model, open('luci/models/myself_intentions', 'wb'))
    logging.info('done')


def no_free_lunch():
    """
    Tests the score for different models. A model will not fit on every data
    samples but certainly, some will show better performance.

    param: data : <list> os np.Array;
    param: targets :np.Array
    """
    # from sklearn import model_selection
    # from sklearn.dummy import DummyClassifier
    # from sklearn.tree import DecisionTreeClassifier
    # from sklearn.neighbors import KNeighborsClassifier
    # from sklearn.naive_bayes import GaussianNB
    # from sklearn.svm import SVC
    # from sklearn.ensemble import RandomForestClassifier
    from sklearn import metrics

    samples = [nlp(sample['text']).vector for sample in myself_intent_samples]

    targets = np.array(
        [sample['intention'] for sample in myself_intent_samples]
    )


    X_train, X_test , y_train, y_test = train_test_split(
        samples, targets, random_state=0
    )

    # for model in [
    #     DummyClassifier,
    #     LogisticRegression,
    #     DecisionTreeClassifier,
    #     KNeighborsClassifier,
    #     GaussianNB,
    #     SVC,
    #     RandomForestClassifier
    # ]:
    #     cls = model()
    #     cls.fit(X_train, y_train)

    #     pred = cls.predict(X_test)
    #     print(f"{model.__name__:22} test set score: {np.mean(pred == y_test):.2f}")
    #     print(metrics.precision_score(y_test, pred, average='weighted'))

    from sklearn.neural_network import MLPClassifier
    nn = MLPClassifier(
        hidden_layer_sizes=(10, ),
        activation='relu',
        solver='adam',
        alpha=0.0001,
        batch_size='auto',
        learning_rate='constant',
        learning_rate_init=0.001,
        power_t=0.5,
        max_iter=1000,
        shuffle=True,
        random_state=None,
        tol=0.0001,
        verbose=False,
        warm_start=False,
        momentum=0.9,
        nesterovs_momentum=True,
        early_stopping=False,
        validation_fraction=0.1,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-08,
        n_iter_no_change=10,
        max_fun=15000
    )
    nn.fit(X_train, y_train)
    pred = nn.predict(X_test)
    print(f"test set score: {np.mean(pred == y_test):.2f}")
    print(metrics.precision_score(y_test, pred, average='weighted'))