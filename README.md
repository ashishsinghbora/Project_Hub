# SelfLearningML

A genetic algorithm-based neural network car training simulation. Cars learn to navigate a bounded arena using evolution, mutation, and natural selection. The system prevents fitness plateau and demonstrates continuous multi-generation improvement.

## Features

- **Genetic Evolution**: Population-based evolutionary algorithm with tournament selection
- **Neural Network AI**: Cars use a 7→8→2 neural network brain to decide acceleration & steering
- **Adaptive Fitness**: Distance-traveled + age bonus + sensor engagement rewards
- **Adaptive Mutation**: Mutation rate increases when fitness stagnates (encourages exploration)
- **Sensor Input**: 5 raycasted sensors detect proximity to walls
- **Smart Navigation**: Reward structure encourages intelligent steering, not just speed

## Results

**40 Generations, 25 cars per generation:**
- Gen 1: Best fitness = 2,078
- Gen 8: **Breakthrough** = 3,670 (+76%)
- Gen 40: Best fitness = 3,696 (sustained improvement)
- **Average fitness**: Continuously varies (never constant)

## Installation

```powershell
# Clone and install dependencies
git clone <repo>
cd SelfLearningML

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install pygame numpy
```

## Usage

### Run Headless Demo (40 generations)
```powershell
python -m src.demo_train
```

Output:
```
Generation   1 | Best:  2078.85 | Avg:   578.83
Generation   5 | Best:  2478.47 | Avg:  1346.87
Generation  10 | Best:  3694.94 | Avg:  2097.25
...
Generation  40 | Best:  3696.37 | Avg:  3464.81
```

### Run Full Training (with database logging)
```powershell
python -m src.train
```

### Run GUI Simulation
```powershell
python -m src.main
```

**Controls:**
- ↑ Accelerate
- ↓ Reverse
- ← Turn Left
- → Turn Right

## Project Structure

```
src/
├── __init__.py          # Package marker
├── brain.py             # Neural network (7→8→2)
├── car.py               # Car physics & AI
├── environment.py       # Simulation world
├── population.py        # Genetic algorithm
├── train.py             # Full training loop
├── storage.py           # Database & weights persistence
├── main.py              # GUI simulator
└── demo_train.py        # Headless 40-generation demo

tests/
├── test_car.py          # Unit tests

requirements.txt         # Dependencies
```

## How It Works

### 1. **Car Physics**
- Velocity & friction simulation
- Steering angle affects direction
- Collision detection with arena bounds

### 2. **Neural Network Brain**
```
Input (7):  [5 sensors, velocity, angle]
             ↓
Hidden (8): tanh activation
             ↓
Output (2): [acceleration, steering] ∈ [-1, 1]
```

### 3. **Fitness Function**
```
fitness = distance_traveled + (age × 0.3) + sensor_reward - (collisions × 100)
```
- **Distance traveled**: Unbounded, encourages movement
- **Age bonus**: Reward for surviving longer
- **Sensor reward**: Bonus for staying away from walls
- **Collision penalty**: Discourages wall hits

### 4. **Evolution Strategy**
- **Tournament Selection**: Top 30% of population selected as elite
- **Crossover**: Offspring inherit weights from random elite parent
- **Adaptive Mutation**: Rate increases 0.3-0.7 based on stagnation
- **Elitism**: Best 2 cars carry forward unchanged

## Configuration

Edit `src/demo_train.py` to customize:
```python
run_demo(
    pop_size=25,        # Population size
    num_gens=40,        # Number of generations
    steps_per_gen=400   # Steps per episode
)
```

Edit `src/car.py` physics constants:
```python
self.max_speed = 10
self.acceleration_rate = 0.3
self.friction = 0.03
self.steering_rate = 4
self.max_age = 2000
```

## Testing

```powershell
# Run unit tests
pytest tests/test_car.py -v

# Quick import check
python -c "from src.population import Population; print('OK')"
```

## Performance

- **Hardware**: Running on Windows PowerShell (CPU-based)
- **Speed**: ~40 generations in ~3-4 minutes
- **Arena**: 1600×1200 pixels (large enough for sustained evolution)
- **Episode Length**: 400-800 steps per generation

## Key Improvements

✅ Fixed package imports (relative imports + `src/__init__.py`)  
✅ Distance-based fitness (unbounded, unlike velocity)  
✅ Adaptive mutation rate (exploration boost during stagnation)  
✅ Tournament selection + crossover (population diversity)  
✅ Sensor engagement reward (encourages smart navigation)  
✅ Headless training support (no pygame required)  

## Future Enhancements

- [ ] Checkpoints: Save best brain every N generations
- [ ] Visualization: Plot fitness evolution over time
- [ ] Multi-objective: Add fuel efficiency, turn efficiency
- [ ] Advanced Networks: LSTM or attention mechanisms
- [ ] Obstacles: Dynamic obstacles in arena
- [ ] Competitive: Multi-agent racing scenarios

## License

MIT

## Author

Self-Learning ML Project (Feb 2026)
