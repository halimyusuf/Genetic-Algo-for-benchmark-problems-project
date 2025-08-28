# This file contains the implementation of the 7 benchmark functions.
# Each function takes a list or numpy array 'x' as input, representing a point
# in the search space, and returns a single floating-point value, which is
# the fitness or objective value to be minimized.

import numpy as np

# 1. Ackley Function
def ackley(x):
    """
    Ackley function. A complex multimodal function with many local minima.
    The global minimum is at f(0, 0, ..., 0) = 0.
    """
    n = len(x)
    sum1 = np.sum(np.square(x))
    sum2 = np.sum(np.cos(2 * np.pi * x))
    term1 = -20 * np.exp(-0.2 * np.sqrt(sum1 / n))
    term2 = -np.exp(sum2 / n)
    return term1 + term2 + 20 + np.e

# 2. Rosenbrock Function
def rosenbrock(x):
    """
    Rosenbrock function. A non-convex function with a narrow, parabolic-shaped
    global minimum valley.
    The global minimum is at f(1, 1, ..., 1) = 0.
    """
    return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

# 3. Rastrigin Function
def rastrigin(x):
    """
    Rastrigin function. A highly multimodal function with a regular pattern
    of local minima.
    The global minimum is at f(0, 0, ..., 0) = 0.
    """
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

# 4. Shekel Function
def shekel(x):
    """
    Shekel function. A multimodal function with several local minima.
    This implementation uses a standard set of parameters for the function.
    """
    m = 10
    # C and A are predefined matrices for the Shekel function
    C = np.array([4, 1, 8, 6, 3, 2, 5, 8, 6, 7])
    A = np.array([
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    ])
    
    # Ensure x is compatible with A for subtraction
    # We only use the first len(x) columns of A
    A_subset = A[:m, :len(x)]

    result = 0
    for i in range(m):
        term = np.sum((x - A_subset[i])**2)
        result -= 1 / (term + C[i])
    return result


# 5. Sphere Function
def sphere(x):
    """
    Sphere function. A simple, convex, and unimodal function.
    The global minimum is at f(0, 0, ..., 0) = 0.
    """
    return np.sum(np.square(x))

# 6. Schwefel Function
def schwefel(x):
    """
    Schwefel function. A complex multimodal function where the global minimum
    is far from the best local minima.
    The global minimum is near f(420.9687, ..., 420.9687).
    """
    n = len(x)
    return 418.9829 * n - np.sum(x * np.sin(np.sqrt(np.abs(x))))

# 7. Griewangk Function
def griewangk(x):
    """
    Griewangk function. A multimodal function with a product term that
    introduces dependencies between the variables.
    The global minimum is at f(0, 0, ..., 0) = 0.
    """
    sum_term = np.sum(x**2 / 4000)
    prod_term = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
    return sum_term - prod_term + 1

# Dictionary to easily access functions by name and their typical bounds
# These bounds are crucial for initializing the population within a reasonable search space.
FUNCTIONS = {
    "Ackley": {"func": ackley, "bounds": (-32.768, 32.768)},
    "Rosenbrock": {"func": rosenbrock, "bounds": (-5, 10)},
    "Rastrigin": {"func": rastrigin, "bounds": (-5.12, 5.12)},
    "Shekel": {"func": shekel, "bounds": (0, 10)},
    "Sphere": {"func": sphere, "bounds": (-5.12, 5.12)},
    "Schwefel": {"func": schwefel, "bounds": (-500, 500)},
    "Griewangk": {"func": griewangk, "bounds": (-600, 600)},
}