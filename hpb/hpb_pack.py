import struct
from zlib import crc32
from pathlib import Path
import sys

def repack(packname):
    # 收集所有解压后的文件
    base_dir = Path(f'{packname}_out')
    files = []
    for file_path in base_dir.rglob('*'):
        if file_path.is_file():
            rel_path = file_path.relative_to(base_dir)
            files.append(str(rel_path).replace('\\', '/'))  # 统一使用正斜杠
    files.sort()  # 按路径排序，可能需要与原顺序一致
    count = len(files)
    
    # 生成hpb文件内容并收集条目信息
    entries = []
    hpb_data = bytearray(0)
    for path in files:
        file_path = base_dir / path
        with open(file_path, 'rb') as f:
            data = f.read()
        crc = crc32(data)
        size = len(data)
        offset = len(hpb_data)  # 当前数据偏移量
        if len(data) % 64 != 0 or not data:
            data += b'\0' * (64 - len(data) % 64)
        hpb_data.extend(data)
        entries.append({
            'offset': offset,
            'size': size,
            'crc': crc,
            'path': path
        })
    
    # 构建hph文件内容
    magic = int.from_bytes(b'HPAC', 'little')
    version = 0x00010100  # 根据样例设定版本
    hpb_size = len(hpb_data)
    nameoffset = 32 + count * 32  # 头部32B + 条目数×32B
    
    # 头部（5I + 12x填充）
    header = struct.pack('<5I12x', magic, version, count, 0, nameoffset)
    
    # 条目区域（每个条目32B）
    entries_bin = bytearray()
    for entry in entries:
        # 结构：Q(offset) I(0) Q(size) I(crc) 8x填充
        entry_bin = struct.pack('<QIQI8x', 
                               entry['offset'], 
                               0,  # 未知字段，置0
                               entry['size'], 
                               entry['crc'])
        entries_bin.extend(entry_bin)
    
    # 文件名区域（以null分隔）
    name_block = bytearray()
    for path in files:
        path = path.split('.')[-1]
        name_block.extend(path.encode('utf-8'))
        name_block.append(0)
    
    # 合并hph内容
    hph_data = header + entries_bin + name_block
    if len(hph_data) % 64 != 0:
        hph_data += b'\0' * (64 - len(hph_data) % 64)
    length = len(hph_data)
    hph_data = hph_data[:12] + struct.pack('<I', length) + hph_data[16:]
    
    # 写入文件
    with open(f'{packname}.hph', 'wb') as f:
        f.write(hph_data)
    with open(f'{packname}.hpb', 'wb') as f:
        f.write(hpb_data)
    
    print(f'Repacked {count} files into {packname}.hph and {packname}.hpb')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} packname')
        sys.exit(1)
    repack(sys.argv[1])