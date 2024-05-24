import tkinter as tk
import ttkbootstrap as ttk
import csv

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

def load_champion_names(filename):
    try:
        with open(filename, 'r') as file:
            champion_names = [line.strip().lower() for line in file.readlines()]
        return champion_names
    except FileNotFoundError:
        return []

def search_champion_in_builds(champion, builds):
    results = []
    champion = champion.lower()
    for build in builds:
        if champion in build['Champions'].lower():
            results.append(build)
    return results

# Load the meta builds from the file
builds = load_meta_builds('metaBuildsFile.csv')

# Load the champion names from the file
champion_names = load_champion_names('championNames.txt')

window = ttk.Window(themename='darkly')
window.title('Tft Companion App')
window.geometry('1980x1080')

main_frame = ttk.Frame(master=window)
main_frame.pack()

label = ttk.Label(master=window, text="Enter Champion Name:")
label.pack(pady=5)

champion_entry = ttk.Entry(master=window, width=30)
champion_entry.pack(pady=10)

output_text = tk.Text(master=window, width=100, height=50)
output_text.pack()

def search_champion():
    champion = champion_entry.get().lower()
    if champion in champion_names:
        results = search_champion_in_builds(champion, builds)
        output_text.delete(1.0, tk.END)
        if results:
            for i, result in enumerate(results):
                output_text.insert(tk.END, f"Buildname: {result['Buildname']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Buildname
                output_text.insert(tk.END, f"Difficulty: {result['Difficulty']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Difficulty
                output_text.insert(tk.END, f"Rank: {result['Rank']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Rank
                output_text.insert(tk.END, f"Champions: {result['Champions']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Champions
                output_text.insert(tk.END, f"Items: {result['Items']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Items
                output_text.insert(tk.END, f"Augments: {result['Augments']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Augments
                output_text.insert(tk.END, f"Steps: {result['Steps']}\n")
                output_text.insert(tk.END, "─" * 50 + "\n")  # Separator line after Steps
                if i < len(results) - 1:
                    output_text.insert(tk.END, "━" * 50 + "\n")  # Separator line between builds
        else:
            output_text.insert(tk.END, f"No builds found for champion '{champion}'.")
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"'{champion}' is not a valid champion name.")

search_button = ttk.Button(master=window, text="Search", command=search_champion, state='disabled')
search_button.pack(pady=10)

def check_entry(event):
    if champion_entry.get():
        search_button['state'] = 'normal'
    else:
        search_button['state'] = 'disabled'

champion_entry.bind('<KeyRelease>', check_entry)

# Make the columns and rows expandable
for i in range(2):
    main_frame.columnconfigure(i, weight=1)
main_frame.rowconfigure(1, weight=1)

# Start the Tkinter main loop
window.mainloop()
