import struct
import sys

import lzss  # install pylzss, not lzss (requires initial buffer value argument)


def hdgl2hdlg(hdgl_file, hdlg_file):
    with open(hdgl_file, 'rb') as bin_file:
        data = bin_file.read()
        assert data[:4] == b"HDGL"
        
        encode_data = lzss.compress(data, 0)
        encode_size = len(encode_data)
        decode_size = len(data)
        
        with open(hdlg_file, 'wb') as output_file:
            output_file.write(b"HLZS")
            output_file.write(struct.pack('<I', 0x00001000))
            output_file.write(struct.pack('<I', encode_size))
            output_file.write(struct.pack('<I', decode_size))
            output_file.write(b'\x00' * 16)
            output_file.write(encode_data)
            if len(encode_data) % 32 != 0:
                output_file.write(b'\x00' * (32 - len(encode_data) % 32))
            
    print(f"{hdlg_file} saved.")

if __name__ == "__main__":
    hdgl_path = sys.argv[1]
    output_path = hdgl_path + ".hdlg"
    hdgl2hdlg(hdgl_path, output_path)
