import struct
import sys

import lzss  # install pylzss, not lzss (requires initial buffer value argument)

def hdlg2hdgl(hdlg_file, hdgl_file):
    with open(hdlg_file, 'rb') as bin_file:
        magic_number = bin_file.read(4).decode('utf-8')
        assert magic_number == "HLZS"
        
        version = struct.unpack('<I', bin_file.read(4))[0] # guess
        encode_size = struct.unpack('<I', bin_file.read(4))[0]
        decode_size = struct.unpack('<I', bin_file.read(4))[0]
        bin_file.read(16)
        
        encode_data = bin_file.read(encode_size)
        decode_data = lzss.decompress(encode_data, 0)
        assert len(decode_data) == decode_size
        
        with open(hdgl_file, 'wb') as output_file:
            output_file.write(decode_data)

    print(f"{hdgl_file} saved.")




if __name__ == "__main__":
    hdlg_path = sys.argv[1]
    output_path = hdlg_path + ".hdgl"
    hdlg2hdgl(hdlg_path, output_path)
