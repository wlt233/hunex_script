import struct
import sys

def hdgl2txt(hdgl_file, text_file):
    with open(hdgl_file, 'rb') as bin_file:
        magic_number = bin_file.read(4).decode('utf-8')
        assert magic_number == "HDGL"
        
        version = struct.unpack('<I', bin_file.read(4))[0] # guess
        line_count = struct.unpack('<I', bin_file.read(4))[0]
        text_offset = struct.unpack('<I', bin_file.read(4))[0]
        bin_file.read(16)
        
        offsets = []
        for _ in range(line_count):
            offset = struct.unpack('<I', bin_file.read(4))[0]
            offsets.append(offset)
            
        bin_file.seek(text_offset)
        text_data = bin_file.read()
        
        lines = []
        for i in range(line_count):
            start_offset = offsets[i]
            if i < line_count - 1:
                end_offset = offsets[i + 1]
            else:
                end_offset = len(text_data)
            line = text_data[start_offset:end_offset].split(b'\x00')[0].decode('utf-8')
            lines.append(line)
            
        with open(text_file, 'w', encoding='utf-8') as output_file:
            for line in lines[:-1]:
                output_file.write(line + '\n')
            output_file.write(lines[-1])

    print(f"{text_file} saved.")




if __name__ == "__main__":
    hdgl_path = sys.argv[1]
    output_path = hdgl_path + ".txt"
    hdgl2txt(hdgl_path, output_path)
