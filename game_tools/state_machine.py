import networkx as nx
from enum import Enum
import numpy as np


class States(Enum):
    START = 1
    P1_CHOOSING = 2
    P1_SECRET = 3
    P1_BURN = 4
    P1_GIFT = 5
    P1_COMP = 6
    P2_RESPONDG_GIFT = 7
    P2_RESPOND_COMP = 8
    P2_CHOOSING = 9
    P2_SECRET = 10
    P2_BURN = 11
    P2_GIFT = 12
    P2_COMP = 13
    P1_RESPONDG_GIFT = 14
    P1_RESPOND_COMP = 15
    IS_IT_OVER = 16
    END = 17

    def is_p1_choosing_cards(self):
        if self.value in [3, 4, 5, 6]:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.value > other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __hash__(self):
        return self.value


class HanamikojiStateMachine:

    edges = [(1, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
             (3, 2), (3, 4), (3, 5), (3, 6), (3, 9),
             (4, 2), (4, 3), (4, 5), (4, 6), (4, 9),
             (5, 2), (5, 3), (5, 4), (5, 6), (5, 7),
             (6, 2), (6, 3), (6, 4), (6, 5), (6, 8),
             (7, 9), (8, 9), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (10, 9), (10, 16), (11, 9), (11, 16), (12, 9),
             (12, 14), (13, 9), (13, 15), (14, 16), (15, 16), (16, 2), (16, 17)]

    plot_pos = {1: np.array([-0.75, 0.5]), 2: np.array([-0.5, 0.5]), 3: np.array([0.0, 0.8]), 4: np.array([0.0, 0.6]),
                5: np.array([-0.2, 0.4]), 8: np.array([0.0, 0.2]), 6: np.array([-0.2, 0.2]), 7: np.array([0.0, 0.4]),
                9: np.array([0.5, 0.5]), 10: np.array([0.2, 0.0]), 11: np.array([0.4, 0.0]), 12: np.array([0.6, 0.2]),
                13: np.array([0.8, 0.2]), 14: np.array([0.6, 0.0]), 15: np.array([0.8, 0.0]), 16: np.array([-0.5, -0.5]),
                17: np.array([-0.5, -0.8])}

    def __init__(self):
        self.graph = nx.DiGraph(self.edges)
        self.state = States.START
        self.turn = 0

    @property
    def states(self):
        return {x: States(x) for x in self.graph.nodes}

    @property
    def transitions(self):
        return {x: (States(x[0]), States(x[1])) for x in self.graph.edges}

    def get_allowed_transitions(self):
        return [States(e[1]) for e in self.graph.edges if e[0] == self.state]

    def to(self, next_state):
        if next_state in self.get_allowed_transitions():
            print(f'State Machine transition from: {self.state} to {next_state}.')
            self.state = States(next_state)
        else:
            raise Exception(f'\n State Transition from: {self.state} to {next_state} NOT ALLOWED.')

    def jump_to(self, next_state):
        self.state = States(next_state)

    def remove_state(self, state_to_remove):
        self.graph.remove_node(state_to_remove.value)

    def remove_transition(self, origin_state, destination_state):
        self.graph.remove_edge(origin_state.value, destination_state.value)

    def plot(self):
        nx.draw_networkx(self.graph, pos=self.plot_pos, with_labels=True)

    def reset(self):
        self.graph = nx.DiGraph(self.edges)
        self.state = States.START

    def __repr__(self):
        return f'Hanamikoji State Machine at state: {self.state} in turn: {self.turn}.'
