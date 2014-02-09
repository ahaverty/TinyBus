# -*- mode: python -*-
a = Analysis(['dublinbusspider.py'],
             pathex=['C:\\Users\\Alan\\PycharmProjects\\TinyBus\\scrapy\\scrapy\\DublinBusSpider\\DublinBusSpider\\spiders'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='dublinbusspider.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='dublinbusspider')
