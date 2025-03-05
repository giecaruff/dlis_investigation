import pandas as pd
import numpy as np
from dlisio import dlis  # Correct library import

def parse_dlis(file_path):
    all_data = {}

    with dlis.load(file_path) as files:
        for f in files:
            file_key = str(f)  # Unique identifier for each file

            file_data = {
                'frames': [
                    {
                        "frame_name": frame.name,
                        "channels": [
                            {
                                "curves_name": channel.name,
                                "long_name": channel.long_name,
                                "unit": channel.units,
                                "curves_data": np.array(channel.curves())  # Convert directly to numpy array
                            }
                            for channel in frame.channels
                        ]
                    }
                    for frame in f.frames
                ]
            }

            all_data[file_key] = file_data

    return all_data

# Example of calling the function
file_path = 'data/IODP_311-U1325A_rab-proc.dlis'
data = parse_dlis(file_path)

for logical_file in data:
    print(f'Logical file: {logical_file}')

print('0 level:',data.keys())
print('1 level:',data['LogicalFile(RAB_shallow)'].keys())
print('2 level:',data['LogicalFile(RAB_shallow)']['frames'])
print('3 level:',data['LogicalFile(RAB_shallow)']['frames'][0].keys())
print('4 level:',data['LogicalFile(RAB_shallow)']['frames'][0]['channels'])
print('5 level:',data['LogicalFile(RAB_shallow)']['frames'][0]['channels'][0].keys())
print('6 level:',data['LogicalFile(RAB_shallow)']['frames'][0]['channels'][0]['curves_data'][0:10])