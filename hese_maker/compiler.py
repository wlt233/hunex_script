

import os
import struct
import sys


def pad(data, size):
    return data + b"\x00" * (size - (len(data) % size))

def LDI(value):
    if type(value) == int:
        return b"\xA0\x23\x00\x90" + struct.pack("<I", value)
    elif type(value) == float:
        return b"\xA0\x23\x00\x88" + struct.pack("<f", value)
def STRING(string):
    return pad(b"\xA0\x2D" + string.encode("utf-8"), 4)
def CALL(func):
    return b"\xA0\x19\x00\x90" + struct.pack("<I", func)
def COM(command, args=[]):
    b = b"\xA0\x1B\x00\x90" + struct.pack("<I", command)
    for arg in args: b += struct.pack("<I", arg)
    return b
def FUNC(func):
    return b"\xA0\x1A\x00\x90" + struct.pack("<I", func)


def command_trans(offset, t=1.0, filename=""):
    inst = [
        LDI(offset + 0x8),
        STRING(filename),
        LDI(t),
        LDI(0x40),
        LDI(0x1),
        LDI(0x4),
        CALL(0x0000b274),
    ]
    return b"".join(inst)

def _waitkey(offset):
    inst = [
        LDI(0x1),
        LDI(0x1),
        CALL(0x00015ee0),
    ]
    return b"".join(inst)


def command_background(offset, bg_name, t=1.0, rule=""):
    inst = [
        LDI(offset + 0x8),
        STRING(bg_name),
        LDI(0x1),
        CALL(0x00011298),
    ]
    b = b"".join(inst)
    offset += len(b)
    return b + command_trans(offset, t, rule)

# def command_bgwait(offset, bg_name, t1=1.0, t2=1.0):
#     inst = [
#         LDI(0x2),
#         LDI(0x1),
#         LDI(t2),
#         LDI(0x1),
#         LDI(0x4),
#         CALL(0x0000ba30),
#     ]
#     return command_bg(offset, bg_name, t1) + b"".join(inst)


def command_bgm(offset, bgm_name):
    inst = [
        LDI(offset + 0x8),
        STRING(bgm_name),
        LDI(0x1),
        LDI(0.0),
        LDI(0.0),
        LDI(0.0),
        LDI(0x5),
        CALL(0x0000d584),
    ]
    return b"".join(inst)


def command_nametag(offset, tag_id):
    inst = [
        LDI(tag_id),
        LDI(0x1),
        CALL(0x0000f594),
    ]
    return b"".join(inst)

def command_text(offset, text_id, dialog_id):
    inst = [
        COM(0x01, [text_id, dialog_id]), # 0x01: UNAS_COMMAND_CODE_TEXT2
    ]
    return b"".join(inst) + _waitkey(offset)

def command_hidetext(offset, t=1.0):
    inst = [
        LDI(t),
        LDI(0x1),
        CALL(0x00015d9c),
    ]
    b = b"".join(inst)
    offset += len(b)
    return b + command_trans(offset, t)

def command_wait(offset, t=1.0):
    inst = [
        LDI(t),
        LDI(0x0),
        LDI(0x2),
        FUNC(0x1A), # 0x1A: UNAS_FUNCTION_CODE_WAIT_TIME
    ]
    return b"".join(inst)

def command_sepia(offset, color=1, t=1.0):
    inst = [
        LDI(0xffffffff),
        LDI(color), # 0x1 brown 0x0 grey
        LDI(0x2),
        CALL(0x0000974c),
        LDI(0xffffffff),
        LDI(0.0),
        LDI(t),
        LDI(0x1),
        LDI(0x4),
        CALL(0x00009f64),
    ]
    return b"".join(inst)

def command_bgmstop(offset, t=1.0):
    inst = [
        LDI(t),
        LDI(0x1),
        CALL(0x0000d630),
    ]
    return b"".join(inst)

def command_speech(offset, sound_name):
    inst = [
        LDI(0x0a),
        LDI(0xffffd8f1),
        LDI(offset + 0x8 * 3),
        STRING(sound_name),
        LDI(0x1),
        LDI(0xffffffff),
        LDI(0x5),
        CALL(0x00015f44),
    ]
    return b"".join(inst)

