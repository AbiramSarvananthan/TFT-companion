# Import necessary modules
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk  # For themed Tkinter widgets
import csv  # For reading CSV files

# Function to load meta builds from a CSV file
def load_meta_builds(filename):
    builds = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                builds.append(row)
        return builds
    except FileNotFoundError:
        return []

# Function to load trait names from a text file
def load_trait_names(filename):
    try:
        with open(filename, 'r') as file:
            trait_names = [line.strip().lower() for line in file.readlines()]
        return trait_names
    except FileNotFoundError:
        return []

# Function to search for a trait in the list of builds
def search_trait_in_builds(trait, builds):
    results = []
    trait = trait.lower()
    for build in builds:
        if trait in build['Trait'].lower():
            results.append(build)
    return results

# Load the meta builds from the CSV file
builds = load_meta_builds('metaBuildsFile.csv')

# Load the trait names from the text file
trait_names = load_trait_names('traitNames.txt')

# Create the main window
window = ttk.Window(themename='darkly')
window.title('Tft Companion App')
window.geometry('1980x1080')

# Create a notebook to switch between different pages
notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
main_frame = ttk.Frame(notebook)
odds_frame = ttk.Frame(notebook)

notebook.add(main_frame, text="Meta Builds")
notebook.add(odds_frame, text="TFT Odds Calculator")

# Main Frame Widgets (Meta Builds)
label = ttk.Label(main_frame, text="Enter Trait Name:")
label.pack(pady=5)

trait_entry = ttk.Entry(main_frame, width=30)
trait_entry.pack(pady=10)

output_text = ScrolledText(main_frame, width=100, height=50, wrap=WORD)
output_text.pack()

def search_trait():
    trait = trait_entry.get().lower()
    if trait in trait_names:
        results = search_trait_in_builds(trait, builds)
        output_text.delete(1.0, tk.END)
        bullet_point = "\u2192"

        if results:
            for i, result in enumerate(results):
                output_text.insert(tk.END, f"Build {i+1}:\n", 'title')
                output_text.insert(tk.END, "\n")
                output_text.insert(tk.END, f"Buildname: {result['Buildname']}\n", 'buildname_title')
                output_text.insert(tk.END, f"Trait: {result['Trait']}\n", 'trait_title')
                output_text.insert(tk.END, f"Difficulty: {result['Difficulty']}\n", 'difficulty_title')
                output_text.insert(tk.END, f"Rank: {result['Rank']}\n", 'rank_title')
                
                champion_list = result['Champions'].split(',')
                item_list = result['Items'].split(',')
                augment_list = result['Augments'].split(',')
                step_list = result['Steps'].split(',')

                output_text.insert(tk.END, "Champions:\n", 'champions_title')
                for champion in champion_list:
                    output_text.insert(tk.END, f"{bullet_point} {champion.strip()}\n")

                output_text.insert(tk.END, "Items:\n", 'items_title')
                for item in item_list:
                    output_text.insert(tk.END, f"{bullet_point} {item.strip()}\n")

                output_text.insert(tk.END, "Augments:\n", 'augments_title')
                for augment in augment_list:
                    output_text.insert(tk.END, f"{bullet_point} {augment.strip()}\n")

                output_text.insert(tk.END, "Steps:\n", 'steps_title')
                for step in step_list:
                    output_text.insert(tk.END, f"{bullet_point} {step.strip()}\n")

                if i < len(results) - 1:
                    output_text.insert(tk.END, "\n" + "-" * 80 + "\n\n")

        else:
            output_text.insert(tk.END, f"No builds found for trait '{trait}'.")

        output_text.tag_configure('title', font=('Helvetica', 12, 'bold'), underline=True)
        output_text.tag_configure('buildname_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('trait_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('difficulty_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('rank_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('champions_title', font=('Helvetica', 10, 'bold'), foreground='red')
        output_text.tag_configure('items_title', font=('Helvetica', 10, 'bold'), foreground='brown')
        output_text.tag_configure('augments_title', font=('Helvetica', 10, 'bold'), foreground='cyan')
        output_text.tag_configure('steps_title', font=('Helvetica', 10, 'bold'), foreground='magenta')

    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"'{trait}' is not a valid trait name.")

search_button = ttk.Button(main_frame, text="Search", command=search_trait, state='disabled')
search_button.pack(pady=10)

def check_entry(event):
    if trait_entry.get():
        search_button['state'] = 'normal'
    else:
        search_button['state'] = 'disabled'

trait_entry.bind('<KeyRelease>', check_entry)

# TFT Odds Calculator Widgets (Odds Frame)
odds_label_level = ttk.Label(odds_frame, text="Enter Level (2-11):")
odds_label_level.pack(pady=5)

level_entry = ttk.Entry(odds_frame, width=10)
level_entry.pack(pady=5)

odds_label_cost = ttk.Label(odds_frame, text="Enter Unit Cost (1-5):")
odds_label_cost.pack(pady=5)

cost_entry = ttk.Entry(odds_frame, width=10)
cost_entry.pack(pady=5)

odds_label_purchased = ttk.Label(odds_frame, text="Enter Number of Units Purchased:")
odds_label_purchased.pack(pady=5)

purchased_entry = ttk.Entry(odds_frame, width=10)
purchased_entry.pack(pady=5)

odds_output = ScrolledText(odds_frame, width=50, height=10, wrap=WORD)
odds_output.pack(pady=10)

# Odds data
odds_data = {
    2: [100, 0, 0, 0, 0],
    3: [75, 25, 0, 0, 0],
    4: [55, 30, 15, 0, 0],
    5: [45, 33, 20, 2, 0],
    6: [30, 40, 25, 5, 0],
    7: [20, 33, 36, 10, 1],
    8: [18, 27, 32, 20, 3],
    9: [15, 20, 25, 30, 10],
    10: [5, 10, 20, 40, 25],
    11: [1, 2, 12, 50, 35]
}

# Pool sizes
pool_sizes = {
    1: 22,
    2: 20,
    3: 17,
    4: 10,
    5: 9
}

def calculate_odds():
    level = int(level_entry.get())
    cost = int(cost_entry.get())
    purchased = int(purchased_entry.get())

    if 2 <= level <= 11 and 1 <= cost <= 5:
        cost_index = cost - 1
        base_odds = odds_data[level][cost_index] / 100
        pool_size = pool_sizes[cost]
        remaining_units = pool_size - purchased

        if remaining_units <= 0:
            odds_output.delete(1.0, tk.END)
            odds_output.insert(tk.END, f"No units left in the pool for cost {cost}.")
        else:
            total_units = sum(pool_sizes.values())
            hit_rate = (remaining_units / pool_size) * base_odds * 100
            odds_output.delete(1.0, tk.END)
            odds_output.insert(tk.END, f"At level {level}, with {purchased} units purchased, the odds of finding a {cost}-cost unit are {hit_rate:.2f}%.")
    else:
        odds_output.delete(1.0, tk.END)
        odds_output.insert(tk.END, "Please enter a valid level (2-11) and cost (1-5).")

calculate_button = ttk.Button(odds_frame, text="Calculate Odds", command=calculate_odds)
calculate_button.pack(pady=10)

# Start the Tkinter main loop
window.mainloop()
