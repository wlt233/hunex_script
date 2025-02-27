
import os
import struct
import sys

# code by wlt233 | 2025.02.25

eUNAS_SCRIPT_CODE = {
    0x00: "UNAS_COMMAND_CODE_TEXT",
    0x01: "UNAS_COMMAND_CODE_TEXT2", # 8bytes param
    0x02: "UNAS_COMMAND_CODE_TEXT_ADD",
    0x03: "UNAS_COMMAND_CODE_TEXT_ADD2",
    0x04: "UNAS_COMMAND_CODE_FLUSH_TEXT",
    0x05: "UNAS_COMMAND_CODE_READ_FLAG",
    0x06: "UNAS_FUNCTION_CODE_CLEAR_TEXT",
    0x07: "UNAS_FUNCTION_CODE_FAMILY_NAME",
    0x08: "UNAS_FUNCTION_CODE_FIRST_NAME",
    0x09: "UNAS_FUNCTION_CODE_USER_NAME",
    0x0a: "UNAS_FUNCTION_CODE_GET_NAME_ID",
    0x0b: "UNAS_FUNCTION_CODE_NAME_TAG",
    0x0c: "UNAS_FUNCTION_CODE_NAME_TAG2",
    0x0d: "UNAS_FUNCTION_CODE_SET_DIALOG",
    0x0e: "UNAS_FUNCTION_CODE_ROLLBACK_POINT",
    0x0f: "UNAS_FUNCTION_CODE_GET_KEY",
    0x10: "UNAS_COMMAND_CODE_WAIT_KEY_TOUCH",
    0x11: "UNAS_FUNCTION_CODE_KEY_WAIT",
    0x12: "UNAS_FUNCTION_CODE_KEY_WAIT_TIME",
    0x13: "UNAS_FUNCTION_CODE_VOICE_WAIT",
    0x14: "UNAS_FUNCTION_CODE_WAIT",
    0x15: "UNAS_FUNCTION_CODE_WAIT_CAMERA",
    0x16: "UNAS_FUNCTION_CODE_WAIT_MOVIE",
    0x17: "UNAS_FUNCTION_CODE_WAIT_OBJECT",
    0x18: "UNAS_FUNCTION_CODE_WAIT_SEPIA",
    0x19: "UNAS_FUNCTION_CODE_WAIT_TASK",
    0x1a: "UNAS_FUNCTION_CODE_WAIT_TIME",
    0x1b: "UNAS_FUNCTION_CODE_WAIT_TRANSITION",
    0x1c: "UNAS_FUNCTION_CODE_WAIT_WINDOW",
    0x1d: "UNAS_COMMAND_CODE_GET_ACTIVE_WINDOW",
    0x1e: "UNAS_FUNCTION_CODE_SET_ACTIVE_WINDOW",
    0x1f: "UNAS_FUNCTION_CODE_TEXT_WINDOW",
    0x20: "UNAS_FUNCTION_CODE_WINDOW_GET_POSITION",
    0x21: "UNAS_FUNCTION_CODE_WINDOW_SET_POSITION",
    0x22: "UNAS_FUNCTION_CODE_WINDOW_MOVE_POSITION",
    0x23: "UNAS_FUNCTION_CODE_SNS_START",
    0x24: "UNAS_FUNCTION_CODE_SNS_FINISH",
    0x25: "UNAS_FUNCTION_CODE_SNS_ADDICON",
    0x26: "UNAS_FUNCTION_CODE_SNS_ADDNAME",
    0x27: "UNAS_FUNCTION_CODE_SNS_ADDNAME2",
    0x28: "UNAS_FUNCTION_CODE_SNS_ADDCHAT",
    0x29: "UNAS_FUNCTION_CODE_SNS_ADDCHAT2",
    0x2a: "UNAS_FUNCTION_CODE_SNS_ADDSTAMP",
    0x2b: "UNAS_FUNCTION_CODE_SNS_VISIBLE",
    0x2c: "UNAS_FUNCTION_CODE_SNS_KEYWAIT",
    0x2d: "UNAS_FUNCTION_CODE_SNS_GET_STATE",
    0x2e: "UNAS_FUNCTION_CODE_AUDIO_GET_VOLUME",
    0x2f: "UNAS_FUNCTION_CODE_AUDIO_SET_MUTE",
    0x30: "UNAS_FUNCTION_CODE_AUDIO_SET_PANNING",
    0x31: "UNAS_FUNCTION_CODE_AUDIO_SET_VOLUME",
    0x32: "UNAS_FUNCTION_CODE_AUDIO_SET_SYSVOLUME",
    0x33: "UNAS_FUNCTION_CODE_AUDIO_IS_PLAY",
    0x34: "UNAS_FUNCTION_CODE_BGM_PLAY",
    0x35: "UNAS_FUNCTION_CODE_SE_PLAY",
    0x36: "UNAS_FUNCTION_CODE_SE_ATTACH_PAD",
    0x37: "UNAS_FUNCTION_CODE_VOICE_PLAY",
    0x38: "UNAS_FUNCTION_CODE_VOICE_ATTACH",
    0x39: "UNAS_FUNCTION_CODE_VOICE_SET_CONFIG_NAME",
    0x3a: "UNAS_FUNCTION_CODE_CAMERA_SELECT",
    0x3b: "UNAS_FUNCTION_CODE_CAMERA_TRANS",
    0x3c: "UNAS_FUNCTION_CODE_CAMERA_GET_PARAM",
    0x3d: "UNAS_FUNCTION_CODE_CAMERA_SET_PARAM",
    0x3e: "UNAS_FUNCTION_CODE_CAMERA_MOVE",
    0x3f: "UNAS_FUNCTION_CODE_GET_SCREEN_TO_WORLD",
    0x40: "UNAS_FUNCTION_CODE_GET_WORLD_TO_SCREEN",
    0x41: "UNAS_FUNCTION_CODE_FADE",
    0x42: "UNAS_FUNCTION_CODE_FADE_PRIORITY",
    0x43: "UNAS_FUNCTION_CODE_GET_AMBIENT_COLOR",
    0x44: "UNAS_FUNCTION_CODE_SET_AMBIENT_COLOR",
    0x45: "UNAS_FUNCTION_CODE_MOVE_AMBIENT_COLOR",
    0x46: "UNAS_FUNCTION_CODE_GET_BLEND",
    0x47: "UNAS_FUNCTION_CODE_SET_BLEND",
    0x48: "UNAS_FUNCTION_CODE_SEPIA",
    0x49: "UNAS_FUNCTION_CODE_SEPIA_PRIORITY",
    0x4a: "UNAS_FUNCTION_CODE_IS_SEPIA",
    0x4b: "UNAS_FUNCTION_CODE_GET_SEPIA",
    0x4c: "UNAS_FUNCTION_CODE_SET_SEPIA",
    0x4d: "UNAS_FUNCTION_CODE_MOVE_SEPIA",
    0x4e: "UNAS_FUNCTION_CODE_SCREEN_SPIRAL",
    0x4f: "UNAS_FUNCTION_CODE_IS_SCREEN_SPIRAL",
    0x50: "UNAS_FUNCTION_CODE_GET_SCREEN_SPIRAL",
    0x51: "UNAS_FUNCTION_CODE_SET_SCREEN_SPIRAL",
    0x52: "UNAS_FUNCTION_CODE_MOVE_SCREEN_SPIRAL",
    0x53: "UNAS_FUNCTION_CODE_SCREEN_RASTER",
    0x54: "UNAS_FUNCTION_CODE_IS_SCREEN_RASTER",
    0x55: "UNAS_FUNCTION_CODE_GET_SCREEN_RASTER",
    0x56: "UNAS_FUNCTION_CODE_SET_SCREEN_RASTER",
    0x57: "UNAS_FUNCTION_CODE_MOVE_SCREEN_RASTER",
    0x58: "UNAS_FUNCTION_CODE_SCREEN_RIPPLE",
    0x59: "UNAS_FUNCTION_CODE_IS_SCREEN_RIPPLE",
    0x5a: "UNAS_FUNCTION_CODE_GET_SCREEN_RIPPLE",
    0x5b: "UNAS_FUNCTION_CODE_SET_SCREEN_RIPPLE",
    0x5c: "UNAS_FUNCTION_CODE_SHAKE",
    0x5d: "UNAS_FUNCTION_CODE_TRANSITION",
    0x5e: "UNAS_FUNCTION_CODE_TURNPAGE_TRANSITION",
    0x5f: "UNAS_FUNCTION_CODE_AUTOSAVE",
    0x60: "UNAS_FUNCTION_CODE_QUICKSAVE",
    0x61: "UNAS_FUNCTION_CODE_SYSTEMSAVE",
    0x62: "UNAS_FUNCTION_CODE_POPUP",
    0x63: "UNAS_FUNCTION_CODE_AUTOSKIPICON_DISP",
    0x64: "UNAS_FUNCTION_CODE_MOVIE_CANCEL_BUTTON",
    0x65: "UNAS_FUNCTION_CODE_MOVIE_LOAD",
    0x66: "UNAS_FUNCTION_CODE_MOVIE_START",
    0x67: "UNAS_FUNCTION_CODE_MOVIE_STOP",
    0x68: "UNAS_FUNCTION_CODE_NOISE_SET",
    0x69: "UNAS_FUNCTION_CODE_NOISE_SET_PARAM",
    0x6a: "UNAS_FUNCTION_CODE_NOISE_GET_PARAM",
    0x6b: "UNAS_FUNCTION_CODE_NOISE_MOVE_PARAM",
    0x6c: "UNAS_FUNCTION_CODE_NOISE_STOP_PARAM",
    0x6d: "UNAS_FUNCTION_CODE_GET_ASSET_FLAG",
    0x6e: "UNAS_FUNCTION_CODE_GET_FLAG",
    0x6f: "UNAS_FUNCTION_CODE_SET_FLAG",
    0x70: "UNAS_FUNCTION_CODE_GET_INT_PARAM",
    0x71: "UNAS_FUNCTION_CODE_SET_INT_PARAM",
    0x72: "UNAS_FUNCTION_CODE_GET_FLOAT_PARAM",
    0x73: "UNAS_FUNCTION_CODE_SET_FLOAT_PARAM",
    0x74: "UNAS_FUNCTION_CODE_GET_STR_PARAM",
    0x75: "UNAS_FUNCTION_CODE_SET_STR_PARAM",
    0x76: "UNAS_FUNCTION_CODE_CALL_TASK",
    0x77: "UNAS_FUNCTION_CODE_PROCESS_START",
    0x78: "UNAS_FUNCTION_CODE_PROCESS_STOP",
    0x79: "UNAS_FUNCTION_CODE_PROCESS_RESUME",
    0x7a: "UNAS_FUNCTION_CODE_PROCESS_SUSPEND",
    0x7b: "UNAS_COMMAND_CODE_SELECT_GET",
    0x7c: "UNAS_FUNCTION_CODE_SELECT",
    0x7d: "UNAS_FUNCTION_CODE_SELECT_GET_PARAM",
    0x7e: "UNAS_FUNCTION_CODE_STOP_SYSTEM",
    0x7f: "UNAS_FUNCTION_CODE_STOP_AMBIENT_COLOR",
    0x80: "UNAS_FUNCTION_CODE_STOP_CAMERA",
    0x81: "UNAS_FUNCTION_CODE_STOP_CHAPTER_JUMP",
    0x82: "UNAS_FUNCTION_CODE_STOP_FILTER",
    0x83: "UNAS_FUNCTION_CODE_STOP_PRELOAD",
    0x84: "UNAS_FUNCTION_CODE_STOP_SEPIA",
    0x85: "UNAS_FUNCTION_CODE_STOP_SKIP",
    0x86: "UNAS_COMMAND_CODE_GET_SKIP",
    0x87: "UNAS_COMMAND_CODE_GET_STEPTIME",
    0x88: "UNAS_FUNCTION_CODE_CHAPTER",
    0x89: "UNAS_FUNCTION_CODE_CHAPTER_TITLE",
    0x8a: "UNAS_FUNCTION_CODE_CHAPTER_TITLE2",
    0x8b: "UNAS_FUNCTION_CODE_GET_FILE_NO",
    0x8c: "UNAS_FUNCTION_CODE_GET_LANGUAGE",
    0x8d: "UNAS_FUNCTION_CODE_IS_DEFAULT_NAME",
    0x8e: "UNAS_FUNCTION_CODE_RANDOM_FLOAT",
    0x8f: "UNAS_FUNCTION_CODE_RANDOM_INT",
    0x90: "UNAS_FUNCTION_CODE_SCRIPT_JUMP",
    0x91: "UNAS_FUNCTION_CODE_SET_STEPTIME",
    0x92: "UNAS_FUNCTION_CODE_ANIMATOR_PLAY",
    0x93: "UNAS_FUNCTION_CODE_ANIMATOR_GET_INTEGER",
    0x94: "UNAS_FUNCTION_CODE_ANIMATOR_GET_FLOAT",
    0x95: "UNAS_FUNCTION_CODE_ANIMATOR_SET_INTEGER",
    0x96: "UNAS_FUNCTION_CODE_ANIMATOR_SET_FLOAT",
    0x97: "UNAS_FUNCTION_CODE_OBJECT_SET",
    0x98: "UNAS_FUNCTION_CODE_OBJECT_KILL",
    0x99: "UNAS_FUNCTION_CODE_OBJECT_READY",
    0x9a: "UNAS_FUNCTION_CODE_OBJECT_START",
    0x9b: "UNAS_FUNCTION_CODE_OBJECT_ADD_TEXTURE",
    0x9c: "UNAS_FUNCTION_CODE_OBJECT_GET_COLOR",
    0x9d: "UNAS_FUNCTION_CODE_OBJECT_GET_ID",
    0x9e: "UNAS_FUNCTION_CODE_OBJECT_GET_KEY",
    0x9f: "UNAS_FUNCTION_CODE_OBJECT_GET_FILENAME",
    0xa0: "UNAS_FUNCTION_CODE_OBJECT_GET_PARAM",
    0xa1: "UNAS_FUNCTION_CODE_OBJECT_GET_PRIORITY",
    0xa2: "UNAS_FUNCTION_CODE_OBJECT_GET_TYPE",
    0xa3: "UNAS_FUNCTION_CODE_OBJECT_SET_ALPHATEST",
    0xa4: "UNAS_FUNCTION_CODE_OBJECT_SET_COLOR",
    0xa5: "UNAS_FUNCTION_CODE_OBJECT_SET_DISPLAY",
    0xa6: "UNAS_FUNCTION_CODE_OBJECT_SET_ID",
    0xa7: "UNAS_FUNCTION_CODE_OBJECT_SET_MASK",
    0xa8: "UNAS_FUNCTION_CODE_OBJECT_SET_PARAM",
    0xa9: "UNAS_FUNCTION_CODE_OBJECT_SET_PATH",
    0xaa: "UNAS_FUNCTION_CODE_OBJECT_SET_PRIORITY",
    0xab: "UNAS_FUNCTION_CODE_OBJECT_MOVE_COLOR",
    0xac: "UNAS_FUNCTION_CODE_OBJECT_MOVE_PARAM",
    0xad: "UNAS_FUNCTION_CODE_OBJECT_START_PATH",
    0xae: "UNAS_FUNCTION_CODE_OBJECT_STOP_COLOR",
    0xaf: "UNAS_FUNCTION_CODE_OBJECT_STOP_PARAM",
    0xb0: "UNAS_FUNCTION_CODE_OBJECT_PAUSE_PARAM",
    0xb1: "UNAS_FUNCTION_CODE_OBJECT_COPY_TEXTURE",
    0xb2: "UNAS_FUNCTION_CODE_STAND_GET_SIZE",
    0xb3: "UNAS_FUNCTION_CODE_STAND_GET_FACE",
    0xb4: "UNAS_FUNCTION_CODE_STAND_SET_FACE",
    0xb5: "UNAS_FUNCTION_CODE_STAND_EYE_BLINK",
    0xb6: "UNAS_FUNCTION_CODE_STAND_LIP_SYNC",
    0xb7: "UNAS_FUNCTION_CODE_STAND_LIP_SET",
    0xb8: "UNAS_FUNCTION_CODE_ITEM_SET_3D",
    0xb9: "UNAS_FUNCTION_CODE_ITEM_SET_ANIM",
    0xba: "UNAS_FUNCTION_CODE_ITEM_SET_PAGE",
    0xbb: "UNAS_FUNCTION_CODE_PARTICLE_SET",
    0xbc: "UNAS_FUNCTION_CODE_PARTICLE_PAUSE",
    0xbd: "UNAS_FUNCTION_CODE_PARTICLE_FINISH",
    0x2710: "UNAS_FUNCTION_CODE_USER_FREE",
}

