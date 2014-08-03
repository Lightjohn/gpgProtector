from setuptools import setup

APP = ['gui.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True,
 'includes': ['sip', 'PyQt4','gpg','gui']}

setup(
app=APP,
data_files=DATA_FILES,
options={'py2app': OPTIONS},
setup_requires=['py2app'],
)
