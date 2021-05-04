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
from core.training.text_gen import model as lstm_model


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


@Halo(text='Loading spacy', spinner='dots')
def load_spacy():
    return spacy.load('pt')


def train_bot():
    """
    Train all Luci models.
    """
    logging.info('STARTING INTENTION CLASSIFIER TRAINING')
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

    logging.info('STARTING GENERAL ADVERSARIAL NETWORKS TRAINING')
    train_who_am_i_gan()
    train_acknowledgement_gan()
    train_forbidden_gan()
    train_funny_gan()
    train_greeting_gan()
    train_helpful_gan()
    train_illegal_stuff()
    train_music_gan()
    train_age_gan()
    train_gender_gan()
    train_praise_gan()
    train_racism_xenophobia_gan()
    train_sports_and_playing_gan()
    train_sexual_abuse_gan()
    train_sorry_gan()
    train_suicide_gan()
    train_threat_gan()
    train_verbal_offense_gan()
    train_what_am_i_gan()
    train_goodbye_gan()
    logging.info('Done!')


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


@Halo(text='Training who am i gan', spinner='dots')
def train_who_am_i_gan():
    data = open('core/training/output_samples/who_am_i.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/who_am_i.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        700,
        0.01
    )
    with open('luci/models/who_am_i_gan', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nwho_am_i GAN total loss: %s\n', loss[-1])


@Halo(text='Training goodbye gan', spinner='dots')
def train_goodbye_gan():
    data = open('core/training/output_samples/goodbye.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/goodbye.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        700,
        0.01
    )
    with open('luci/models/goodbye', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\goodbye GAN total loss: %s\n', loss[-1])


@Halo(text='Training acknowledgement gan', spinner='dots')
def train_acknowledgement_gan():
    data = open('core/training/output_samples/acknowledgement.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/acknowledgement.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/acknowledgement', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nacknowledgement GAN total loss: %s\n', loss[-1])


@Halo(text='Training forbidden gan', spinner='dots')
def train_forbidden_gan():
    data = open('core/training/output_samples/forbidden.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/forbidden.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/forbidden', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nforbidden GAN total loss: %s\n', loss[-1])


@Halo(text='Training funny gan', spinner='dots')
def train_funny_gan():
    data = open('core/training/output_samples/funny.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/funny.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/funny', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nfunny GAN total loss: %s\n', loss[-1])


@Halo(text='Training greeting gan', spinner='dots')
def train_greeting_gan():
    data = open('core/training/output_samples/greeting.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/greeting.txt',
        chars_to_idx, idx_to_chars,
        150,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/greeting', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\ngreeting GAN total loss: %s\n', loss[-1])


@Halo(text='Training helpful gan', spinner='dots')
def train_helpful_gan():
    data = open('core/training/output_samples/helpful.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/helpful.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/helpful', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nhelpful GAN total loss: %s\n', loss[-1])


@Halo(text='Training illegal stuff gan', spinner='dots')
def train_illegal_stuff():
    data = open('core/training/output_samples/illegal_stuff.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/illegal_stuff.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/illegal_stuff', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nillegal_stuff GAN total loss: %s\n', loss[-1])


@Halo(text='Training music gan', spinner='dots')
def train_music_gan():
    data = open('core/training/output_samples/music.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/music.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/music', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nmusic GAN total loss: %s\n', loss[-1])


@Halo(text='Training age gan', spinner='dots')
def train_age_gan():
    data = open('core/training/output_samples/my_age.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/my_age.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/my_age', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nmy_age GAN total loss: %s\n', loss[-1])


@Halo(text='Training gender gan', spinner='dots')
def train_gender_gan():
    data = open('core/training/output_samples/my_gender.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/my_gender.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/my_gender', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nmy_gender GAN total loss: %s\n', loss[-1])


@Halo(text='Training praise gan', spinner='dots')
def train_praise_gan():
    data = open('core/training/output_samples/praise.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/praise.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/praise', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\npraise GAN total loss: %s\n', loss[-1])


@Halo(text='Training racism and xenophobia gan', spinner='dots')
def train_racism_xenophobia_gan():
    data = open('core/training/output_samples/racism_xenophobia.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/racism_xenophobia.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/racism_xenophobia', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('racism_xenophobia GAN total loss: %s', loss[-1])


@Halo(text='Training sexual abuse gan', spinner='dots')
def train_sexual_abuse_gan():
    # Load names
    data = open('core/training/output_samples/sexual_abuse.txt').read()
    # Convert characters to lower case
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/sexual_abuse.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/sexual_abuse', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('sexual_abuse GAN total loss: %s', loss[-1])


@Halo(text='Training sorry gan', spinner='dots')
def train_sorry_gan():
    data = open('core/training/output_samples/sorry.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/sorry.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/sorry', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nsorry GAN total loss: %s', loss[-1])


@Halo(text='Training suicide gan', spinner='dots')
def train_suicide_gan():
    data = open('core/training/output_samples/suicide.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/suicide.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/suicide', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nsuicide GAN total loss: %s', loss[-1])


@Halo(text='Training sports and playing gan', spinner='dots')
def train_sports_and_playing_gan():
    data = open('core/training/output_samples/sports_and_playing.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/sports_and_playing.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/sports_and_playing', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nsports_and_playing GAN total loss: %s', loss[-1])


@Halo(text='Training threat gan', spinner='dots')
def train_threat_gan():
    data = open('core/training/output_samples/threat.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/threat.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/threat', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nthreat GAN total loss: %s\n', loss[-1])


@Halo(text='Training verbal offensa gan', spinner='dots')
def train_verbal_offense_gan():
    data = open('core/training/output_samples/verbal_offense.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/verbal_offense.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/verbal_offense', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nverbal_offense GAN total loss: %s\n', loss[-1])


@Halo(text='Training what am i gan', spinner='dots')
def train_what_am_i_gan():
    data = open('core/training/output_samples/what_am_i.txt').read()
    data = data.lower()

    chars = list(sorted(set(data)))
    chars_to_idx = {ch:i for i, ch in enumerate(chars)}
    idx_to_chars = {i:ch for ch, i in chars_to_idx.items()}

    # Get the size of the data and vocab size
    data_size = len(data)
    vocab_size = len(chars_to_idx)
    logging.info(f'\nThere are {data_size} characters and {vocab_size} unique characters.')

    # Fitting the model
    parameters, loss = lstm_model(
        'core/training/output_samples/what_am_i.txt',
        chars_to_idx, idx_to_chars,
        100,
        vocab_size,
        500,
        0.01
    )
    with open('luci/models/what_am_i', 'wb') as fpath:
        pickle.dump([parameters, chars_to_idx, idx_to_chars], fpath)

    logging.info('\nwhat_am_i GAN total loss: %s', loss[-1])


@Halo(text='Training global intentions', spinner='dots')
def train_global_intentions():
    """
    Train a Logistic Regression model to recognize Luci global intentions.
    """
    model = LogisticRegression(max_iter=1000, solver='liblinear')
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
    model = LogisticRegression(max_iter=1000, solver='liblinear')
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
    model = LogisticRegression(max_iter=1000, solver='liblinear')
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
    model = LogisticRegression(max_iter=1000, solver='liblinear')
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
    model = LogisticRegression(max_iter=1000, solver='liblinear')
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
