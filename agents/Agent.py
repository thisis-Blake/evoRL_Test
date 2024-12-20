import random


class Agent:
    def __init__(self, action_set, traits):
        self.action_set = action_set
        self.traits = traits  # Example traits: speed, stamina
        self.policy = self.random_policy  # Start with random policy
        self.q_table = {}  # Initialize Q-table
        self.fitness = 0  # Initialize fitness to 0

    def random_policy(self, state):
        """Choose an action randomly from the action set."""
        return random.choice(self.action_set)

    def policy(self, state, epsilon=0.1):
        """Epsilon-greedy policy: choose the best action or explore."""
        if random.random() < epsilon:  # Exploration
            return random.choice(self.action_set)
        if state in self.q_table:  # Exploitation
            return max(self.q_table[state], key=self.q_table[state].get)
        return random.choice(self.action_set)  # Default to random if state unknown

    def update_q_table(self, state, action, reward, next_state, alpha=0.1, gamma=0.9):
        """Update Q-values using the Q-learning formula."""
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.action_set}  # Initialize actions

        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in self.action_set}

        best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
        self.q_table[state][action] += alpha * (
            reward + gamma * self.q_table[next_state][best_next_action] - self.q_table[state][action]
        )

class Predator(Agent):
    def __init__(self, traits):
        action_set = ["left", "right", "up", "down", "rest"]
        super().__init__(action_set, traits)

class Prey(Agent):
    def __init__(self, traits):
        action_set = ["left", "right", "up", "down", "rest"]
        super().__init__(action_set, traits)