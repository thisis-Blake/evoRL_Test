# Initialize environment
import random
from agents.Agent import Agent, Predator, Prey
from environments.Environment import Environment


env = Environment(grid_size=(10, 10), obstacles=[(3, 3), (5, 5)])
# Initialize populations
predators = [Predator(traits={"speed": random.uniform(1, 10), "stamina": random.uniform(1, 10), "position": (0, 0)}) for _ in range(10)]
prey = [Prey(traits={"speed": random.uniform(1, 10), "agility": random.uniform(1, 10), "position": (5, 5)}) for _ in range(20)]

# RL Loop (Within a Generation)
for t in range(100):  # 100 time steps
    env.step(predators, prey)

# Evolutionary Loop (Across Generations)
def evolve_population(agents):
    """Perform selection, crossover, and mutation."""
    # Select top-performing agents
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    top_agents = agents[:len(agents)//2]

    # Reproduce to form the next generation
    offspring = []
    for _ in range(len(agents) - len(top_agents)):
        parent1, parent2 = random.sample(top_agents, 2)
        child_traits = crossover_traits(parent1.traits, parent2.traits)
        mutate_traits(child_traits)
        offspring.append(type(parent1)(traits=child_traits))

    return top_agents + offspring

def crossover_traits(traits1, traits2):
    """Combine traits from two parents."""
    new_traits = {}
    for key in traits1:
        if isinstance(traits1[key], (int, float)):  # Handle numeric traits
            new_traits[key] = (traits1[key] + traits2[key]) / 2
        elif isinstance(traits1[key], tuple):  # Handle tuple traits (e.g., position)
            new_traits[key] = tuple((t1 + t2) / 2 for t1, t2 in zip(traits1[key], traits2[key]))
        else:
            new_traits[key] = traits1[key]  # Default to one parent's trait if unsupported type
    return new_traits


def mutate_traits(traits):
    """Apply random mutations to traits."""
    for key in traits:
        if isinstance(traits[key], (int, float)):  # Numeric traits
            if random.random() < 0.1:  # 10% mutation chance
                traits[key] += random.uniform(-0.5, 0.5)
        elif isinstance(traits[key], tuple):  # Tuple traits (e.g., position)
            if random.random() < 0.1:  # 10% mutation chance
                traits[key] = tuple(t + random.uniform(-0.5, 0.5) for t in traits[key])

# Evolve populations
predators = evolve_population(predators)
prey = evolve_population(prey)


for predator in predators:
    state = env.get_state(predator)
    action = predator.policy(state)
    reward = env.calculate_predator_fitness(predator)
    next_state = env.get_next_state(predator, action)
    predator.update_q_table(state, action, reward, next_state)

for prey_agent in prey:
    state = env.get_state(prey_agent)
    action = prey_agent.policy(state)
    reward = env.calculate_predator_fitness(prey_agent)
    next_state = env.get_next_state(prey_agent, action)
    prey_agent.update_q_table(state, action, reward, next_state)

print("Evolutionary loop completed:")
print(f"Top predator traits: {predators[0].traits}")
print(f"Top prey traits: {prey[0].traits}")

# print("Predator Policies After Evolution:")
# for predator in predators[:2]:  # Display policies for 2 sample predators
#     print('predator: ', predator.q_table,'\n')

# print("Prey Policies After Evolution:")
# for prey_agent in prey[:2]:  # Display policies for 2 sample prey
#     print('prey: ',prey_agent.q_table, '\n')

print("Updated Prey and Predator Q-Tables:")
for prey_state, predator_state in zip(prey[0].q_table.items(), predators[0].q_table.items()):
    prey_s, prey_actions = prey_state
    predator_s, predator_actions = predator_state
    print(f"PREY | State: {prey_s}, Actions: {prey_actions}")
    print(f"PREDATOR | State: {predator_s}, Actions: {predator_actions}",'\n')


