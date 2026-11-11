import os
import sys


# 1. Get the absolute directory where conftest.py lives
PROJECT_ROOT = os.path.join(os.path.dirname(__file__),'..')
print(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)
# 2. Add it to sys.path so tests can import your app modules directly


