import os
import sys
path = '/home/bijur/hack/ralumni'
if path not in sys.path:
    sys.path.append(path)
from ralumni import app as application
