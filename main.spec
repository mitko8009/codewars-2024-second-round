# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui/main.ui', 'ui'),
        ('ui/settings.ui', 'ui'),
        ('ui/theme.qss', 'ui'),
        ('assets/icon.png', 'assets'),
        ('assets/branch-closed.png', 'assets'),
        ('assets/branch-open.png', 'assets'),
        ('assets/checkbox-check.png', 'assets'),
        ('assets/checkbox-check-disabled.png', 'assets'),
        ('assets/combobox-down.png', 'assets'),
        ('assets/scrollbar-down.png', 'assets'),
        ('assets/scrollbar-down-disabled.png', 'assets'),
        ('assets/scrollbar-down-hover.png', 'assets'),
        ('assets/scrollbar-left.png', 'assets'),
        ('assets/scrollbar-left-disabled.png', 'assets'),
        ('assets/scrollbar-left-hover.png', 'assets'),
        ('assets/scrollbar-right.png', 'assets'),
        ('assets/scrollbar-right-disabled.png', 'assets'),
        ('assets/scrollbar-right-hover.png', 'assets'),
        ('assets/scrollbar-up.png', 'assets'),
        ('assets/scrollbar-up-disabled.png', 'assets'),
        ('assets/scrollbar-up-hover.png', 'assets'),
        ('assets/sort-asc.png', 'assets'),
        ('assets/sort-desc.png', 'assets'),
        ('assets/spinner-down.png', 'assets'),
        ('assets/spinner-up.png', 'assets'),
        ('assets/sub-menu-arrow.png', 'assets'),
        ('assets/sub-menu-arrow-hover.png', 'assets'),
        ('static/style.css', 'static'),
        ('static/script.js', 'static'),
        ('static/password.html', 'static'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
