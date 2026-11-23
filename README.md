# Sorting Algorithm Analyzer

A desktop application for visualizing and analyzing sorting algorithms.

The application allows users to run sorting algorithms on randomly generated arrays, observe their execution step by step, and compare their performance.

## Features

- **Sorting visualization** — watch sorting algorithms rearrange array elements in real time.
- **Custom input** — choose a sorting algorithm from a Python file.
- **Adjustable array size** — specify the number of elements to sort.
- **Execution speed control** — configure the delay between visualization steps.
- **Statistics** — track execution time and sorting operations.
- **Custom appearance** — switch between light and dark themes and customize bar colors.
- **Statistics settings** — choose which information is displayed during visualization.
- **SQLite database** — save and review previous sorting results.
- **Result management** — delete individual records or clear the database.

## Technologies

- Python
- PyQt6 — graphical user interface
- SQLite — result storage

## Installation

1. Clone the repository:
```text
git clone https://github.com/NoamXXxXxx/Sorting-Algoryhm-Analyser.git
```

3. Navigate to the project directory:
```text
cd Sorting-Algoryhm-Analyser
```

5. Install the required dependency:
```text
pip install PyQt6
```

## Running the Application

Run the following command from the project directory:
```text
python main.py
```

## Project Structure

```text
Sorting-Algoryhm-Analyser
│
├── sorting algorythms   # Sorting algorithm implementations
├── main.py              # Application entry point
├── ui.py                # Graphical interface
├── visualiser.py        # Sorting visualization
├── db.py                # SQLite database operations
├── database.db          # Database file (generated)
├── about.md             # Project information
└── README.md            # Documentation
```

## How It Works

1. Open the visualizer.
2. Select a Python file containing a sorting algorithm.
3. Enter the database record name.
4. Specify the array size and visualization delay.
5. Start the sorting process.
6. Observe the algorithm and its statistics.
7. Save and review the results in the database.

## Project Status
probably i will never update it 
Build 1.0
