# Quick Start Guide - Food Delivery Optimizer

## Implementations

This project includes two implementations of the same algorithm:

| Implementation | File | Requirements |
|----------------|------|--------------|
| **Python** | `food_delivery_optimizer.py` | Python 3.6+ (standard library only) |
| **C++** | `food_delivery_optimizer.cpp` | C++ compiler (g++, clang++, or MSVC); C++11+ |

Sample run screenshots (WSL):
- **`output_python_run_wsl.png`** – Python implementation
- **`output_cpp_run_wsl.png`** – C++ implementation
- **`output_grid_visualizer.png`** – Grid visualization tool

## Installation

**Python:** No installation required; uses only the Python standard library.

**C++:** Install a C++ compiler (e.g. `g++` on Linux/WSL, or Visual Studio on Windows).

## Running the Program

### Step 1: Prepare Input File
Create a text file with your test cases following this format:

```
<number_of_test_cases>
<grid_size> <num_riders> <num_restaurants>
<restaurant_name> <location> <num_orders>
<order_name> <location> <time_limit>
...
```

### Step 2: Run the Optimizer

**Python:**
```bash
python food_delivery_optimizer.py input.txt
```

**C++ (Linux / WSL):**
```bash
g++ -o food_delivery_optimizer food_delivery_optimizer.cpp
./food_delivery_optimizer input.txt
```

**C++ (Windows):** Build the `.cpp` file in your IDE or with MSVC, then run the executable with the input file as argument.

Replace `input.txt` with your input file name.

### Step 3: View Results
The program will display:
- Test case details
- Restaurant and order information  
- Optimized routes for each rider (full path with every node)
- Total delivery time (sum of all rider times)

## Example

**Input file (sample.txt):**
```
1
5 2 2
BurgerPalace 10 2
Beef 7 5
Zinger 15 8
PizzaPlanet 18 1
Tikka 21 5
```

**Run:**
```bash
python food_delivery_optimizer.py sample.txt
```

**Output:**
```
============================================================
Test Case 1
============================================================
Grid Size: 5x5
Number of Riders: 2
...

Optimized Routes:
------------------------------------------------------------
Rider 1: 10 (BurgerPalace) -> 15 (Zinger) -> ... -> 7 (Beef) = 5 time units
Rider 2: 18 (PizzaPlanet) -> 17 -> 16 -> 21 (Tikka) = 3 time units
Total: 8 time units
```

For full sample runs, see **`output_python_run_wsl.png`** (Python) and **`output_cpp_run_wsl.png`** (C++).

## Understanding the Grid

Nodes are numbered 1 to N² in a 5×5 grid:

```
 1  2  3  4  5
 6  7  8  9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
```

- Node numbering goes left to right, top to bottom
- Adjacent nodes are connected (up, down, left, right)
- Each edge takes 1 unit of time to travel

## Grid Visualization Tool

Use the included visualization tool to understand node positions:

```bash
python grid_visualizer.py
```

This shows marked nodes and calculates distances for the test cases. A sample run is captured in **`output_grid_visualizer.png`**.

## Common Issues

### "File not found" Error
**Solution:** Ensure the input file path is correct
```bash
# Check if file exists
ls input.txt

# Use absolute path if needed
python food_delivery_optimizer.py /full/path/to/input.txt
```

### "Invalid input format" Error
**Solution:** Check your input file format:
- Ensure no missing values
- Verify locations are within grid bounds (1 to N²)
- Check that all values are integers

### No Routes Generated
**Possible causes:**
- Time constraints too tight (orders can't be delivered in time)
- Location validation failed (location > N²)

## Input Validation

The program validates:
✓ File exists and is readable
✓ Positive grid size, rider count, restaurant count
✓ Locations within grid bounds (1 to N²)
✓ Non-negative time limits
✓ Complete data for all restaurants and orders

## Testing Your Solution

1. **Start with simple test cases** (3×3 grid, 1 rider, 1 restaurant)
2. **Gradually increase complexity** (larger grids, more riders)
3. **Test edge cases:**
   - Single rider with multiple restaurants
   - Multiple riders with single restaurant
   - Tight time constraints
   - Orders at grid corners

## Sample Test Cases Included

- `input.txt` - Basic test cases from problem statement
- `test_input.txt` - Comprehensive test suite with 4 different scenarios

## Algorithm Overview

The optimizer uses a **Greedy Assignment with Nearest Neighbor** approach:

1. **Sort orders by time limit** (urgent orders first)
2. **Assign to best rider** (minimum additional time)
3. **Build routes** using nearest neighbor heuristic
4. **Group by restaurant** for efficiency

This provides near-optimal solutions in polynomial time.

## Performance

- **Time Complexity:** O(I × R × O × N²)
  - I = riders, R = restaurants, O = orders, N = grid size
- **Space Complexity:** O(N² + R + O + I×O)

Scales well for typical delivery scenarios:
- 10×10 grid: < 1 second
- 20×20 grid with 50 orders: < 5 seconds

## Getting Help

If you encounter issues:

1. Check input file format matches specification
2. Verify all locations are valid node numbers
3. Ensure time constraints are reasonable
4. Review error messages for specific problems

## Advanced Usage

### Batch Processing
Process multiple input files:
```bash
for file in test_*.txt; do
    python food_delivery_optimizer.py "$file" > "${file%.txt}_output.txt"
done
```

### Redirecting Output
Save results to file:
```bash
python food_delivery_optimizer.py input.txt > results.txt
```

### Comparing Solutions
Run with different rider counts to find optimal configuration.

## Next Steps

1. ✓ Run provided examples
2. ✓ Create your own test cases
3. ✓ Experiment with different grid sizes
4. ✓ Test edge cases
5. ✓ Analyze route optimality

## Support Files

- `food_delivery_optimizer.py` - Main program (Python)
- `food_delivery_optimizer.cpp` - Main program (C++)
- `output_python_run_wsl.png` - Screenshot of Python run on WSL
- `output_cpp_run_wsl.png` - Screenshot of C++ run on WSL
- `output_grid_visualizer.png` - Screenshot of grid visualizer on WSL
- `input.txt` - Sample input
- `test_input.txt` - Comprehensive tests
- `grid_visualizer.py` - Grid visualization tool
- `README.md` - Full documentation
- `QUICKSTART.md` - This file

---

**Happy Optimizing! 🚴‍♂️📦**
