# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['qianduan.py','kbqa_test.py','entity_extractor.py','getQuestion.py','search_answer.py'],
             pathex=['F:\\Python_test\\QASystemOnBasketballGraph_master'],
             binaries=[],
             datas=[('F:\Anaconda\envs\py36\Lib\site-packages\eel\\eel.js', 'eel'),('F:\Anaconda\envs\py36\Lib\site-packages\py2neo\__init__.py','py2neo'),
             ('web', 'web'),('F:\Anaconda\envs\py36\Lib\site-packages\jieba\__init__.py','jieba'),('F:\Anaconda\envs\py36\Lib\site-packages\sklearn','sklearn')],
             hiddenimports=['bottle_websocket'],
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
          name='qianduan',
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
               name='qianduan')
