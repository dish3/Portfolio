"""NOVA AI Portfolio OS — Backend API Application."""

import sys
from pathlib import Path

# Ensure both apps/api and repository root are on sys.path
_current_dir = Path(__file__).resolve().parent       # .../apps/api/app
_api_dir = _current_dir.parent                       # .../apps/api
_root_dir = _api_dir.parent.parent                   # .../Portfolio

for _p in [str(_api_dir), str(_root_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

__version__ = "0.1.0"
