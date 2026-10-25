# 4200-Project2

## Overview

This project implements two local search algorithms to solve the n-queen problem:

- Steepest-ascent hill climbing (no sideways moves)
- Genetic algorithm

The program supports:

- Solving n-queen problems for n = 8, 12, 16
- Running multiple random instances for statistical analysis
- Reporting success rate, average steps/generations, and runtime
- Printing sample solved board configurations in grid format

---

## Structure

```bash
CS4200_P2/
│
├── hillclimbing.py     # Steepest-ascent hill climbing implementation (table + 3 samples)
├── genetic.py          # Genetic algorithm implementation (exp. summary + 3 samples)
├── README.md
└── Report.pdf

```

---

## How to Run the Program

```bash
python hillclimbing.py   # Run to see the result table for 200 instances which includes success rate, avg steps, avg steps (solved), avg time in addition to 3 sample outputs for each n
python genetic.py        # Run to see success rate, avg generation and avg runtime for 10 instances and 3 solved sample outputs for each n
```
