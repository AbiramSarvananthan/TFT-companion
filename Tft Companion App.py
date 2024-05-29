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

# Create the main frame
main_frame = ttk.Frame(master=window)
main_frame.pack()

# Create label prompting user to enter trait name
label = ttk.Label(master=window, text="Enter Trait Name:")
label.pack(pady=5)

# Create entry field for trait input
trait_entry = ttk.Entry(master=window, width=30)
trait_entry.pack(pady=10)

# Create output text area for displaying search results
output_text = ScrolledText(master=window, width=100, height=50, wrap=WORD)
output_text.pack()

# Function to search for trait and display results
def search_trait():
    trait = trait_entry.get().lower()
    if trait in trait_names:
        results = search_trait_in_builds(trait, builds)
        output_text.delete(1.0, tk.END)
        # Define Unicode arrow character for bullet point
        bullet_point = "\u2192"  # Arrow point character (→)

        if results:
            for i, result in enumerate(results):
                output_text.insert(tk.END, f"Build {i+1}:\n", 'title')
                output_text.insert(tk.END, "\n")  # Add an empty line after the title
                output_text.insert(tk.END, f"Buildname: {result['Buildname']}\n", 'buildname_title')
                output_text.insert(tk.END, f"Trait: {result['Trait']}\n", 'trait_title')
                output_text.insert(tk.END, f"Difficulty: {result['Difficulty']}\n", 'difficulty_title')
                output_text.insert(tk.END, f"Rank: {result['Rank']}\n", 'rank_title')
                
                # Group related information together
                champion_list = result['Champions'].split(',')
                item_list = result['Items'].split(',')
                augment_list = result['Augments'].split(',')
                step_list = result['Steps'].split(',')

                # Insert champions
                output_text.insert(tk.END, "Champions:\n", 'champions_title')
                for champion in champion_list:
                    output_text.insert(tk.END, f"{bullet_point} {champion.strip()}\n")

                # Insert items
                output_text.insert(tk.END, "Items:\n", 'items_title')
                for item in item_list:
                    output_text.insert(tk.END, f"{bullet_point} {item.strip()}\n")

                # Insert augments
                output_text.insert(tk.END, "Augments:\n", 'augments_title')
                for augment in augment_list:
                    output_text.insert(tk.END, f"{bullet_point} {augment.strip()}\n")

                # Insert steps
                output_text.insert(tk.END, "Steps:\n", 'steps_title')
                for step in step_list:
                    output_text.insert(tk.END, f"{bullet_point} {step.strip()}\n")

                # Add separator between builds
                if i < len(results) - 1:
                    output_text.insert(tk.END, "\n" + "-" * 80 + "\n\n")

        else:
            output_text.insert(tk.END, f"No builds found for trait '{trait}'.")

        # Define text styles with colors for titles only
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

# Create search button
search_button = ttk.Button(master=window, text="Search", command=search_trait, state='disabled')
search_button.pack(pady=10)

# Function to enable/disable search button based on entry field input
def check_entry(event):
    if trait_entry.get():
        search_button['state'] = 'normal'
    else:
        search_button['state'] = 'disabled'

# Bind event to check for entry field input
trait_entry.bind('<KeyRelease>', check_entry)

# Make the columns and rows expandable
for i in range(2):
    main_frame.columnconfigure(i, weight=1)
main_frame.rowconfigure(1, weight=1)

# Start the Tkinter main loop
window.mainloop()
