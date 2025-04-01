import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Button

# ---------------------------------------------------------------------------------------- #

def dict_to_dataframe(data):
    rows = []
    for digital_file, frames in data.items():
        for frame_name, mnemonics in frames.items():
            for mnemonic in mnemonics:  # Each mnemonic gets its own row
                rows.append([digital_file, frame_name, mnemonic])
    df = pd.DataFrame(rows, columns=["Digital File", "Frame Name", "Mnemonics"])
    return df

def dataframe_to_dict(df):
    data = {}
    for digital_file, frame_group in df.groupby("Digital File"):
        data[digital_file] = {}
        for frame_name, mnemonics_group in frame_group.groupby("Frame Name"):
            data[digital_file][frame_name] = mnemonics_group["Mnemonics"].tolist()
    return data

# ---------------------------------------------------------------------------------------- #

with open("data/data_vis.json", 'r') as json_file:
    dlis_data_structure = json.load(json_file)

# Convert JSON to DataFrame
table = dict_to_dataframe(dlis_data_structure)
num_rows = len(table)
rows_per_page = 50
num_pages = (num_rows // rows_per_page) + (1 if num_rows % rows_per_page else 0)

# Pagination Variables
current_page = 0
checkbox_states = [False] * len(table)

# ---------------------------------------------------------------------------------------- #

# Function to update the displayed checkboxes
def update_checkboxes():
    global checkboxes
    start_idx = current_page * rows_per_page
    end_idx = min(start_idx + rows_per_page, num_rows)
    checkbox_labels = [', '.join(row) for row in table.iloc[start_idx:end_idx].values]

    # Remove previous checkboxes
    checkbox_ax.clear()
    checkbox_ax.set_position([0.3, 0.2, 0.4, 0.7])
    
    # Create new checkboxes
    checkboxes = CheckButtons(checkbox_ax, checkbox_labels, checkbox_states[start_idx:end_idx])
    checkboxes.on_clicked(toggle_row)
    
    fig.canvas.draw_idle()

# Toggle checkbox selection
def toggle_row(label):
    index = table.apply(lambda row: ', '.join(row), axis=1).tolist().index(label)
    checkbox_states[index] = not checkbox_states[index]
    print(f'{label} is {"checked" if checkbox_states[index] else "unchecked"}')

# Navigation Functions
def next_page(event):
    global current_page
    if current_page < num_pages - 1:
        current_page += 1
        update_checkboxes()

def prev_page(event):
    global current_page
    if current_page > 0:
        current_page -= 1
        update_checkboxes()

# ---------------------------------------------------------------------------------------- #

# Create Figure
fig, ax = plt.subplots(figsize=(8, 10))
ax.axis('off')

# Checkboxes
checkbox_ax = fig.add_axes([0.3, 0.2, 0.4, 0.7])  # Adjust position
update_checkboxes()  # Initialize first page

# Buttons
btn_next_ax = fig.add_axes([0.7, 0.05, 0.2, 0.075])
btn_prev_ax = fig.add_axes([0.1, 0.05, 0.2, 0.075])

btn_next = Button(btn_next_ax, "Next")
btn_prev = Button(btn_prev_ax, "Previous")

btn_next.on_clicked(next_page)
btn_prev.on_clicked(prev_page)

plt.show()