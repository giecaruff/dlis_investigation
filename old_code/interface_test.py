import json
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Slider
import pandas as pd
import numpy as np

# Constants
ROWS_PER_PAGE = 30
LIGHT_BLUE = (0.85, 0.92, 1)  # Light blue shade for text background

def load_json_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def _dict_to_dataframe(data):
    rows = []
    for digital_file, frames in data.items():
        for frame_name, mnemonics in frames.items():
            for mnemonic in mnemonics:
                rows.append([digital_file, frame_name, mnemonic])
    return pd.DataFrame(rows, columns=["Digital File", "Frame Name", "Mnemonics"])

def _dataframe_to_dict(df):
    data = {}
    for digital_file, frame_group in df.groupby("Digital File"):
        data[digital_file] = {}
        for frame_name, mnemonics_group in frame_group.groupby("Frame Name"):
            data[digital_file][frame_name] = mnemonics_group["Mnemonics"].tolist()
    return data

# Load data
info = load_json_data(r"data\data_vis.json")
table = _dict_to_dataframe(info)

# Calculate number of pages needed
total_rows = len(table)
num_pages = (total_rows + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE  # Ceiling division

# Create figure with appropriate height
fig_height = max(6, min(ROWS_PER_PAGE, total_rows) * 0.3)
fig, ax = plt.subplots(figsize=(9, fig_height))  # Adjust size
plt.subplots_adjust(left=0.2)  # Make room for the vertical slider
ax.axis('off')

# Create vertical slider axis
slider_ax = plt.axes([0.25, 0.13, 0.05, 0.73])  # (left, bottom, width, height)
page_slider = Slider(slider_ax, 'Page', valmin = 1, valmax = num_pages, valinit=num_pages, valstep=1, orientation='vertical')

# Create checkbox axis (will be updated)
checkbox_ax = plt.axes([0.2, 0.1, 0.7, 0.8])  # (left, bottom, width, height)
checkbox_ax.set_axis_off()

# Store all checkbox states and labels globally
all_checkbox_states = [False] * total_rows
checkbox_labels_all = [', '.join(row) for row in table.values]
current_checkboxes = None

def update_checkboxes(page):
    global current_checkboxes
    
    # Clear previous checkboxes
    checkbox_ax.clear()
    checkbox_ax.set_axis_off()
    
    # Calculate current page range (reversed order)
    page_idx = int(num_pages - page)  # This reverses the page order
    start_idx = page_idx * ROWS_PER_PAGE
    end_idx = min(start_idx + ROWS_PER_PAGE, total_rows)
    
    # Get current page labels and states
    current_labels = checkbox_labels_all[start_idx:end_idx]
    current_states = all_checkbox_states[start_idx:end_idx]
    
    # Create new checkboxes
    current_checkboxes = CheckButtons(checkbox_ax, current_labels, current_states)
    
    # Apply alternating row colors
    for i, label in enumerate(current_checkboxes.labels):
        if i % 2 == 1:  # Apply light blue to every second row
            label.set_backgroundcolor(LIGHT_BLUE)
        else:
            label.set_backgroundcolor('white')  # Keep other rows white
        label.set_color('black')  # Set text color to black for contrast

    def toggle_row(label):
        global all_checkbox_states
        full_index = checkbox_labels_all.index(label)
        all_checkbox_states[full_index] = not all_checkbox_states[full_index]
        print(f'{label} is {"checked" if all_checkbox_states[full_index] else "unchecked"}')

    current_checkboxes.on_clicked(toggle_row)
    plt.draw()

# Initialize first page
update_checkboxes(1)

# Connect slider to update function
page_slider.on_changed(update_checkboxes)

plt.show()

# After closing the window, get selected rows
selected_rows = [i for i, checked in enumerate(all_checkbox_states) if checked]
selected_table = table.iloc[selected_rows]
dict_data_info = _dataframe_to_dict(selected_table)
print(f"Selected {len(selected_table)} rows")
print("Selected rows data:")
print(dict_data_info)