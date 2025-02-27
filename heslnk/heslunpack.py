import struct
import lzss  # install pylzss, not lzss (requires initial buffer value argument)
import os

# from https://gist.github.com/kjy00302/cce541058c1698f2eb6e3d9d7d34da17

def readuntilnull(f):
    buf = b''
    while True:
        data = f.read(16)
        offset = data.find(b'\0')
        if offset != -1:
            f.seek(offset-15, 1)
            return buf + data[:offset]
        else:
            buf += data


def hlzsdecomp(f):
    magic, version, compsize, size = struct.unpack('<4I16x', f.read(32))
    assert magic == int.from_bytes(b'HLZS', 'little')
    data = lzss.decompress(f.read(compsize), 0)
    assert len(data) == size
    return data


f = open('script.heslnk', 'rb')
os.makedirs('script_out', exist_ok=True)

magic, version, count, unk1, unk2, nameoffset, dataoffset = struct.unpack('<5I12x2I8x', f.read(48))
assert magic == int.from_bytes(b'HESL', 'little')

offset = f.tell()
f.seek(nameoffset, 0)
paths = []
for i in range(count):
    paths.append(readuntilnull(f).decode())
f.seek(offset, 0)

for i in range(count):
    i1, itemoffset, itemsize = struct.unpack('<3I4x', f.read(16))
    print(f'offset: {itemoffset} size: {itemsize} -> {paths[i]}')
    with open(f'script_out/{paths[i]}.hese', 'wb') as item_f:
        offset = f.tell()
        f.seek(itemoffset, 0)
        item_f.write(hlzsdecomp(f))
        f.seek(offset, 0)

