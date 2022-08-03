from collections import Counter
from random import randint
import random
import numpy as np
from core.external_requests import Query
from core.utils import get_gql_client, remove_id
from luci.settings import BACKEND_URL


def filter_messages(messages):
    text = [m for m in messages
            if (len(m.split()) > 1
            and not m.startswith(';')
            and '@' not in m
            and 'http' not in m
            and not m.startswith('!')
            and not m.startswith('/')
            and not m.startswith('>'))]
    return text


def get_relations(messages):
    temp = {}
    for message in messages:
        tokens = message.split()
        for i, token in enumerate(tokens):
            token = token.lower().strip()
            if token not in temp:
                temp[token] = []

            if i+1 < len(tokens):
                temp[token].append(tokens[i+1].lower().strip())
            else:
                temp[token].append('EOS')

    relations = {}
    for k, v in temp.items():
        frequency = {token: count/len(v) for token, count in Counter(v).items()}
        relations[k] = frequency

    return relations


def get_map(relations):
    i_to_actions = {i:token for i, token in enumerate(relations.keys())}
    actions_to_i = {v:k for k, v in i_to_actions.items()}
    return i_to_actions, actions_to_i


def get_environment(relations, i_to_actions, actions_to_i):
    environment = {}
    for state, action in i_to_actions.items():
        environment[state] = []
        for fate, prob in relations[action].items():
            if fate == 'EOS':
                environment[-2] = [('EOS',[[-1,-1,1]])]
            else:
                environment[state].append((
                    fate,
                    [[actions_to_i[fate], randint(-3, 0), prob]]
                ))
    return environment


def get_q_matrix(environment):
    q_matrix = []
    for _ in range(len(environment)):
        q_matrix.append([0 for _ in range(len(environment))])
    return q_matrix


def get_exit_states(relations, actions_to_i):
    exit_states = []
    for token, fates in relations.items():
        fate = list({k: v for k, v in sorted(fates.items(), key=lambda item: item[1])}.keys())
        if fate[-1] == 'EOS':
            exit_states.append(actions_to_i[token])

    exit_states += [-1, -2]
    return exit_states


def get_possible_next_actions(cur_pos, environment):
    if cur_pos in environment:
        return environment[cur_pos]
    else:
        return []


def get_next_state(action):
    # word = action[0]
    possible_states = action[1]
    fate = {}
    for p in possible_states:
        s = p[0]
        r = p[1]
        l = p[2]
        fate[s] = [r, l]
    
    # normalize
    p = [v[1] for v in fate.values()]
    p = np.array(p)
    p /= p.sum()
    next_state = np.random.choice(list(fate.keys()), 1, p=p)
    reward = fate[next_state[0]][0]
    return next_state[0], reward


def game_over(cur_pos, exit_states):
    return cur_pos in exit_states or cur_pos == []


def train(environment, q_matrix, actions_to_i, exit_states, learning_rate=0.1, epochs=200):
    discount = 0.99
    learning_rate = 0.1

    for _ in range(epochs):
        # while goal state is not reached
        cur_pos = 0
        episode_return = 0
        while(not game_over(cur_pos, exit_states)):
            # get all possible next states from cur_step
            possible_actions = get_possible_next_actions(cur_pos, environment)
            # select any one action randomly
            if not possible_actions:
                break
            action = random.choice(possible_actions)
            word = action[0]
            action_i = actions_to_i[word]
            # find the next state corresponding to the action selected
            next_state,reward = get_next_state(action)
            episode_return+=reward

            # update the q_matrix
            next_state_possible_actions = get_possible_next_actions(next_state, environment)
            action_values = []
            max_value = 0
            if next_state_possible_actions != []:
                for action in next_state_possible_actions:
                    action_values.append(q_matrix[next_state][actions_to_i[action[0]]])
                max_value = max(action_values)
            
            q_matrix[cur_pos][action_i] = q_matrix[cur_pos][action_i] + learning_rate * (reward + discount * max_value - q_matrix[cur_pos][action_i])
            # go to next state
            cur_pos = next_state
    
    return q_matrix

def gen_text(environment, q_matrix, exit_states, actions_to_i, cur_pos=0):
    episode_return = 0
    output = []
    while(not game_over(cur_pos, exit_states)):
        # get all possible next states from cur_step
        possible_actions = get_possible_next_actions(cur_pos, environment)
    
        # select the *possible* action with highest Q value
        action = None
        if np.linalg.norm(q_matrix[cur_pos]) == 0:
            action = random.choice(possible_actions)
        else:
            action = actions_to_i[possible_actions[0][0]]
            c = 0
            action_i = c
            for a in possible_actions:
                a_i = actions_to_i[a[0]]
                if q_matrix[cur_pos][a_i] > q_matrix[cur_pos][action]:
                    action = a_i
                    action_i = c
                c+=1
            action = possible_actions[action_i]
    
        output.append(action[0])
        next_state,reward = get_next_state(action)
        episode_return+=reward
        cur_pos = next_state

    return ' '.join(output).strip(), episode_return


def get_responses(text):
    gql_client = get_gql_client(BACKEND_URL)
    # busca possíveis respostas na memória de longo prazo
    payload = Query.get_possible_responses(
        text=remove_id(text)
    )

    try:
        response = gql_client.execute(payload)
    except Exception as _:
        response = {'messages': []}

    responses = []
    for message in response['messages']:
        for r in message['possible_responses']:
            responses.append(r['text'])
    return responses


def generate_answer(text):
    messages = filter_messages(get_responses(text))
    if not messages:
        return

    relations = get_relations(messages)
    i_to_actions, actions_to_i = get_map(relations)
    environment = get_environment(relations, i_to_actions, actions_to_i)
    q_matrix = get_q_matrix(environment)
    exit_states = get_exit_states(relations, actions_to_i)
    kb = train(environment, q_matrix, actions_to_i, exit_states)

    return gen_text(environment, kb, exit_states, actions_to_i)[0]
