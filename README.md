# Hunex Script

several wheels for Hunex Engine games, only tested on Nijigasaki VN (にじちず) ([Switch Demo](https://gitea.tqlwsl.moe/wlt233/nijichizu_heslnk)) and Steam ver

remember to `pip install pylzss` before use

## hdlg: text translate file

.hdlg (dialog binary lzss-compressed) -> .hdgl (dialog binary) -> .txt (text lines)

## heslnk: scene script bundle file

.heslnk (script link bundle) -> .hese (script binary) -> .dasm (disassembled) -> .txt (dialog content)

- `heslunpack.py`: from https://gist.github.com/kjy00302/cce541058c1698f2eb6e3d9d7d34da17
- `hunex_script.py`: pack dir to heslnk, code by k
- `hese_dasm.py`: disassemble hese and parse dialog contents

you may change code below in `hese_dasm.py` before use on other Hunex games (Meikoi etc.):

- opcode (`hunex.UNAS.ADV.unas_code.eUNAS_CODE`)
- function code (`hunex.UNAS.ADV.Script.eUNAS_SCRIPT_CODE`)
- name tag, select dialog function offset (or param)

## hpb/hph: assetbundles' bundle and header file

.hpb/hph -> index.filename(replaced / to __) (assetbundle)

- `hpb_unpack.py`: modded from https://gist.github.com/kjy00302/34461f7ced79be7c48e3d46ae94f047b
- `hpb_pack.py`: pack hpb/hph from unpack output dir (switch)
- `hpb_pack_lzss.py`: pack with lzss compression (steam)
- `batch_pack_ab.py`: batch replace images of output assetbundles (for steam ver)

## hese_maker: messy code to make a fanmade scene script

- `compiler.py`: not a compiler
- `ayumu_birthday.txt`: see https://www.bilibili.com/video/BV1Bv9hYZEGh/

## credit

- https://gist.github.com/kjy00302
- https://github.com/YuriSizuku/GalgameReverse/tree/master/project/hunex/src
