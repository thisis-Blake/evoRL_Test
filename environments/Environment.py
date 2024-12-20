import random
class Environment:
    def __init__(self, grid_size, obstacles):
        self.grid_size = grid_size  # Example: (10, 10)
        self.obstacles = obstacles  # List of obstacle positions

    def step(self, predators, prey):
        """Advance the environment by one time step."""
        for predator in predators:
            state = self.get_state(predator)
            action = predator.policy(state)
            reward = self.calculate_predator_fitness(predator)
            next_state = self.get_next_state(predator, action)
            predator.update_q_table(state, action, reward, next_state)
            predator.traits["position"] = next_state  # Use the tuple directly

        for prey_agent in prey:
            state = self.get_state(prey_agent)
            action = prey_agent.policy(state)
            reward = self.calculate_prey_fitness(prey_agent)
            next_state = self.get_next_state(prey_agent, action)
            prey_agent.update_q_table(state, action, reward, next_state)
            prey_agent.traits["position"] = next_state  # Use the tuple directly


    def get_state(self, agent):
        """Return the current state for a given agent."""
        position = agent.traits.get("position", (0, 0))  # Default position
        stamina = agent.traits.get("stamina", 0)        # Default stamina
        speed = agent.traits.get("speed", 0)            # Default speed
        return (position, stamina, speed)  # Include speed in the state tuple


    def get_next_state(self, agent, action):
        """Calculate the next state for a given agent based on its action."""
        current_position = agent.traits.get("position", (0, 0))  # Default to (0, 0) if no position exists
        x, y = current_position

        # Example movement logic based on actions
        if action == "right":
            x = min(self.grid_size[0] - 1, x + 1)  # Move right
        elif action == "left":
            x = max(0, x - 1)  # Move left
        elif action == "down":
            y = (y + 1) % self.grid_size[1]  # Move down in zigzag
        elif action =='up':
            y = (y - 1) % self.grid_size[1] 
        elif action == "rest":
            pass  # Resting doesn't change position

        # Return the next state as a tuple
        return (x, y)


    def execute_action(self, agent, action):
        if action in ["left", "right", "up", "down"]:#:or action == "flee":
            agent.traits["stamina"] -= 1  # Reduce stamina
        elif action == "rest":
            agent.traits["stamina"] += 2  # Recover stamina
        agent.traits["stamina"] = max(0, agent.traits["stamina"])  # Prevent negative stamina


    def calculate_predator_fitness(self, predator):
        """Fitness is based on captures and stamina use."""
        return 10 if random.random() < 0.3 else -1  # Simplified fitness logic

    def calculate_prey_fitness(self, prey_agent):
        """Fitness is based on survival and stamina use."""
        return 5 if random.random() < 0.7 else -2  # Simplified fitness logic