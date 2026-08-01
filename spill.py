"""Desktop entry point.

The game itself lives in main.py (async, so the same code can run in the
browser via pygbag). Running `python spill.py` still works exactly as before.
"""

import asyncio

from main import main

if __name__ == "__main__":
    asyncio.run(main())
