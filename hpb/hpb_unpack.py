import struct
from zlib import crc32
from pathlib import Path
import sys

# Based on https://github.com/YuriSizuku/GalgameReverse/blob/master/project/hunex/src/hunex_hpb.py
# modded from https://gist.github.com/kjy00302/34461f7ced79be7c48e3d46ae94f047b

packname = sys.argv[1]

f = open(f'{packname}.hph', 'rb')
data_f = open(f'{packname}.hpb', 'rb')

magic, version, count, size, nameoffset = struct.unpack('<5I12x', f.read(32))
assert magic == int.from_bytes(b'HPAC', 'little')

offset = f.tell()
f.seek(nameoffset, 0)
paths = list(map(lambda x: x.decode(), f.read().split(b'\0')[:count]))
f.seek(offset, 0)

print(f'filesize: {size}, itemcnt: {count}')

for i in range(count):
    data = f.read(32)
    # TODO: QIQI or I4xII4xI?
    item = struct.unpack('<QIQI8x', data)
    itemoffset, itemsize, itemcrc = item[0], item[2], item[3]
    print(f'offset:{itemoffset} size:{itemsize} crc:{itemcrc:08x} -> {paths[i]}')
    # if itemsize == 0: continue
    data_f.seek(itemoffset, 0)
    itemdata = data_f.read(itemsize)
    assert itemcrc == crc32(itemdata)
    p = (Path(f'{packname}_out') / (f"{i:03d}."+paths[i]))
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('wb') as item_f:
        item_f.write(itemdata)
