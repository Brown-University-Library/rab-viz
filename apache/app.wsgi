import os
import sys

#parent dir
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#python3 modification
#https://stackoverflow.com/questions/25020451/no-activate-this-py-file-in-venv-pyvenv
activate_this = os.path.join(path, 'venv/bin/activate_this.py')
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

if path not in sys.path:
  sys.path.append(path)

from rabviz.service import app as application
