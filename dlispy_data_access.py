import numpy as np
from dlispy import parse, FrameData
import re

from dlispy import LogicalFile, Object, Attribute, FrameData, PrivateEncryptedEFLR, parse
from dlispy import OlrEFLR, FrameEFLR
from dlispy import Frame, FrameData, Origin

def parse_dlispy(file_path):

    # Parse the .dlis file
    _, logical_file_list = parse(file_path, eflr_only=False)

    data_file = {}
    for lf in logical_file_list:
        logical_file_id = lf.id.strip()
        file_key = f"LogicalFile({logical_file_id})"
        file_data = {"frames": []}
        
        simple_frames_keys = list(lf.simpleFrames.keys())

        ii = 0
        data_file[logical_file_id] = {}
        for frame_name, fDataList in lf.frameDataDict.items():
            sfk = simple_frames_keys[ii]
            frame_id = str(frame_name.identifier) if hasattr(frame_name, "identifier") else str(frame_name)
            
            data_file[logical_file_id][frame_id] = {}
            for jj in range(len(lf.simpleFrames[sfk].ChannelNames)):
                mnemonic = lf.simpleFrames[sfk].ChannelNames[jj].identifier
                unit = lf.simpleFrames[sfk].Channels[jj].Units

                data_file[logical_file_id][frame_id][mnemonic] = {}
                data_file[logical_file_id][frame_id][mnemonic]['unit'] = unit
                data_file[logical_file_id][frame_id][mnemonic]['values'] = []

                _data = []
                for fdata in fDataList:
                    _data.append(fdata.slots[jj])

                data_file[logical_file_id][frame_id][mnemonic]['values'] = np.array(_data)
                
            ii += 1

    return data_file

########################################################################################

def inspect_dlispy_structure(file_path):
    _, logical_file_list = parse(file_path, eflr_only=False)

    print(f"Logical Files Found: {len(logical_file_list)}")
    for lf in logical_file_list:
        logical_file_id = lf.id.strip()
        print("\n==========================")
        print(f"Logical File: LogicalFile({logical_file_id})")

        # List all frames and their respective channels
        frames = lf.simpleFrames
        print(f"Total Frames: {len(frames)}")

        for frame_name, frame in frames.items():
            print(f" - Frame Name: {frame_name.identifier}, Channels: {len(frame.ChannelNames)}")
            
            for jj, channel in enumerate(frame.ChannelNames):
                mnemonic = channel.identifier
                unit = frame.Channels[jj].Units
                print(f"   * Mnemonic: {mnemonic}, \t Units: {unit}")

# Call the function
inspect_dlispy_structure('data/IODP_311-U1325A_rab-proc.dlis')
               
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

def parse_dlispy(file_path, data_access):
    _, logical_file_list = parse(file_path, eflr_only=False)

    extracted_data = {}

    for lf in logical_file_list:
        logical_file_id = lf.id.strip()
        file_key = f"LogicalFile({logical_file_id})"

        if file_key not in data_access:
            continue  # Skip if the logical file is not in the selection

        extracted_data[file_key] = {}

        simple_frames_keys = list(lf.simpleFrames.keys())

        ii = 0
        for frame_name, fDataList in lf.frameDataDict.items():
            sfk = simple_frames_keys[ii]
            frame_id = str(frame_name.identifier) if hasattr(frame_name, "identifier") else str(frame_name)

            if frame_id not in data_access[file_key]:
                ii += 1
                continue  # Skip if the frame is not in the selection

            extracted_data[file_key][frame_id] = {}

            for jj in range(len(lf.simpleFrames[sfk].ChannelNames)):
                mnemonic = lf.simpleFrames[sfk].ChannelNames[jj].identifier

                if mnemonic not in data_access[file_key][frame_id]:
                    continue  # Skip if the curve is not in the selection

                unit = lf.simpleFrames[sfk].Channels[jj].Units

                _data = []
                for fdata in fDataList:
                    _data.append(fdata.slots[jj])

                extracted_data[file_key][frame_id][mnemonic] = {
                    'unit': unit,
                    'values': np.array(_data)
                }

            ii += 1

    return extracted_data

# Example usage
print('\n')
file_path = 'data/IODP_311-U1325A_rab-proc.dlis'
data = parse_dlispy(file_path, data_access)
print(data)
del data