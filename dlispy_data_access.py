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

        # Only functional for visualization
        #for jj in lf.simpleFrames:
        #    print(lf.simpleFrames[jj].ChannelNames[0].identifier, lf.simpleFrames[jj].Channels[0].Units) # functional - take the mnemonics and units

        
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

    print(data_file)
    #return all_data

# Example usage
file_path = 'data/IODP_311-U1325A_rab-proc.dlis'
data = parse_dlispy(file_path)

#print('0 level:', data.keys())
#print('1 level:', data['LogicalFile(RAB_shallow)'].keys())
#print('2 level:', data['LogicalFile(RAB_shallow)']['frames'])
#print('3 level:', data['LogicalFile(RAB_shallow)']['frames'][0].keys())
#print('4 level:', data['LogicalFile(RAB_shallow)']['frames'][0]['channels'])
#print('5 level:', data['LogicalFile(RAB_shallow)']['frames'][0]['channels'][0].keys())
#print('6 level:', data['LogicalFile(RAB_shallow)']['frames'][0]['channels'][0]['curves_data'][0:10])