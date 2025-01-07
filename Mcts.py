import random
import time
import math
from copy import deepcopy
from ConnectState import ConnectState
from meta import GameMeta, MCTSMeta

class TreeNode:
    def __init__(self, action, parent_node):
        """
        Initializes a TreeNode with an action, parent node, visit count,
        win count, children, and game outcome.
        """
        self.action = action
        self.parent_node = parent_node
        self.visit_count = 0  # Node visit count
        self.win_count = 0    # Node win count
        self.children = {}
        self.outcome = GameMeta.PLAYERS['none']
        self.nodes_expanded = 0

    def add_children(self, child_nodes: list) -> None:
        """
        Adds child nodes to the current node.
        """
        for child in child_nodes:
            self.children[child.action] = child

    def calculate_value(self, exploration: float = MCTSMeta.EXPLORATION):
        """
        Calculates the value of the node using the UCT formula.
        """
        if self.visit_count == 0:
            return 0 if exploration == 0 else GameMeta.INF
        else:
            return self.win_count / self.visit_count + exploration * math.sqrt(math.log(self.parent_node.visit_count) / self.visit_count)

class MonteCarloTreeSearch:
    def __init__(self, state=ConnectState()):
        """
        Initializes the MCTS with the initial game state.
        """
        self.root_state = deepcopy(state)
        self.root_node = TreeNode(None, None)
        self.execution_time = 0
        self.node_count = 0
        self.rollout_count = 0

    def select_promising_node(self) -> tuple:
        """
        Selects the most promising node to explore by traversing the tree using the UCT formula.
        """
        current_node = self.root_node
        game_state = deepcopy(self.root_state)
        while current_node.children:
            children_nodes = list(current_node.children.values())
            max_value = max(child.calculate_value() for child in children_nodes)
            best_nodes = [child for child in children_nodes if child.calculate_value() == max_value]
            current_node = random.choice(best_nodes)
            game_state.make_move(current_node.action)  # Use make_move
            if current_node.visit_count == 0:
                return current_node, game_state
        if self.expand_node(current_node, game_state):
            current_node = random.choice(list(current_node.children.values()))
            game_state.make_move(current_node.action)  # Use make_move
        return current_node, game_state

    def expand_node(self, parent_node: TreeNode, game_state: ConnectState) -> bool:
        """
        Expands the given node by adding all possible actions as children.
        """
        if game_state.is_game_over():  # Use is_game_over
            return False
        child_nodes = [TreeNode(action, parent_node) for action in game_state.available_moves()]  # Use available_moves
        parent_node.add_children(child_nodes)
        return True

    def simulate_random_playout(self, game_state: ConnectState) -> int:
        """
        Simulates a random playout from the given game state until the game ends.
        """
        while not game_state.is_game_over():  # Use is_game_over
            game_state.make_move(random.choice(game_state.available_moves()))  # Use make_move and available_moves
        return game_state.get_winner()  # Use get_winner

    def backpropagate(self, node: TreeNode, current_turn: int, outcome: int) -> None:
        """
        Backpropagates the result of a simulation through the tree.
        """
        reward = 0 if outcome == current_turn else 1
        while node:
            node.visit_count += 1
            node.win_count += reward
            node = node.parent_node
            reward = 0 if outcome == GameMeta.OUTCOMES['draw'] else 1 - reward

    def run_search(self, time_limit: int):
        """
        Conducts the MCTS for a specified time limit.
        """
        start_time = time.process_time()
        while time.process_time() - start_time < time_limit:
            node, state = self.select_promising_node()
            outcome = self.simulate_random_playout(state)
            self.backpropagate(node, state.current_player, outcome)  # Use current_player
            self.rollout_count += 1
        self.execution_time = time.process_time() - start_time

    def determine_best_move(self):
        """
        Determines the best move from the root node based on the visit count.
        """
        if self.root_state.is_game_over():  # Use is_game_over
            return -1
        max_visits = max(child.visit_count for child in self.root_node.children.values())
        best_children = [child for child in self.root_node.children.values() if child.visit_count == max_visits]
        best_choice = random.choice(best_children)
        return best_choice.action
    def perform_move(self, action):
        """0
        Updates the root to the child corresponding to the given action.
        """
        if action in self.root_node.children:
            self.root_state.make_move(action)  # Use make_move
            self.root_node = self.root_node.children[action]
        else:
            self.root_state.make_move(action)  # Use make_move
            self.root_node = TreeNode(None, None)

    def get_statistics(self) -> tuple:
        """
        Returns the number of rollouts and the execution time.
        """
        return self.rollout_count, self.execution_time, self.get_max_depth()

    def get_max_depth(self):
        """
        Calculates the maximum depth of the tree.
        """

        def depth(node):
            if not node.children:
                return 1
            return 1 + max(depth(child) for child in node.children.values())

        return depth(self.root_node)  # Call depth on root_node

def play_game():
    state = ConnectState()
    mcts = MonteCarloTreeSearch(state)
    game_over = False  # Flag to track if the game is over

    while not game_over:
        print("Current state:")
        state.display()
        user_move = int(input("Enter a move: "))
        while user_move not in state.available_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))
        state.make_move(user_move)
        mcts.perform_move(user_move)
        state.display()
        if state.is_game_over():
            print("Player one won!")
            game_over = True
            break
        print("AI Move...")
        mcts.run_search(8)
        num_rollouts, run_time, max_depth = mcts.get_statistics()
        print(f"Statistics: {num_rollouts} rollouts in {run_time} seconds, Max Depth: {max_depth}")
        move = mcts.determine_best_move()
        print(f"MCTS chose move: {move}")
        state.make_move(move)
        mcts.perform_move(move)
        if state.is_game_over():
            print("Player two won!")
            game_over = True
            break

if __name__ == "__main__":
    MCTSMeta.EXPLORATION = 1.5
    play_game()
