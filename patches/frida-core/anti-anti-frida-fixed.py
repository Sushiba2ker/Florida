"""
Florida anti-anti-frida.py - FIXED VERSION
============================================
Fix: Bao ve symbols cua Java bridge de Java API hoat dong.
 
Nguyen nhan goc: Phien ban cu rename TAT CA symbols chua "frida",
bao gom ca Java bridge init functions. Khi do, Java bridge 
khong the khoi tao -> Java undefined trong script.

Cach dung: Thay the file anti-anti-frida.py trong frida-core/src/
bang file nay truoc khi build.
"""

import lief
import sys
import random
import os

# Symbols CAN THIET cho Java bridge hoat dong
# Khong duoc rename nhung symbols nay!
JAVA_BRIDGE_KEYWORDS = [
    "_java",        # frida_java_init, frida_java_dispose, etc.
    "_jvm",         # JVM-related functions
    "java_bridge",  # Java bridge module functions
    "_jni",         # JNI bridge functions
    "ClassFactory", # Class loading
    "dalvik",       # Dalvik VM interaction
    "art_",         # ART runtime functions
]

def should_skip_rename(symbol_name):
    """Kiem tra symbol co thuoc Java bridge khong"""
    name_lower = symbol_name.lower()
    for keyword in JAVA_BRIDGE_KEYWORDS:
        if keyword.lower() in name_lower:
            return True
    return False

if __name__ == "__main__":
    input_file = sys.argv[1]
    print(f"[*] Patch frida-agent: {input_file}")
    random_name = "".join(random.sample("ABCDEFGHIJKLMNO", 5))
    print(f"[*] Patch `frida` to `{random_name}`")

    binary = lief.parse(input_file)

    if not binary:
        exit()

    renamed_count = 0
    skipped_count = 0

    for symbol in binary.symbols:
        if symbol.name == "frida_agent_main":
            symbol.name = "main"
            renamed_count += 1
            continue

        if "frida" in symbol.name:
            if should_skip_rename(symbol.name):
                skipped_count += 1
                # print(f"  [SKIP] {symbol.name}")  # Uncomment de debug
            else:
                symbol.name = symbol.name.replace("frida", random_name)
                renamed_count += 1

        if "FRIDA" in symbol.name:
            if should_skip_rename(symbol.name):
                skipped_count += 1
            else:
                symbol.name = symbol.name.replace("FRIDA", random_name)
                renamed_count += 1

    print(f"[*] Renamed {renamed_count} symbols, skipped {skipped_count} (Java bridge)")
    binary.write(input_file)

    # gum-js-loop thread (11 chars -> 11 chars, safe)
    random_name = "".join(random.sample("abcdefghijklmn", 11))
    print(f"[*] Patch `gum-js-loop` to `{random_name}`")
    os.system(f"sed -b -i s/gum-js-loop/{random_name}/g {input_file}")

    # gmain thread (5 chars -> 5 chars, safe)
    random_name = "".join(random.sample("abcdefghijklmn", 5))
    print(f"[*] Patch `gmain` to `{random_name}`")
    os.system(f"sed -b -i s/gmain/{random_name}/g {input_file}")
