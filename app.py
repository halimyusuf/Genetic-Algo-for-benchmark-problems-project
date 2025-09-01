# This is the main file to run the application.
# It uses Tkinter to create the Graphical User Interface (GUI) and connects it
# to the Genetic Algorithm engine and the benchmark functions.

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

# Import the logic and functions from the other files
from benchmark_functions import FUNCTIONS
from genetic_algorithm import GeneticAlgorithm

class App(tk.Tk):
    """
    Main application class that creates and manages the GUI.
    """
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Genetic Algorithm for Benchmark Functions")
        self.geometry("800x600")
        self.configure(bg="#2E2E2E")

        # --- Style Configuration ---
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Arial", 12))
        self.style.configure("TButton", background="#4A4A4A", foreground="#FFFFFF", font=("Arial", 12, "bold"), borderwidth=0)
        self.style.map("TButton", background=[("active", "#6A6A6A")])
        self.style.configure("TCombobox", fieldbackground="#4A4A4A", background="#4A4A4A", foreground="#FFFFFF")
        self.style.configure("TEntry", fieldbackground="#4A4A4A", foreground="#FFFFFF")

        # --- Class Members ---
        self.ga_instance = None
        self.running = False
        self.generation_count = 0
        self.fitness_history = [] # To store fitness values for plotting

        # --- GUI Creation ---
        self._create_widgets()

    def _create_widgets(self):
        """Creates and arranges all the widgets in the main window."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Control Panel (Left Side) ---
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="ns")

        ttk.Label(control_frame, text="GA Controls", font=("Arial", 16, "bold")).pack(pady=(0, 10), anchor="w")

        # Function Selection
        ttk.Label(control_frame, text="Benchmark Function:").pack(anchor="w", pady=(10, 2))
        self.function_var = tk.StringVar(value=list(FUNCTIONS.keys())[0])
        function_menu = ttk.Combobox(control_frame, textvariable=self.function_var, values=list(FUNCTIONS.keys()), state="readonly")
        function_menu.pack(fill=tk.X)

        # Dimension Selection
        ttk.Label(control_frame, text="Dimension:").pack(anchor="w", pady=(10, 2))
        self.dimension_var = tk.StringVar(value="5")
        dimension_menu = ttk.Combobox(control_frame, textvariable=self.dimension_var, values=["5", "10"], state="readonly")
        dimension_menu.pack(fill=tk.X)
        
        # Other GA Parameters
        ttk.Label(control_frame, text="Population Size:").pack(anchor="w", pady=(10, 2))
        self.pop_size_var = tk.StringVar(value="100")
        ttk.Entry(control_frame, textvariable=self.pop_size_var).pack(fill=tk.X)

        ttk.Label(control_frame, text="Max Generations:").pack(anchor="w", pady=(10, 2))
        self.max_gen_var = tk.StringVar(value="500")
        ttk.Entry(control_frame, textvariable=self.max_gen_var).pack(fill=tk.X)

        # Control Buttons
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_ga)
        self.start_button.pack(pady=20, fill=tk.X, ipady=5)

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_ga, state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X, ipady=5)
        
        self.plot_button = ttk.Button(control_frame, text="Plot Convergence", command=self.plot_convergence, state=tk.DISABLED)
        self.plot_button.pack(pady=(10,0), fill=tk.X, ipady=5)


        # --- Results Display (Right Side) ---
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(results_frame, text="Results", font=("Arial", 16, "bold")).pack(pady=(0, 10), anchor="w")

        self.gen_label = ttk.Label(results_frame, text="Generation: 0", font=("Arial", 12))
        self.gen_label.pack(anchor="w")

        self.fitness_label = ttk.Label(results_frame, text="Best Fitness: N/A", font=("Arial", 12))
        self.fitness_label.pack(anchor="w", pady=5)

        ttk.Label(results_frame, text="Best Solution Vector:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 5))
        self.solution_text = tk.Text(results_frame, height=15, width=50, background="#1E1E1E", foreground="#D4D4D4", relief="flat", font=("Courier", 11))
        self.solution_text.pack(fill=tk.BOTH, expand=True)
        self.solution_text.insert(tk.END, "Waiting to start...")
        self.solution_text.config(state=tk.DISABLED)


    def start_ga(self):
        """Initializes and starts the Genetic Algorithm run."""
        try:
            func_name = self.function_var.get()
            dimension = int(self.dimension_var.get())
            pop_size = int(self.pop_size_var.get())
            
            self.ga_instance = GeneticAlgorithm(
                objective_func=FUNCTIONS[func_name]["func"],
                bounds=FUNCTIONS[func_name]["bounds"],
                dimension=dimension,
                pop_size=pop_size
            )

            # Reset state and update UI
            self.running = True
            self.generation_count = 0
            self.fitness_history.clear() # Clear history for the plot
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.plot_button.config(state=tk.DISABLED)
            
            # Start the GA loop
            self.run_ga_loop()

        except ValueError:
            messagebox.showerror("Input Error", "Population size and max generations must be valid integers.")

    def stop_ga(self):
        """Stops the Genetic Algorithm run."""
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.plot_button.config(state=tk.NORMAL) # Enable plot button when stopped


    def run_ga_loop(self):
        """The main loop that runs generations and updates the GUI."""
        if self.running and self.generation_count < int(self.max_gen_var.get()):
            best_solution, best_fitness = self.ga_instance.run_generation()
            self.fitness_history.append(best_fitness) # Add data for plot
            
            # Update GUI
            self.generation_count += 1
            self.gen_label.config(text=f"Generation: {self.generation_count}")
            self.fitness_label.config(text=f"Best Fitness: {best_fitness:.6f}")
            
            self.solution_text.config(state=tk.NORMAL)
            self.solution_text.delete("1.0", tk.END)
            solution_str = np.array2string(best_solution, formatter={'float_kind':lambda x: "%.4f" % x})
            self.solution_text.insert(tk.END, solution_str)
            self.solution_text.config(state=tk.DISABLED)
            
            # Schedule the next run
            self.after(1, self.run_ga_loop)
        else:
            if self.running: # If it finished without being stopped
                self.stop_ga()

    def plot_convergence(self):
        """Plots the fitness history of the last GA run."""
        if not self.fitness_history:
            messagebox.showinfo("No Data", "There is no fitness data to plot. Please run the GA first.")
            return

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(self.fitness_history, color='cyan', linewidth=2)
        
        # Style the plot to match the dark theme
        fig.patch.set_facecolor('#2E2E2E')
        ax.set_facecolor('#2E2E2E')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('#2E2E2E')
        ax.spines['right'].set_color('#2E2E2E')
        
        # Set labels and title
        ax.set_xlabel("Generation", color='white', fontsize=12)
        ax.set_ylabel("Best Fitness", color='white', fontsize=12)
        
        func_name = self.function_var.get()
        dim = self.dimension_var.get()
        title = f"GA Convergence for {func_name} Function ({dim}D)"
        ax.set_title(title, color='white', fontsize=16, weight='bold')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()