def command_character(offset, chara_name, position, oid=0):
    position_func = { # left to right
        "": 0x000115d8, # ?
        "1/2": 0x0001193c,
        "2/2": 0x00011b0c,
        "1/3": 0x00011ecc,
        "2/3": 0x0001209c,
        "3/3": 0x0001226c,
        "1/4": 0x0001243c,
        "2/4": 0x0001260c,
        "3/4": 0x000127dc,
        "4/4": 0x000129ac,
        "1/5": 0x00012b7c,
        "2/5": 0x00012d40,
        "3/5": 0x00012f04,
        "4/5": 0x000130c8,
        "5/5": 0x0001328c,
    }[position]
    oid = int(position.split('/')[0]) if not oid else oid
    inst = [
        LDI(oid), # object id
        LDI(offset + 0x8 * 2),
        STRING(chara_name),
        LDI(0xffffffff),
        LDI(0x3),
        CALL(position_func),
    ]
    b = b"".join(inst)
    offset += len(b)
    return b# + command_trans(offset, 0.3)

def command_clearchara(offset):
    inst = [
        LDI(0xffffffff),
        LDI(0x0),
        LDI(0x2),
        CALL(0x000024d0),
    ]
    return b"".join(inst)

def command_se(offset, se_name):
    inst = [
        LDI(0x4),
        LDI(offset + 0x8 * 2),
        STRING(se_name),
        LDI(0x1),
        LDI(0.0),
        LDI(0x4),
        CALL(0x0000d818),
    ]
    return b"".join(inst)

def command_shake(offset, t=1.0):
    inst = [
        LDI(5.0),
        LDI(t),
        LDI(28.0),
        LDI(10.0),
        LDI(0x5),
        LDI(0x0),
        LDI(0x6),
        CALL(0x0000164bc),
    ]
    return b"".join(inst)











def compile_hese(script_path, output_path):
    with open(script_path, "r", encoding="utf8") as f:
        script = f.readlines()
    
    with open("template.hese", "rb") as f:
        template = f.read()
    hearder, content = template[:0x40], template[0x40:]
    
    text_id = 0
    for line in script:
        line = line.strip()
        if not line: continue
        if line.startswith("#"): continue
        args = [arg.strip() for arg in line.split(",")]
        offset = len(content)
        
        if args[0] == "TRANS":
            content += command_trans(offset, float(args[1]))
        if args[0] == "BACKGROUND":
            content += command_background(offset, args[1], float(args[2]), args[3] if len(args) > 3 else "")
        # if args[0] == "BGWAIT":
        #     content += command_bgwait(offset, args[1], float(args[2]), float(args[3]))
        if args[0] == "BGM":
            content += command_bgm(offset, args[1])
        
        if args[0] == "NAMETAG":
            content += command_nametag(offset, int(args[1]))
            
        if args[0] == "TEXT":
            content += command_text(offset, text_id, int(args[1]))
            text_id += 1
            
        if args[0] == "HIDETEXT":
            content += command_hidetext(offset, float(args[1]))
            
        if args[0] == "WAIT":
            content += command_wait(offset, float(args[1]))
            
        if args[0] == "SEPIA":
            content += command_sepia(offset, int(args[1]), float(args[2]))
        
        if args[0] == "BGMSTOP":
            content += command_bgmstop(offset, float(args[1]))
            
        if args[0] == "SPEECH":
            content += command_speech(offset, args[1])
        
        if args[0] == "CHARACTER":
            content += command_character(offset, args[1], args[2], int(args[3]) if len(args) > 3 else 0)
        
        if args[0] == "CLEARCHARA":
            content += command_clearchara(offset)
        
        if args[0] == "SE":
            content += command_se(offset, args[1])
        
        if args[0] == "SHAKE":
            content += command_shake(offset, float(args[1]))
        
        
        
        
        
        
        
        
        
    content += bytes.fromhex("A0 27 00 04 00 00 00 00") # RET
    with open(output_path, "wb") as f:
        f.write(hearder + content)








if __name__ == "__main__":
    for script_path in sys.argv[1:]:
        #output_path = script_path + ".hese"
        if not os.path.exists("script"): os.mkdir("script")
        output_path = "script/sc_pro_0010.hese"
        compile_hese(script_path, output_path)
    #os.system("pause")

