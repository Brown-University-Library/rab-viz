import os
import sys

#parent dir
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if path not in sys.path:
  sys.path.append(path)

from rabviz.service import app as application
