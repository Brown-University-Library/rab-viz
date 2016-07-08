import os
import sys

#base_dir = os.path.dirname(os.path.abspath(__file__))
#parent dir
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#back up one
#path = os.path.dirname(path)

activate_this = os.path.join(path, 'venv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

if path not in sys.path:
  sys.path.append(path)

from app import app as application
