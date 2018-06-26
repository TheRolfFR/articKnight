# -*- mode: python -*-

block_cipher = None


a = Analysis(['jeu.py'],
             pathex=['C:\\Users\\Yann\\Desktop\\TheRolf\\Python\\projet ISN'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='jeu',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='C:\\Users\\Yann\\Desktop\\TheRolf\\Python\\projet ISN\\icon.ico')
