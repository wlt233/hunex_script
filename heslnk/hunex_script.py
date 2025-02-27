import sys
import os
import lzss  # pip install pylzss
import struct



def pad_bytes(data: bytes) -> bytes:
    padding_length = (0x20 - (len(data) % 0x20)) % 0x20
    return data + b"\x00" * padding_length


def decompress_hlzs(enc: bytes) -> bytes:
    if len(enc) < 0x20:
        raise ValueError("Invalid HLZS header")
    
    signature, version, enc_size, dec_size = struct.unpack("<4I", enc[:0x10])
    if signature != int.from_bytes(b"HLZS", "little"):
        raise ValueError("Invalid HLZS signature")

    dec = lzss.decompress(enc[0x20: 0x20 + enc_size], 0)
    if len(dec) < dec_size:
        raise ValueError("Not enough data in HLZS buffer")
    return dec[:dec_size]


def compress_hlzs(dec: bytes) -> bytes:
    enc = lzss.compress(dec, 0)
    signature = int.from_bytes(b"HLZS", "little")
    version = 0x1000
    enc_size = len(enc)
    dec_size = len(dec)
    header = struct.pack("<4I", signature, version, enc_size, dec_size)
    return pad_bytes(header) + pad_bytes(enc)


def unpack_hesl(input_buffer: bytes, output_folder: str):
    header_data = input_buffer[:0x30]
    magic, version, count, unk1, unk2, name_offset, data_offset = struct.unpack("<5I12x2I8x", header_data)
    if magic != int.from_bytes(b"HESL", "little"):
        raise ValueError("Invalid HESL signature")

    paths = []
    offset = name_offset
    for i in range(count):
        end = input_buffer.find(b"\x00", offset)
        if end == -1:
            raise ValueError("Unterminated string in HESL header")
        paths.append(input_buffer[offset: end].decode())
        offset = end + 1

    for i in range(count):
        checksum, item_offset, decrypted_size = struct.unpack("<3I4x", input_buffer[0x30 + i * 0x10: 0x30 + i * 0x10 + 0x10])
        output_path = os.path.join(output_folder, f"{paths[i]}.hese")
        compressed_buffer = input_buffer[item_offset: item_offset + decrypted_size]

        try:
            decompressed = decompress_hlzs(compressed_buffer)
        except Exception as e:
            print(f"Error decompressing {paths[i]}: {e}")
            continue

        with open(output_path, "wb") as fo:
            fo.write(decompressed)

        print(f"Processed {i + 1}/{count}: {paths[i]}, offset: {item_offset}, size: {decrypted_size}")


def repack_hesl(input_folder: str) -> bytes:
    hese_files = [f for f in os.listdir(input_folder) if f.endswith(".hese")]
    hese_files.sort()
    count = len(hese_files)
    name_offset = 0x30 + count * 0x10
    if count % 2 == 0:
        name_offset += 0x10

    name_list = []
    for hese_file in hese_files:
        hese_script_name = os.path.splitext(hese_file)[0]
        name_list.append(hese_script_name.encode() + b"\x00")
    name_bytes = b"".join(name_list)
    name_bytes = pad_bytes(name_bytes)

    data_offset = name_offset + len(name_bytes)
    header = struct.pack("<5I12x2I8x", int.from_bytes(b"HESL", "little"), 0x10000, count, 0, 0, name_offset, data_offset)
    
    output_buffer = bytearray(header)

    item_offset = data_offset
    hese_compressed_bytes = []
    for i, hese_file in enumerate(hese_files):
        hese_path = os.path.join(input_folder, hese_file)
        with open(hese_path, "rb") as fi:
            decompressed = fi.read()
        item_size = len(decompressed)
        compressed = compress_hlzs(decompressed)
        output_buffer.extend(struct.pack("<3I4x", 0, item_offset, item_size))
        item_offset += len(compressed)
        hese_compressed_bytes.append(compressed)
        print(f"Processed {i + 1}/{count}: {hese_file}")
    
    if count % 2 == 0:
        output_buffer.extend(b"\x00" * 0x10)
    
    output_buffer.extend(name_bytes)

    for hese_compressed in hese_compressed_bytes:
        output_buffer.extend(hese_compressed)

    return bytes(output_buffer)
    

def main(argv):
    if len(argv) < 2:
        print("Usage:")
        print("  Unpack HESL:       python hunex_script.py <script.heslnk>")
        print("  Repack HESL:       python hunex_script.py <script_hese_folder>")
        print("  Decompress HDLG:   python hunex_script.py <script_dialog.hdlg>")
        print("  Recompress HDLG:   python hunex_script.py <script_dialog.hdgl>")
        return 1

    input_path = argv[1]
    
    if os.path.isfile(input_path):
        with open(input_path, "rb") as f:
            input_data = f.read()

        if input_data[:4] == b"HLZS":
            output_data = decompress_hlzs(input_data)
            output_filename = input_path + ".hdgl"
            print("Decompressed:", os.path.basename(input_path))
            with open(output_filename, "wb") as f:
                f.write(output_data)
            print("Output written to:", output_filename)
        elif input_data[:4] == b"HDGL":
            output_data = compress_hlzs(input_data)
            output_filename = input_path + ".hdlg"
            print("Compressed:", os.path.basename(input_path))
            with open(output_filename, "wb") as f:
                f.write(output_data)
            print("Output written to:", output_filename)
        elif input_data[:4] == b"HESL":
            output_folder = os.path.splitext(input_path)[0] + "_hese"
            os.makedirs(output_folder, exist_ok=True)
            unpack_hesl(input_data, output_folder)
            print(f"Files extracted to: {output_folder}")
        else:
            print("Error: Invalid file format")
            return 1

    elif os.path.isdir(input_path):
        output_data = repack_hesl(input_path)
        output_filename = os.path.join(os.path.dirname(input_path), f"{os.path.basename(input_path)}.heslnk")
        with open(output_filename, "wb") as f:
            f.write(output_data)
        print(f"Files repacked to: {output_filename}")

    else:
        print("Error: Path does not exist.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
