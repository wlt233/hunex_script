$pythonPath = "$env:LOCALAPPDATA/Programs/Python/Python39/python.exe"

& $pythonPath "$PWD/compiler.py" "$PWD/test.txt"; 
# & $pythonPath "$PWD/hese_dasm.py";
& $pythonPath "$PWD/hunex_script.py" "$PWD/script";
Copy-Item -Path "$PWD/script.heslnk" -Destination "$env:APPDATA/Ryujinx/mods/contents/0100a9c021d98000/romfs/Data/StreamingAssets/script" -Force;

G:/20250218_tokimap/ryujinx-1.2.82-win_x64/Ryujinx.exe;