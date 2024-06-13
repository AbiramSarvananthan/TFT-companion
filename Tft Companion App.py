# Import necessary modules
import tkinter as tk  # Import the tkinter library for creating GUI applications
from tkinter import *  # Import all tkinter functions and classes for convenience
from tkinter.scrolledtext import ScrolledText  # Import ScrolledText widget for text display with scrollbars
import ttkbootstrap as ttk  # Import ttkbootstrap for themed tkinter widgets
import csv  # Import the csv module for reading CSV files

# Function to load meta builds from a CSV file
def load_meta_builds(filename):
    builds = []  # Initialize an empty list to store the builds
    try:
        with open(filename, 'r') as file:  # Open the CSV file for reading
            reader = csv.DictReader(file)  # Create a DictReader to parse the CSV file
            for row in reader:  # Iterate over each row in the CSV file
                builds.append(row)  # Append each row (as a dictionary) to the builds list
        return builds  # Return the list of builds
    except FileNotFoundError:  # If the file is not found
        return []  # Return an empty list

# Function to load trait names from a text file
def load_trait_names(filename):
    try:
        with open(filename, 'r') as file:  # Open the text file for reading
            trait_names = [line.strip().lower() for line in file.readlines()]  # Read each line, strip whitespace, convert to lowercase
        return trait_names  # Return the list of trait names
    except FileNotFoundError:  # If the file is not found
        return []  # Return an empty list

# Function to search for a trait in the list of builds
def search_trait_in_builds(trait, builds):
    results = []  # Initialize an empty list to store search results
    trait = trait.lower()  # Convert the search trait to lowercase
    for build in builds:  # Iterate over each build in the builds list
        if trait in build['Trait'].lower():  # Check if the trait is in the build's traits
            results.append(build)  # If found, append the build to the results list
    return results  # Return the search results

# Load the meta builds from the CSV file
builds = load_meta_builds('metaBuildsFile.csv')  # Call the function to load builds from a CSV file

# Load the trait names from the text file
trait_names = load_trait_names('traitNames.txt')  # Call the function to load trait names from a text file

# Create the main window
window = ttk.Window(themename='darkly')  # Create a themed window with the 'darkly' theme
window.title('Tft Companion App')  # Set the title of the window

# Get the native screen width and height
screen_width = window.winfo_screenwidth()  # Get the width of the screen
screen_height = window.winfo_screenheight()  # Get the height of the screen

# Set the initial window size to match the native screen resolution
window.geometry(f"{screen_width}x{screen_height}")  # Set the geometry of the window to fit the screen

# Create a notebook to switch between different pages
notebook = ttk.Notebook(window)  # Create a Notebook widget for tabbed pages
notebook.pack(fill='both', expand=True)  # Pack the Notebook to expand and fill the window

# Create frames for each tab
main_frame = ttk.Frame(notebook)  # Create a frame for the 'Meta Builds' tab
odds_frame = ttk.Frame(notebook)  # Create a frame for the 'TFT Odds Calculator' tab

notebook.add(main_frame, text="Meta Builds")  # Add the 'Meta Builds' frame to the Notebook
notebook.add(odds_frame, text="TFT Odds Calculator")  # Add the 'TFT Odds Calculator' frame to the Notebook

# Main Frame Widgets (Meta Builds)
label = ttk.Label(main_frame, text="Enter Trait Name:")  # Create a label for the trait entry
label.pack(pady=5)  # Pack the label with padding

trait_entry = ttk.Entry(main_frame, width=30)  # Create an entry widget for entering the trait name
trait_entry.pack(pady=10)  # Pack the entry widget with padding

output_text = ScrolledText(main_frame, width=100, height=50, wrap=WORD)  # Create a ScrolledText widget for displaying output
output_text.pack(fill='both', expand=True, padx=10, pady=10)  # Pack the ScrolledText widget with padding and expand to fill the frame

