# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import mip
mip_path = mip.__path__[0]
print(mip.__path__)

import os
binaries = []
if os.name == 'nt':
    binaries.append((mip_path+'/libraries/win64/*', 'mip/libraries/win64'))
else:
    binaries.append((mip_path+'/libraries/lin64/*', 'mip/libraries/lin64/'))

binaries.append((mip_path+'/libraries/cbc-c-darwin-x86-64.dylib', 'mip/libraries'))

a = Analysis(['scripts/main.py'],
             pathex=["pySprida"],
             binaries=binaries,
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
