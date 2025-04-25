import io
import os
import struct
import sys
from pathlib import Path
from zlib import crc32

import lzss  # install pylzss, not lzss (requires initial buffer value argument)

# Based on https://github.com/YuriSizuku/GalgameReverse/blob/master/project/hunex/src/hunex_hpb.py
# modded from https://gist.github.com/kjy00302/34461f7ced79be7c48e3d46ae94f047b


def hlzsdecomp(f):
    magic, version, compsize, size = struct.unpack('<4I16x', f.read(32))
    assert magic == int.from_bytes(b'HLZS', 'little')
    data = lzss.decompress(f.read(compsize), 0)
    assert len(data) == size
    return data


packname = sys.argv[1]

f = open(f'{packname}.hph', 'rb')
data_f = open(f'{packname}.hpb', 'rb')

magic, version, count, size, nameoffset = struct.unpack('<5I12x', f.read(32))
assert magic == int.from_bytes(b'HPAC', 'little')

offset = f.tell()
f.seek(nameoffset, 0)
paths = list(map(lambda x: x.decode(), f.read().split(b'\0')[:count]))
f.seek(offset, 0)

print(f'file size: {size}, item count: {count}')

for i in range(count):
    data = f.read(32)
    item = struct.unpack('<QIIIII4x', data)
    offset, size, decomp_size, crc, decomp_crc = item[0], item[2], item[3], item[4], item[5]
    print(f'offset:{offset} size:{size} crc:{crc:08x} -> {paths[i]}')
    
    # if size == 0: continue
    data_f.seek(offset, 0)
    data = data_f.read(size)
    assert crc == crc32(data)
    
    if size != 0 and decomp_size == 0: # ns, no lzss compressed
        pass
    elif size != 0 and decomp_size != 0: #steam, lzss compressed
        data = hlzsdecomp(io.BytesIO(data))
        assert len(data) == decomp_size
        assert decomp_crc == crc32(data)
    elif size == 0: # empty file
        pass
    
    p = (Path(f'{packname}_out') / (f"{i:03d}."+paths[i].replace('/', '__'))).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('wb') as item_f:
        item_f.write(data)