import io
import struct
import sys

import lzss  # install pylzss, not lzss (requires initial buffer value argument)


def hdgl2hdlg(hdgl_data, hdlg_file):
    assert hdgl_data[:4] == b"HDGL"
    
    encode_data = lzss.compress(hdgl_data, 0)
    encode_size = len(encode_data)
    decode_size = len(hdgl_data)
    
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

def txt2hdgl(text_file, version=0x00010000):
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    
    num_lines = len(lines)
    text_start_offset = 32 + num_lines * 4 
    current_offset = 0
    offsets = []
    text_data = bytearray()
    for line in lines:
        offsets.append(current_offset)
        line_bytes = line.encode('utf-8') + b'\x00'
        text_data += line_bytes
        current_offset += len(line_bytes)
    if current_offset % 32 != 0:
        text_data += b'\x00' * (32 - current_offset % 32)
    
    f = io.BytesIO()
    f.write(b'HDGL')
    f.write(version.to_bytes(4, 'little'))
    f.write(num_lines.to_bytes(4, 'little'))
    f.write(text_start_offset.to_bytes(4, 'little'))
    f.write(b'\x00' * 16)
    for offset in offsets:
        f.write(offset.to_bytes(4, 'little'))
    f.write(text_data)
    if f.tell() % 32 != 0:
        f.write(b'\x00' * (32 - f.tell() % 32))
    return f.getvalue()



if __name__ == "__main__":
    txt_path = sys.argv[1]
    output_path = txt_path + ".hdlg"
    hdgl2hdlg(txt2hdgl(txt_path), output_path)
