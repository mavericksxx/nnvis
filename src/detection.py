import numpy as np
from .ui import SpectatorMode

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layers = []
        self.weights = []
        
        for i in range(len(layer_sizes)):
            layer = [{'activation': np.random.random() * 2 - 1} for _ in range(layer_sizes[i])]
            self.layers.append(layer)
            
            if i < len(layer_sizes) - 1:
                weight_matrix = np.random.randn(layer_sizes[i], layer_sizes[i+1])
                self.weights.append(weight_matrix)
    
    def feed_forward(self):
        for i in range(len(self.layers) - 1):
            current_activations = np.array([n['activation'] for n in self.layers[i]])
            next_activations = np.tanh(np.dot(current_activations, self.weights[i]))
            
            for j, activation in enumerate(next_activations):
                self.layers[i + 1][j]['activation'] = float(activation)

class Agent:
    def __init__(self, network):
        self.network = network
        self.fitness = 0.0

class EvolutionSimulation:
    def __init__(self):
        self.population_size = 50
        self.population = []
        self.generation = 0
        self.spectator = SpectatorMode()
        
        for _ in range(self.population_size):
            network = NeuralNetwork([5, 6, 6, 4])
            agent = Agent(network)
            self.population.append(agent)
    
    def evaluate_fitness(self):
        for agent in self.population:
            agent.fitness = np.random.random()
    
    def select_parents(self):
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        return sorted_population[:int(self.population_size * 0.2)]
    
    def create_offspring(self, parents):
        new_population = []
        new_population.extend(parents)
        
        while len(new_population) < self.population_size:
            parent = np.random.choice(parents)
            new_network = NeuralNetwork([5, 6, 6, 4])
            new_agent = Agent(new_network)
            new_population.append(new_agent)
        
        return new_population
    
    def run_generation(self):
        self.evaluate_fitness()
        parents = self.select_parents()
        self.population = self.create_offspring(parents)
        
        for agent in self.population:
            agent.network.feed_forward()
        
        self.generation += 1
        self.spectator.current_generation = self.generation
        self.spectator.top_performers = sorted(
            self.population,
            key=lambda x: x.fitness,
            reverse=True
        )[:10]
        
        return {
            'generation': self.generation,
            'best_fitness': max(agent.fitness for agent in self.population),
            'average_fitness': np.mean([agent.fitness for agent in self.population])
        } 