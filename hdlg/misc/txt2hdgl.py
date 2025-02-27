import sys


def txt2hdgl(text_file, hdgl_file, version=0x00010000):
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
    
    with open(hdgl_file, 'wb') as f:
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
        
    print(f"{hdgl_file} saved.")




if __name__ == "__main__":
    txt_path = sys.argv[1]
    output_path = txt_path + ".hdgl"
    txt2hdgl(txt_path, output_path)
