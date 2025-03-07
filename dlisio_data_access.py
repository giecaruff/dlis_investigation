import pandas as pd
import numpy as np
from dlisio import dlis  # Correct library import

def parse_dlis(file_path):
    all_data = {}

    with dlis.load(file_path) as files:
        for f in files:
            logical_file_id = str(f)  # Unique identifier for each file
            all_data[logical_file_id] = {}

            simple_frames = {frame.name: frame for frame in f.frames}

            for frame in f.frames:
                frame_id = frame.name
                all_data[logical_file_id][frame_id] = {}

                for channel in frame.channels:
                    mnemonic = channel.name
                    unit = channel.units
                    values = np.array(channel.curves())  # Convert to numpy array

                    all_data[logical_file_id][frame_id][mnemonic] = {
                        'unit': unit,
                        'values': values
                    }

    return all_data

########################################################################################

def inspect_dlis_structure(dlis_file):
    with dlis.load(dlis_file) as file:
        print(f"Logical Files Found: {len(file)}")
        for lf in file:
            print("\n==========================")
            print(f"Logical File: {lf}")
            
            # List all frames and their respective channels
            frames = lf.frames
            print(f"Total Frames: {len(frames)}")
            for frame in frames:
                print(f" - Frame Name: {frame.name}, Channels: {len(frame.channels)}")
                for ch in frame.channels:
                    print(f"   * Mnemonic: {ch.name}, \t Units: {ch.units}, \t Description: {ch.long_name}")

# Call the function
inspect_dlis_structure('data/IODP_311-U1325A_rab-proc.dlis')
                
########################################################################################

data_access = {
    'LogicalFile(RAB_shallow)':{
        'B77185':['TDEP','BSAV'],
        'B77226':['TDEP','RB','GR']
        },
    'LogicalFile(RAB_medium)':{
        'B77185':['TDEP','BMIM'],
        'B77226':['TDEP','GR']
        },
    'LogicalFile(RAB_deep)':{
        'B77226':['TDEP','GR'] 
        }
    }

########################################################################################

def parse_dlis(file_path, data_access):
    extracted_data = {}

    with dlis.load(file_path) as files:
        for f in files:
            logical_file_id = str(f)  # Unique identifier for each logical file
            
            if logical_file_id not in data_access:
                continue  # Skip if the logical file is not in the selection

            extracted_data[logical_file_id] = {}

            simple_frames = {frame.name: frame for frame in f.frames}

            for frame_name, mnemonics in data_access[logical_file_id].items():
                if frame_name not in simple_frames:
                    continue  # Skip if the frame is not found

                frame = simple_frames[frame_name]
                extracted_data[logical_file_id][frame_name] = {}

                for channel in frame.channels:
                    if channel.name in mnemonics:
                        mnemonic = channel.name
                        unit = channel.units
                        values = np.array(channel.curves())  # Convert to numpy array

                        extracted_data[logical_file_id][frame_name][mnemonic] = {
                            'unit': unit,
                            'values': values
                        }

    return extracted_data

# Example usage
print('\n')
file_path = 'data/IODP_311-U1325A_rab-proc.dlis'
data = parse_dlis(file_path, data_access)
print(data)
del data