eUNAS_CODE = {
    0x00: "NOP",
    0x01: "INC",
    0x02: "DEC",
    0x03: "NEG",
    0x04: "NOT",
    0x05: "ADD",
    0x06: "SUB",
    0x07: "MUL",
    0x08: "DIV",
    0x09: "MOD",
    0x0a: "AND",
    0x0b: "OR",
    0x0c: "XOR",
    0x0d: "REV",
    0x0e: "SAL",
    0x0f: "SAR",
    0x10: "LSS",
    0x11: "LEQ",
    0x12: "GRT",
    0x13: "GEQ",
    0x14: "EQU",
    0x15: "NEQ",
    0x16: "AND2",
    0x17: "OR2",
    0x18: "CAST",
    0x19: "CALL",
    0x1a: "FUNC",
    0x1b: "COM",
    0x1c: "DEL",
    0x1d: "JMP",
    0x1e: "JPT",
    0x1f: "JPF",
    0x20: "EQCMP",
    0x21: "LOD",
    0x22: "LDA",
    0x23: "LDI",
    0x24: "STO",
    0x25: "ADBR",
    0x26: "ADSP",
    0x27: "RET",
    0x28: "ASS",
    0x29: "ASSV",
    0x2a: "VAL",
    0x2b: "STOP",
    0x2c: "CRLF",
    0x2d: "STRING",
    0x2e: "DBVAR",
    0x2f: "DBST",
    0x30: "CHAR",
    0x31: "MAX",
}