def search_trait():
    trait = trait_entry.get().lower()  # Get the entered trait name and convert to lowercase
    if trait in trait_names:  # Check if the entered trait name is valid
        results = search_trait_in_builds(trait, builds)  # Search for the trait in the builds
        output_text.delete(1.0, tk.END)  # Clear the output text widget
        bullet_point = "\u2192"  # Define a bullet point symbol

        if results:  # If results are found
            for i, result in enumerate(results):  # Iterate over each result
                output_text.insert(tk.END, f"Build {i+1}:\n", 'title')  # Insert build title
                output_text.insert(tk.END, "\n")
                output_text.insert(tk.END, f"Buildname: {result['Buildname']}\n", 'buildname_title')  # Insert build name
                output_text.insert(tk.END, f"Trait: {result['Trait']}\n", 'trait_title')  # Insert trait
                output_text.insert(tk.END, f"Difficulty: {result['Difficulty']}\n", 'difficulty_title')  # Insert difficulty
                output_text.insert(tk.END, f"Rank: {result['Rank']}\n", 'rank_title')  # Insert rank
                
                champion_list = result['Champions'].split(',')  # Split the champions string into a list
                item_list = result['Items'].split(',')  # Split the items string into a list
                augment_list = result['Augments'].split(',')  # Split the augments string into a list
                step_list = result['Steps'].split(',')  # Split the steps string into a list

                output_text.insert(tk.END, "Champions:\n", 'champions_title')  # Insert 'Champions' title
                for champion in champion_list:  # Iterate over each champion
                    output_text.insert(tk.END, f"{bullet_point} {champion.strip()}\n")  # Insert each champion with bullet point

                output_text.insert(tk.END, "Items:\n", 'items_title')  # Insert 'Items' title
                for item in item_list:  # Iterate over each item
                    output_text.insert(tk.END, f"{bullet_point} {item.strip()}\n")  # Insert each item with bullet point

                output_text.insert(tk.END, "Augments:\n", 'augments_title')  # Insert 'Augments' title
                for augment in augment_list:  # Iterate over each augment
                    output_text.insert(tk.END, f"{bullet_point} {augment.strip()}\n")  # Insert each augment with bullet point

                output_text.insert(tk.END, "Steps:\n", 'steps_title')  # Insert 'Steps' title
                for step in step_list:  # Iterate over each step
                    output_text.insert(tk.END, f"{bullet_point} {step.strip()}\n")  # Insert each step with bullet point

                if i < len(results) - 1:  # If not the last result
                    output_text.insert(tk.END, "\n" + "-" * 80 + "\n\n")  # Insert a separator line

        else:  # If no results are found
            output_text.insert(tk.END, f"No builds found for trait '{trait}'.")  # Display a no results message

        # Configure text tags for formatting
        output_text.tag_configure('title', font=('Helvetica', 12, 'bold'), underline=True)
        output_text.tag_configure('buildname_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('trait_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('difficulty_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('rank_title', font=('Helvetica', 10, 'bold'))
        output_text.tag_configure('champions_title', font=('Helvetica', 10, 'bold'), foreground='red')
        output_text.tag_configure('items_title', font=('Helvetica', 10, 'bold'), foreground='brown')
        output_text.tag_configure('augments_title', font=('Helvetica', 10, 'bold'), foreground='cyan')
        output_text.tag_configure('steps_title', font=('Helvetica', 10, 'bold'), foreground='magenta')

    else:  # If the entered trait name is not valid
        output_text.delete(1.0, tk.END)  # Clear the output text widget
        output_text.insert(tk.END, f"'{trait}' is not a valid trait name.")  # Display an invalid trait message

search_button = ttk.Button(main_frame, text="Search", command=search_trait, state='disabled')  # Create a search button
search_button.pack(pady=10)  # Pack the button with padding

def check_entry(event):
    if trait_entry.get():  # If the entry widget has text
        search_button['state'] = 'normal'  # Enable the search button
    else:  # If the entry widget is empty
        search_button['state'] = 'disabled'  # Disable the search button

trait_entry.bind('<KeyRelease>', check_entry)  # Bind the key release event to the check_entry function

# TFT Odds Calculator Widgets (Odds Frame)
odds_label_level = ttk.Label(odds_frame, text="Enter Level (2-11):")  # Create a label for level entry
odds_label_level.pack(pady=5)  # Pack the label with padding

level_entry = ttk.Entry(odds_frame, width=10)  # Create an entry widget for entering the level
level_entry.pack(pady=5)  # Pack the entry widget with padding

odds_label_cost = ttk.Label(odds_frame, text="Enter Unit Cost (1-5):")  # Create a label for unit cost entry
odds_label_cost.pack(pady=5)  # Pack the label with padding

cost_entry = ttk.Entry(odds_frame, width=10)  # Create an entry widget for entering the unit cost
cost_entry.pack(pady=5)  # Pack the entry widget with padding

odds_label_purchased = ttk.Label(odds_frame, text="Enter Number of Units Purchased:")  # Create a label for units purchased entry
odds_label_purchased.pack(pady=5)  # Pack the label with padding

purchased_entry = ttk.Entry(odds_frame, width=10)  # Create an entry widget for entering the number of units purchased
purchased_entry.pack(pady=5)  # Pack the entry widget with padding

odds_output = ScrolledText(odds_frame, width=50, height=10, wrap=WORD)  # Create a ScrolledText widget for displaying output
odds_output.pack(fill='both', expand=True, padx=10, pady=10)  # Pack the ScrolledText widget with padding and expand to fill the frame

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
    level = int(level_entry.get())  # Get the entered level
    cost = int(cost_entry.get())  # Get the entered unit cost
    purchased = int(purchased_entry.get())  # Get the entered number of units purchased

    if 2 <= level <= 11 and 1 <= cost <= 5:  # Validate the entered level and unit cost
        cost_index = cost - 1  # Calculate the index for the unit cost
        base_odds = odds_data[level][cost_index] / 100  # Get the base odds for the level and unit cost
        pool_size = pool_sizes[cost]  # Get the pool size for the unit cost
        remaining_units = pool_size - purchased  # Calculate the remaining units in the pool

        if remaining_units <= 0:  # If no units are left in the pool
            odds_output.delete(1.0, tk.END)  # Clear the output text widget
            odds_output.insert(tk.END, f"No units left in the pool for cost {cost}.")  # Display a no units message
        else:  # If units are left in the pool
            total_units = sum(pool_sizes.values())  # Calculate the total units in the pool
            hit_rate = (remaining_units / pool_size) * base_odds * 100  # Calculate the hit rate
            odds_output.delete(1.0, tk.END)  # Clear the output text widget
            odds_output.insert(tk.END, f"At level {level}, with {purchased} units purchased, the odds of finding a {cost}-cost unit are {hit_rate:.2f}%.")  # Display the calculated odds
    else:  # If the entered level or unit cost is invalid
        odds_output.delete(1.0, tk.END)  # Clear the output text widget
        odds_output.insert(tk.END, "Please enter a valid level (2-11) and cost (1-5).")  # Display an invalid input message

calculate_button = ttk.Button(odds_frame, text="Calculate Odds", command=calculate_odds)  # Create a button for calculating odds
calculate_button.pack(pady=10)  # Pack the button with padding

# Responsive Design Handling
def on_window_resize(event):
    # Get the new window size
    window.update_idletasks()  # Ensure window size is updated
    new_width = window.winfo_width()  # Get the new width of the window
    new_height = window.winfo_height()  # Get the new height of the window

    # Adjust the size of ScrolledText widgets based on new window size
    output_text.config(width=int(new_width / 15), height=int(new_height / 30))  # Adjust the size of the output_text widget
    odds_output.config(width=int(new_width / 30), height=int(new_height / 60))  # Adjust the size of the odds_output widget

# Bind the window resize event to the function
window.bind('<Configure>', on_window_resize)  # Bind the window resize event to the on_window_resize function

# Start the Tkinter main loop
window.mainloop()  # Start the main event loop of the Tkinter application
