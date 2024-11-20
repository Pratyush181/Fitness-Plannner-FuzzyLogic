import tkinter as tk
from tkinter import ttk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FitnessPlanner:
    def __init__(self, master):
        self.master = master
        master.title("Fuzzy Logic Fitness Planner")
        master.geometry("600x900")

        # Create input widgets
        self.create_input_widgets()

        # Calculate Button
        calculate_btn = tk.Button(master, text="Generate Fitness Plan", command=self.generate_fitness_plan)
        calculate_btn.pack(pady=20)

        # Result Display
        self.result_text = tk.Text(master, height=20, width=70)
        self.result_text.pack(pady=10)

    def create_input_widgets(self):
        # Weight Input
        tk.Label(self.master, text="Weight (kg):").pack()
        self.weight_entry = tk.Entry(self.master)
        self.weight_entry.pack()

        # Age Input
        tk.Label(self.master, text="Age (years):").pack()
        self.age_entry = tk.Entry(self.master)
        self.age_entry.pack()

        # Fat Level
        tk.Label(self.master, text="Body Fat Percentage:").pack()
        self.fat_level = ttk.Combobox(self.master, values=[
            "Very Low (Below 10%)",
            "Low (10-15%)",
            "Medium (15-20%)",
            "High (20-25%)",
            "Very High (Above 25%)"
        ])
        self.fat_level.pack()

        # Muscle Level
        tk.Label(self.master, text="Muscle Level:").pack()
        self.muscle_level = ttk.Combobox(self.master, values=[
            "Very Low", "Low", "Medium", "High", "Very High"
        ])
        self.muscle_level.pack()

        # Endurance Level
        tk.Label(self.master, text="Endurance Level:").pack()
        self.endurance_level = ttk.Combobox(self.master, values=[
            "Very Low", "Low", "Medium", "High", "Very High"
        ])
        self.endurance_level.pack()

        # Goal
        tk.Label(self.master, text="Goal:").pack()
        self.goal = ttk.Combobox(self.master, values=[
            "Build Muscle", "Lose Fat", "Maintain", "Improve Endurance"
        ])
        self.goal.pack()

        # Preferred Workout Type
        tk.Label(self.master, text="Preferred Workout Type:").pack()
        self.workout_type = ttk.Combobox(self.master, values=[
            "Weight Training (Gym)", "BodyWeight Training (Calisthenics)"
        ])
        self.workout_type.pack()

    def fuzzy_fitness_system(self):
        # Fuzzy Input Variables
        fat = ctrl.Antecedent(np.arange(0, 101, 1), 'fat')
        muscle = ctrl.Antecedent(np.arange(0, 11, 1), 'muscle')
        endurance = ctrl.Antecedent(np.arange(0, 11, 1), 'endurance')

        # Fuzzy Output Variables
        daily_steps = ctrl.Consequent(np.arange(0, 15001, 1), 'daily_steps')
        calories = ctrl.Consequent(np.arange(1500, 4001, 1), 'calorie_intake')
        protein = ctrl.Consequent(np.arange(50, 251, 1), 'protein_intake')

        # Membership Functions
        # Fat Percentage
        fat['Very Low'] = fuzz.trimf(fat.universe, [0, 0, 10])
        fat['Low'] = fuzz.trimf(fat.universe, [5, 12.5, 15])
        fat['Medium'] = fuzz.trimf(fat.universe, [12, 20, 25])
        fat['High'] = fuzz.trimf(fat.universe, [20, 25, 30])
        fat['Very High'] = fuzz.trimf(fat.universe, [25, 35, 100])

        # Muscle and Endurance Levels
        levels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        muscle.automf(names=levels)
        endurance.automf(names=levels)

        # Define membership functions for output variables
        daily_steps['low'] = fuzz.trimf(daily_steps.universe, [0, 0, 5000])
        daily_steps['low-medium'] = fuzz.trimf(daily_steps.universe, [4000, 7500, 9000])
        daily_steps['medium'] = fuzz.trimf(daily_steps.universe, [8000, 10000, 12000])
        daily_steps['medium-high'] = fuzz.trimf(daily_steps.universe, [11000, 12500, 14000])
        daily_steps['high'] = fuzz.trimf(daily_steps.universe, [13000, 15000, 15000])

        calories['low'] = fuzz.trimf(calories.universe, [1500, 1500, 2000])
        calories['low-medium'] = fuzz.trimf(calories.universe, [1900, 2200, 2500])
        calories['medium'] = fuzz.trimf(calories.universe, [2400, 2750, 3000])
        calories['medium-high'] = fuzz.trimf(calories.universe, [2900, 3250, 3500])
        calories['high'] = fuzz.trimf(calories.universe, [3400, 4000, 4000])

        protein['low'] = fuzz.trimf(protein.universe, [50, 50, 100])
        protein['low-medium'] = fuzz.trimf(protein.universe, [90, 125, 150])
        protein['medium'] = fuzz.trimf(protein.universe, [140, 175, 200])
        protein['medium-high'] = fuzz.trimf(protein.universe, [190, 220, 250])
        protein['high'] = fuzz.trimf(protein.universe, [240, 250, 250])

        # Fuzzy Rules for Daily Steps
        rule_steps = [
            ctrl.Rule(endurance['Very High'], daily_steps['high']),
            ctrl.Rule(endurance['High'], daily_steps['medium-high']),
            ctrl.Rule(endurance['Medium'], daily_steps['medium']),
            ctrl.Rule(endurance['Low'], daily_steps['low-medium']),
            ctrl.Rule(endurance['Very Low'], daily_steps['low'])
        ]

        # Fuzzy Rules for Calories
        rule_calories = [
            ctrl.Rule(muscle['Very High'] & fat['Very Low'], calories['high']),
            ctrl.Rule(muscle['High'] & fat['Low'], calories['medium-high']),
            ctrl.Rule(muscle['Medium'] & fat['Medium'], calories['medium']),
            ctrl.Rule(muscle['Low'] & fat['High'], calories['low-medium']),
            ctrl.Rule(muscle['Very Low'] & fat['Very High'], calories['low'])
        ]

        # Fuzzy Rules for Protein
        rule_protein = [
            ctrl.Rule(muscle['Very High'], protein['high']),
            ctrl.Rule(muscle['High'], protein['medium-high']),
            ctrl.Rule(muscle['Medium'], protein['medium']),
            ctrl.Rule(muscle['Low'], protein['low-medium']),
            ctrl.Rule(muscle['Very Low'], protein['low'])
        ]

        # Create Control Systems
        steps_ctrl = ctrl.ControlSystem(rule_steps)
        calories_ctrl = ctrl.ControlSystem(rule_calories)
        protein_ctrl = ctrl.ControlSystem(rule_protein)

        return {
            'steps': ctrl.ControlSystemSimulation(steps_ctrl),
            'calories': ctrl.ControlSystemSimulation(calories_ctrl),
            'protein': ctrl.ControlSystemSimulation(protein_ctrl)
        }

    def generate_fitness_plan(self):
        # Input validation
        try:
            weight = float(self.weight_entry.get())
            age = int(self.age_entry.get())
        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter valid weight and age!")
            return

        if not all([
            self.fat_level.get(),
            self.muscle_level.get(),
            self.endurance_level.get(),
            self.goal.get(),
            self.workout_type.get()
        ]):
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please fill all fields!")
            return

        # Fuzzy mapping
        level_map = {
            "Very Low": 2,
            "Low": 4,
            "Medium": 6,
            "High": 8,
            "Very High": 10
        }

        fat_map = {
            "Very Low (Below 10%)": 5,
            "Low (10-15%)": 12.5,
            "Medium (15-20%)": 20,
            "High (20-25%)": 25,
            "Very High (Above 25%)": 35
        }

        # Run fuzzy system
        systems = self.fuzzy_fitness_system()

        # Compute inputs
        systems['steps'].input['endurance'] = level_map[self.endurance_level.get()]
        systems['calories'].input['muscle'] = level_map[self.muscle_level.get()]
        systems['calories'].input['fat'] = fat_map[self.fat_level.get()]
        systems['protein'].input['muscle'] = level_map[self.muscle_level.get()]

        # Compute results
        systems['steps'].compute()
        systems['calories'].compute()
        systems['protein'].compute()

        # Workout Plan Generation
        workout_plan = self.generate_workout_plan()

        # Calculate BMR and additional details
        bmr = self.calculate_bmr(weight, age)

        # Display Results
        result = f"""Fitness Plan Details:
Weight: {weight} kg | Age: {age} years
Goal: {self.goal.get()} ({self.workout_type.get()})

Daily Steps Goal: {int(systems['steps'].output['daily_steps'])} steps
Daily Calories: {int(systems['calories'].output['calorie_intake'])} calories
Daily Protein: {int(systems['protein'].output['protein_intake'])} grams
Base Metabolic Rate (BMR): {int(bmr)} calories

Weekly Workout Plan:
{workout_plan}
"""

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def calculate_bmr(self, weight, age):
        # Using Mifflin-St Jeor Equation (assuming male, can be modified)
        return 10 * weight + 6.25 * 170 - 5 * age + 5

    def generate_workout_plan(self):
        goal = self.goal.get()
        workout_type = self.workout_type.get()

        # Simplified workout plan generation
        if goal == "Build Muscle":
            if workout_type == "Weight Training (Gym)":
                return """
- Monday: Chest and Triceps
- Tuesday: Back and Biceps
- Wednesday: Legs and Core
- Thursday: Rest/Active Recovery
- Friday: Shoulders and Arms
- Saturday: Full Body Compound Movements
- Sunday: Rest
"""
            else:  # Bodyweight
                return """
- Monday: Push (Chest, Triceps)
- Tuesday: Pull (Back, Biceps)
- Wednesday: Legs and Core
- Thursday: Rest/Active Recovery
- Friday: Full Body Calisthenics
- Saturday: HIIT Bodyweight Workout
- Sunday: Rest
"""
        elif goal == "Lose Fat":
            return """
- Monday: High-Intensity Interval Training
- Tuesday: Full Body Resistance
- Wednesday: Cardio and Core
- Thursday: Rest/Active Recovery
- Friday: Circuit Training
- Saturday: Long Duration Cardio
- Sunday: Rest and Recovery
"""
        elif goal == "Maintain":
            return """
- Monday: Full Body Workout
- Tuesday: Cardio and Mobility
- Wednesday: Strength Training
- Thursday: Rest/Active Recovery
- Friday: Mixed Intensity Workout
- Saturday: Light Activity
- Sunday: Rest
"""
        else:  # Improve Endurance
            return """
- Monday: Long Steady State Cardio
- Tuesday: Interval Training
- Wednesday: Cross-Training
- Thursday: Rest/Active Recovery
- Friday: Hill or Resistance Cardio
- Saturday: Long Endurance Session
- Sunday: Rest and Recovery
"""


def main():
    root = tk.Tk()
    fitness_planner = FitnessPlanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()