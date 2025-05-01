# 🚗 EV Charging Station Optimization Thesis

This repository contains the code, data, and experiments for my Master's thesis titled:  
**"Comparison Analysis of Optimization Methods for the Location of Electric Vehicles Charging Stations in Urban Areas"**  
The goal is to optimize the placement of EV charging stations using heuristic methods and simulation-based demand modeling.

## 📘 Abstract

The growing concern over environmental sustainability has accelerated the adoption of electric vehicles, driving the increasing demand for reliable and efficient EV charging infrastructure. This study investigates and compares electric vehicle charging station placement optimization using three metaheuristic algorithms: genetic algorithm, particle swarm optimization, and simulated annealing. A demand simulation model based on a population distribution analysis is used to estimate the demand for charging stations. The optimization problem is formulated as a weighted sum of key objectives, including installation cost, spatial coverage, charging speed, and reducing negative impacts on the power grid. Experiments were conducted using real road network data, and the algorithm's performance was evaluated in terms of solution quality and convergence behavior. The results indicate that particle swarm optimization and genetic algorithm are highly effective in finding optimal solutions. In comparison, the simulated annealing algorithm proved to be less effective than the other mentioned methods for addressing this problem. The results highlight each method's performance characteristics in the charging infrastructure optimization field.
## 🗂️ Project Structure
├── configs/ \
│ ├── experiments/     # parameters for experiments\
│ ├── params.yaml      # baseline parameters\
├── experiments/\
│ ├── exp...       # saved results of the experiments\
├── src/      # Source code for optimization, simulation, and analysis \
│ ├── data/      # City graph, distance matrix, population, regions, substantions\
│ ├── optimization/     # GA, PSO, SA implementations \
│ ├── simulation/       # Charging demand simulation model\
│ ├── evaluation/        # Objective function\
├── ga_experiments.ipynb       # Running experiments and their visualization for the GA algorithm\
├── pso_experiments.ipynb      # Running experiments and their visualization for the PSO algorithm\
├── sa_experiments.ipynb       # Running experiments and their visualization for the SA algorithm\
├── requirements.txt     # Python dependencies \
└── README.md

## ⚙️ Features

- 🧬 **Genetic Algorithm (GA)** with customizable mutation/selection rates
- 🕊️ **Particle Swarm Optimization (PSO)** with convergence tracking
- 🔥 **Simulated Annealing (SA)** with flexible temperature schedules
- 📍 **Multi-objective Optimization** combining:
  - Installation cost
  - Average user distance to station
  - Average time required to charge 1kWh
  - Total distance from charging stations to closest power substations
- **Charging Demand Simulation** of EV demand using population data and value of EV per capita
