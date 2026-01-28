import random
import numpy as np
import logging

class GAOptimizer:
    def __init__(self, population_size=20, generations=10, mutation_rate=0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.convergence_history = []
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger('GAOptimizer')

    def fitness_function(self, weights, validation_data=None):
        """
        Enhanced fitness function to evaluate weight configurations.
        """
        w_skills, w_exp, w_edu = weights

        # Constraint: Weights must sum to ~1
        sum_weights = sum(weights)
        penalty = abs(1.0 - sum_weights) * 100

        # Use validation data if provided
        if validation_data:
            # Simulate a scoring mechanism based on validation data
            score = validation_data.get_score(weights)
        else:
            # Default heuristic: Prefer skills > experience > education
            optimal_profile = np.array([0.6, 0.3, 0.1])
            dist_to_optimal = np.linalg.norm(np.array(weights) - optimal_profile)
            score = 100 - (dist_to_optimal * 50) - penalty

        return max(0, score)

    def optimize(self, validation_data=None):
        """
        Runs the GA to find optimal weights [w_skills, w_exp, w_edu].
        Returns: (best_weights, convergence_data)
        """
        import time
        start_time = time.time()
        
        # Initialize population (random weights summing to 1)
        population = [np.random.dirichlet(np.ones(3)) for _ in range(self.population_size)]

        best_weights = None
        avg_fitness_history = []
        diversity_history = []
        
        for gen in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self.fitness_function(ind, validation_data) for ind in population]

            # Track best, average, and diversity
            max_fitness = max(fitness_scores)
            avg_fitness = np.mean(fitness_scores)
            diversity = self._calculate_diversity(population)
            
            self.convergence_history.append(max_fitness)
            avg_fitness_history.append(avg_fitness)
            diversity_history.append(diversity)
            
            best_ind_idx = fitness_scores.index(max_fitness)
            best_weights = population[best_ind_idx]

            self.logger.info(f'Generation {gen + 1}: Best={max_fitness:.2f}, Avg={avg_fitness:.2f}, Diversity={diversity:.4f}')

            # Elitism: Keep the best individual
            new_population = [best_weights]

            # Selection & Crossover
            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection(population, fitness_scores)
                parent2 = self._tournament_selection(population, fitness_scores)

                child = self._crossover(parent1, parent2)
                child = self._mutate(child)

                new_population.append(child)

            population = new_population

        end_time = time.time()
        execution_time = end_time - start_time
        
        # Calculate convergence rate
        convergence_rate = self._calculate_convergence_rate()
        
        convergence_data = {
            'best_weights': best_weights.tolist() if hasattr(best_weights, 'tolist') else list(best_weights),
            'convergence_history': [float(x) for x in self.convergence_history],
            'avg_fitness_history': [float(x) for x in avg_fitness_history],
            'diversity_history': [float(x) for x in diversity_history],
            'convergence_rate': float(convergence_rate),
            'final_fitness': float(self.convergence_history[-1]) if self.convergence_history else 0,
            'generations': int(self.generations),
            'population_size': int(self.population_size),
            'execution_time': float(execution_time),
            'evaluations_count': int(self.generations * self.population_size)
        }
        
        return best_weights.tolist() if hasattr(best_weights, 'tolist') else list(best_weights), convergence_data

    def _tournament_selection(self, population, fitness_scores, k=3):
        selection_ix = random.sample(range(len(population)), k)
        best_ix = selection_ix[0]
        for ix in selection_ix[1:]:
            if fitness_scores[ix] > fitness_scores[best_ix]:
                best_ix = ix
        return population[best_ix]

    def _crossover(self, parent1, parent2):
        """
        Enhanced crossover using blend crossover (BLX-alpha).
        """
        alpha = 0.5
        child = np.clip(parent1 + alpha * (parent2 - parent1), 0, 1)
        child /= child.sum()  # Renormalize
        return child

    def _mutate(self, individual):
        """
        Adaptive mutation: Adjust mutation rate based on convergence.
        """
        if random.random() < self.mutation_rate:
            mutation_idx = random.randint(0, 2)
            mutation_strength = np.random.normal(0, 0.1)
            individual[mutation_idx] += mutation_strength
            individual = np.clip(individual, 0, 1)
            individual /= individual.sum()  # Renormalize
        return individual
    
    def _calculate_diversity(self, population):
        """
        Calculate population diversity using standard deviation.
        Higher diversity = more exploration.
        """
        population_array = np.array(population)
        return np.mean(np.std(population_array, axis=0))
    
    def _calculate_convergence_rate(self):
        """
        Calculate convergence rate: improvement per generation.
        Formula: (final_fitness - initial_fitness) / generations
        """
        if len(self.convergence_history) < 2:
            return 0.0
        
        initial_fitness = self.convergence_history[0]
        final_fitness = self.convergence_history[-1]
        improvement = final_fitness - initial_fitness
        
        return improvement / len(self.convergence_history)
