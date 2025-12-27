# Habit Tracker CLI (Python)

This project is a **Command Line Interface (CLI) Habit Tracker** developed in Python as a learning exercise to practice (OOFP)
Object Oriented and Functional Programming.

The application allows users to create habits, track their completion over time, analyse performance metrics, and simulate accelerated time for testing purposes.

The main objective of this project is to demonstrate fundamental software engineering concepts such as modular design, object-oriented programming, data persistence, and user interaction via a CLI.

-----

## Features 

- Creation of habits with:
  - name
  - description
  - target frequency (in days)
- Incrementing habits when completed
- Automatic tracking of:
  - run streaks
  - number of attempts
- Analytical functions:
  - longest historical run streak
  - ranking of habits by performance
  - identification of worst-performing habits
- Simulated time engine for accelerated testing
- Persistent storage using CSV files
- Interactive command-line interface using `questionary`

-----

## Core Concepts

### Runstreak
A **runstreak** represents the number of consecutive times a habit
has been maintained within its defined frequency.

### Attempts
An **attempt** is increased every time a habit is broken
(i.e. completed after its allowed frequency).

Attempts are stored as an **accumulated counter**.

### Simulated Time
The application includes a `TimeEngine` that simulates time passing
faster than real time, allowing testing of habits that require
days or weeks.

-----

## How to Run

### Requirements
- Python 3.10+
- Required libraries:
- `questionary` – used for interactive command-line prompts
- `pandas` – used for tabular data handling and display

Install dependencies:
```bash
pip install questionary pandas
