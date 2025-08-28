# Genetic Algorithm for Benchmark Function Optimization

This project provides a Python application with a graphical user interface (GUI) for visualizing and running a Genetic Algorithm (GA) to find the minimum value of seven different benchmark functions. It's designed to demonstrate the effectiveness of GAs on various types of optimization problems, from simple unimodal functions to complex, high-dimensional, multimodal landscapes.

This software was developed as a semester project for CSC528: Artificial Intelligence.

## 🚀 Features

* **Interactive GUI**: Easily select parameters and run the algorithm using a clean Tkinter interface.
* **Seven Benchmark Functions**: Test the GA on the following functions:
  1. Ackley
  2. Rosenbrock
  3. Rastrigin
  4. Shekel
  5. Sphere
  6. Schwefel
  7. Griewangk
* **Configurable Dimensions**: Run all functions in either 5 or 10 dimensions.
* **Real-time Results**: Watch the algorithm's progress as it displays the current generation, best fitness, and best solution vector.
* **Modular Codebase**: The project is structured with a clear separation between the GUI, the GA logic, and the benchmark functions, making it easy to understand and extend.

## 🛠️ Setup and Installation

To run this project, you will need **Python 3**. Using a virtual environment is highly recommended to keep dependencies isolated.

### 1. Clone or Download the Project

First, get the project files onto your local machine. This includes:
* `app.py`
* `genetic_algorithm.py`
* `benchmark_functions.py`
* `requirements.txt`

### 2. Create and Activate a Virtual Environment

Open your terminal or command prompt in the project directory and follow these steps.

* **Create the environment:**
  ```bash
  # On macOS/Linux
  python3 -m venv venv
  
  # On Windows
  python -m venv venv
  ```

* **Activate the environment:**
  ```bash
  # On macOS/Linux
  source venv/bin/activate
  
  # On Windows
  .\venv\Scripts\activate
  ```
  Your terminal prompt should now show `(venv)`.

### 3. Install Dependencies

With the virtual environment active, install the required packages using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

## ▶️ How to Run the Application

Once the setup is complete, you can start the application by running the `app.py` script from your terminal:
```bash
python app.py
```
The application window will open, and you can begin your experiments.

### Using the GUI

1. **Select a Benchmark Function** from the dropdown menu.
2. **Choose the Dimension** (5 or 10).
3. (Optional) Adjust the **Population Size** and **Max Generations**.
4. Click the **Start** button to begin the optimization.
5. Click the **Stop** button at any time to halt the process.