def parse_instruction(data):
    assert data[0] == 0xA0
    
    opcode = data[1]
    opcode_name = eUNAS_CODE.get(opcode, f"UNKNOWN_OPCODE_{opcode:02x}")
    typ = struct.unpack('>h', data[2:4])[0]
    typ_name = {
        0x88: "FLOAT",
        0x90: "sp"
    }.get(typ, f"{data[2:4].hex(' ')}")
    info = f"{opcode_name}"
    
    if opcode == 0x1a or opcode == 0x1b: # FUNC COM
        v = struct.unpack('<I', data[4:8])[0]
        func = eUNAS_SCRIPT_CODE.get(v, f"UNK_FUNC_{v:08x}")
        info += f", {typ_name}, {func}"
        if len(data[8:]):
            for i in range(len(data[8:]) // 4):
                v = struct.unpack('<I', data[8+i*4:12+i*4])[0]
                info += f", {v:08x}"
    
    elif opcode == 0x2e: # DBVAR
        v = struct.unpack('<I', data[4:8])[0]
        k = data[8:].decode().rstrip("\0")
        info += f", {typ_name}, {v:08x}, {k}"
            
    elif opcode == 0x2d: # STRING
        info += ", " + data[2:].decode().rstrip("\0")
    
    else:
        if len(data) >= 8:
            if typ == 0x88:
                v = struct.unpack('<f', data[4:8])[0]
                info += f", {typ_name}, {v}"
            else:
                v = struct.unpack('<I', data[4:8])[0]
                info += f", {typ_name}, {v:08x}"
        else:
            info += f", {typ_name}"
    
    return info
    

def parse_hese(hese_path, output_path):
    with open(hese_path, 'rb') as f:
        magic, version, offset, unk2, unk3 = struct.unpack('<5I44x', f.read(64))
        assert magic == int.from_bytes(b'HESE', 'little')
        f.seek(offset, 0)
        data = f.read()
    
    with open(output_path, 'w', encoding="utf8") as f:
        starts = [] 
        for i, byte in enumerate(data):
            if byte != 0xA0 or i % 4: continue
            if data[i-1] == 0x90: continue
            p_i = starts[-1] if starts else -1
            if (starts and data[p_i] == 0xa0 and data[p_i + 1] == 0x1b and data[p_i + 4] == 0x01
                and i - p_i < 16):
                continue # workaround for COM
            starts.append(i)
            
        for i, start in enumerate(starts):
            end = starts[i+1] if i < len(starts) - 1 else len(data)
            chunk = data[start:end]
            f.write(f"{start:08x}: " + parse_instruction(chunk) + '\n')
                


NAME_TAG = { # 0000f594
    0x00: 0x0000019e,
    0x01: 0x000001a4,
    0x02: 0x000001a6,
    0x03: 0x000001a3,
    0x04: 0x000001bf,
    0x05: 0x000001ae,
    0x06: 0x000001ae,
    0x07: 0x000001ae,
    0x08: 0x000001ae,
    0x09: 0x000001ae,
    0x0a: 0x000001ae,
    0x0b: 0x000001ae,
    0x0c: 0x000001ae,
    0x0d: 0x000001ae,
    0x0e: 0x000001ae,
    0x0f: 0x000001ad,
    0x10: 0x000001ad,
    0x11: 0x000001ad,
    0x12: 0x000001ad,
    0x13: 0x000001ad,
    0x14: 0x000001ad,
    0x15: 0x000001ad,
    0x16: 0x000001ad,
    0x17: 0x000001ad,
    0x18: 0x000001ad,
    0x19: 0x000001ad,
    0x1a: 0x000001ad,
    0x1b: 0x000001d4,
    0x1c: 0x000001a1,
    0x1d: 0x000001b3,
    0x1e: 0x000001d6,
    0x1f: 0x000001d7,
    0x20: 0x000001cc,
    0x21: 0x000001cd,
    0x22: 0x000001d5,
    0x23: 0x000001b6,
    0x24: 0x000001bd,
    0x25: 0x000001a7,
    0x26: 0x000001a0,
    0x27: 0x000001db,
    0x28: 0x000001db,
    0x29: 0x000001db,
    0x2a: 0x000001db,
    0x2b: 0x000001db,
    0x2c: 0x000001db,
    0x2d: 0x000001db,
    0x2e: 0x000001db,
    0x2f: 0x000001db,
    0x30: 0x000001db,
    0x31: 0x000001db,
    0x32: 0x000001db,
    0x33: 0x0000019e,
    0x34: 0x000001c6,
    0x35: 0x000001c3,
    0x36: 0x000001d8,
    0x37: 0x000001c4,
    0x38: 0x000001bb,
    0x39: 0x000001c1,
    0x3a: 0x000001b5,
    0x3b: 0x000001b4,
    0x3c: 0x000001d3,
    0x3d: 0x000001c7,
    0x3e: 0x000001c8,
    0x3f: 0x000001c9,
    0x40: 0x000001ca,
    0x41: 0x000001cb,
    0x42: 0x000001ac,
    0x43: 0x000001b0,
    0x44: 0x000001b1,
    0x45: 0x000001b2,
    0x46: 0x000001c2,
    0x47: 0x000001a8,
    0x48: 0x000001a2,
    0x49: 0x000001d9,
    0x4a: 0x000001d9,
    0x4b: 0x000001b8,
    0x4c: 0x000001d1,
    0x4d: 0x000001a9,
    0x4e: 0x000001a5,
    0x4f: 0x0000019f,
    0x50: 0x000001ce,
    0x51: 0x000001d0,
    0x52: 0x000001aa,
    0x53: 0x000001bc,
    0x54: 0x000001be,
    0x55: 0x000001da,
    0x56: 0x000001cf,
    0x57: 0x000001c5,
    0x58: 0x000001c0,
    0x59: 0x000001d2,
    0x5a: 0x000001b7,
    0x5b: 0x000001ba,
    0x5c: 0x000001ba,
    0x5d: 0x000001ba,
    0x5e: 0x000001ba,
    0x5f: 0x000001b9,
    0x60: 0x000001b9,
    0x61: 0x000001b9,
    0x62: 0x000001b9,
    0x63: 0x000001b9,
    0x64: 0x000001ab,
    0x65: 0x000001ab,
    0x66: 0x000001ab,
    0x67: 0x000001ab,
}

with open("script_dialog_ja.hdlg.txt", "r", encoding="utf-8") as f:
    DIALOG = f.readlines()

def get_dialog(no):
    return DIALOG[no].strip()



def parse_dasm(dasm_path, output_path):
    print(f"{file_name}", end="")
    with open(dasm_path, 'rb') as f:
        instructions = f.readlines()
        
    with open(output_path, 'w', encoding="utf8") as f:
        for i, instruction in enumerate(instructions):
            instruction = instruction.decode().strip()
            
            if "CALL, sp, 0000f594" in instruction: # NAME_TAG
                param_instruction = instructions[i-2].decode().strip()
                param = NAME_TAG[int(param_instruction.split(", ")[-1], 16)]
                name_tag = get_dialog(param)
                f.write(f"{param:04x} {name_tag}:\n")
            
            if "CALL, sp, 0000ce58" in instruction: # select
                param_instruction = instructions[i-5].decode().strip()
                param = int(param_instruction.split(", ")[-1], 16)
                select = get_dialog(param)
                f.write(f"{param:04x} select: {select}:\n")
            
            if "UNAS_COMMAND_CODE_TEXT2" in instruction:
                param = int(instruction.split(", ")[-1], 16)
                text = get_dialog(param)
                f.write(f"{param:04x} {text}\n\n")
            
            if "CALL, sp, 0001ca10" in instruction: # chat opponent
                param_instruction = instructions[i-3].decode().strip()
                param = int(param_instruction.split(", ")[-1], 16)
                select = get_dialog(param)
                param2_instruction = instructions[i-4].decode().strip()
                param2 = int(param2_instruction.split(", ")[-1], 16)
                name_tag = get_dialog(param2)
                f.write(f"{param2:04x} {name_tag}:\n")
                f.write(f"{param:04x} {select}:\n\n")
                
            if "CALL, sp, 0001cabc" in instruction: # chat self
                param_instruction = instructions[i-3].decode().strip()
                param = int(param_instruction.split(", ")[-1], 16)
                select = get_dialog(param)
                param2_instruction = instructions[i-4].decode().strip()
                param2 = int(param2_instruction.split(", ")[-1], 16)
                name_tag = get_dialog(param2)
                f.write(f"{param2:04x} {name_tag}:\n")
                f.write(f"{param:04x} {select}:\n\n")

    
    print(" parsed")






if __name__ == "__main__":
    if not os.path.exists("dasm"): os.makedirs("dasm")
    if not os.path.exists("text"): os.makedirs("text")
    # for file_path in sys.argv[1:]:
    for root, dirs, files in os.walk("script.out_orig"):
        for file in files:
            if file.endswith(".hese"):
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                dasm_path = f"./dasm/{file_name}.dasm"
                text_path = f"./text/{file_name}.txt"
                parse_hese(file_path, dasm_path)
                parse_dasm(dasm_path, text_path)
    # os.system("pause")

