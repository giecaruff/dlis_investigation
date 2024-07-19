from dlisio import dlis
import numpy as np
import os
import pandas as pd

def process_curve_info(channel_data):
    def df_column_uniquify(df):
        df_columns = df.columns
        new_columns = []
        print('AQUI')
        for item in df_columns:
            counter = 0
            newitem = item
            while newitem in new_columns:
                counter += 1
                newitem = "{}_{}".format(item, counter)
            new_columns.append(newitem)
        df.columns = new_columns
        return df
    
def process_curve_info(channel_data):
    def df_column_uniquify(df):
        df_columns = df.columns
        new_columns = []
        print('AQUI')
        for item in df_columns:
            counter = 0
            newitem = item
            while newitem in new_columns:
                counter += 1
                newitem = "{}_{}".format(item, counter)
            new_columns.append(newitem)
        df.columns = new_columns
        return df

    for name_index, c in enumerate(channel_data["curves_L"]):
        name = channel_data["curves_name"][name_index]
        print("Processing " + name)
        units = channel_data["unit"][name_index]
        long = channel_data["longs"][name_index]
        c = np.vstack(c)
        try:
            num_col = c.shape[1]
            col_name = [name] * num_col
            df = pd.DataFrame(data=c, columns=col_name)
            channel_data["curve_df"] = pd.concat([channel_data["curve_df"], df], axis=1)
            object_warning = str(
                name) + ' had to be expanded in the final .las file, as it has multiple samples per index'
        except:
            num_col = 1
            df = pd.DataFrame(data=c, columns=[name])
            channel_data["curve_df"] = pd.concat([channel_data["curve_df"], df], axis=1)
            continue
        u = [units] * num_col
        l = [long] * num_col
        channel_data["las_units"].append(u)
        channel_data["las_longs"].append(l)
        print("Completed " + name)

    las_units = [item for sublist in channel_data["las_units"] for item in sublist]
    las_longs = [item for sublist in channel_data["las_longs"] for item in sublist]

    # Check that the lists are ready for the curve metadata
    print("If these are different lengths, something is wrong:")
    print(len(las_units))
    print(len(las_longs))
    
    return channel_data

folder = input("Enter the folder path: ")

log = open('LOG.txt', 'w')

for file in os.listdir(folder):
    if file.endswith(".dlis"):
        dlis_file = os.path.join(folder, file)
        print("#####################################################")
        log.write("#####################################################\n")
        print("Dlis file name: ",dlis_file)
        log.write("FILE NAME: {}\n".format(dlis_file))
        local_log = open(file+'local_log.txt', 'w')

        try:
            with dlis.load(dlis_file) as files:
                frame_all = {}
                ii = 0
                for f in files:
                    print("Logical file:",f)
                    log.write("\nLOGICAL FILE: {} \n".format(f))
                    log.write("-------------------------------------------------\n")
                    local_log.write("\nLOGICAL FILE: {} \n".format(f))
                    local_log.write("-------------------------------------------------\n")
                    ii += 1
                    for frame in f.frames:
                        curves = frame.curves()
                        
                        channel_data = {
                                "curves_name": [],
                                "longs": [],
                                "unit": [],
                                "curves_L": [],
                                "curve_df": pd.DataFrame(),
                                "las_units": [],
                                "las_longs": [],
                            }
                        
                        for channel in frame.channels:
                            channel_data["curves_name"].append(channel.name)
                            channel_data["longs"].append(channel.long_name)
                            channel_data["unit"].append(channel.units)
                            curves = channel.curves()
                            channel_data["curves_L"].append(curves)
                        print(channel_data["curves_name"])
                        print(channel_data["curves_name"][0],":",channel_data["curves_L"][0][0],". . .",channel_data["curves_L"][0][1],'(',len(channel_data["curves_L"][0]),')')
                        print()
                        for iii in range(len(channel_data["curves_name"])):
                            log.write("{}: {} . . . {} ({})\n".format(channel_data["curves_name"][iii],channel_data["curves_L"][iii][0],channel_data["curves_L"][iii][1],np.shape(channel_data["curves_L"][iii])))
                            local_log.write("{}: {} . . . {} ({})\n".format(channel_data["curves_name"][iii],channel_data["curves_L"][iii][0],channel_data["curves_L"][iii][1],np.shape(channel_data["curves_L"][iii])))

                    frame_all[ii] = channel_data
        except:
            print("!!! Error !!! reading file", dlis_file)
            continue
        
        print("#####################################################")

