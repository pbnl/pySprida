# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import mip
from os.path import dirname
pathmip = dirname(mip.__file__)
mippathlib = os.path.join(pathmip, "libraries")

a = Analysis(['scripts/main.py'],
             pathex=['pySprida'],
             binaries=[
             (f"{mippathlib}/win64/*",
              'mip/libraries/win64'),
              (f"{mippathlib}/lin64/*",
               'mip/libraries/lin64/'),
               (f"{mippathlib}/*",
                'mip/libraries')],
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
               name='pySprida')
