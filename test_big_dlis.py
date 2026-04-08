from stoneforge.data_management.preprocessing import DataLoader

path = r"C:\Users\mario\Desktop\1-brsa-1363-rjs.dlis"
dlis_obj = DataLoader(path, filetype = 'dlis')
data_info = dlis_obj.data_obj.get_info()
digital_files = list(data_info.keys())

print('digital_files:',digital_files)

for d_file in digital_files:
    print("frames in '{}':".format(d_file),list(data_info[d_file].keys()))
