# SMWT_GA
Genetic Algorithm to solve the Single Machine Weighted Tardiness Problem

The single-machine total weighted tardiness problem can be stated as follows. Each of n jobs is to be processed without interruption on a single machine that can handle no more
than one job at a time. Job j becomes available for processing at time zero, requires an uninterrupted positive processing time p(j) on the machine, has a positive weight w(j), and has a due date d(j) by which it should ideally be finished. For a given processing order of the jobs, the earliest completion time C(j) and the tardiness T(j) = max {C(j)-d(j),0} of job j can readily be computed. The problem is to find a processing order of the jobs with minimum total weighted tardiness.

The Genetic Algorithm works as follows :

Individual: 
  A list of n(total jobs) numbers from 0 to n-1. The order of jobs in the list is the order in which the jobs are processed.
  
Population: 
  A set of 10 individuals.
  
Fitness: 
  The total weighted tardiness of each state multiplied by -1 to convert it into a maximization of fitness problem. If there are unprocessed jobs,the fitness of this individual is -∞.
  
Selection: 
  An individual is selected for cross-over with a probability of -1/(fitness of individual). An individual with higher fitness i.e lower total weighted tardiness is selected with a higher probability.
  
Crossover: 
  A total of 10 pairs are selected for crossover operation, resulting in 2 offsprings per each pair. The offspring with highest fitness per pair is added to the new population. The crossover operation involves randomly selecting an index and combining the 2 different parts of the 2 parents.
  
Mutate: 
  The probability of mutation for each individual is 0.1. The mutation operation is randomly swapping 2 values of an individual.

Population Initialization:
    Methods of generating each individual in the population:
    
        1. Ascending order of Weighted Modified Due Date
        2. Weighted Shortest Job First
        3. Earliest Deadline First
        4. Moore-Hodgson Method: Minimal number of jobs with positive tardiness
        5. Ascending order of (due_time*processing_time/weight) of each job
     
  The remaining 5 individuals are generated randomly.

Termination of Execution:
    Each run of the genetic algorithm involves 10,000 recombination operations. The execution is halted if the fitness value reaches 0 (maximum possible value as total tardiness     cannot be negative).
    For each instance, the genetic algorithm is run 5 times (mimicking random restart) and the best output out of these runs is reported.
