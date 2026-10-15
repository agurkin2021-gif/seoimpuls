from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        admin_root = exe_dir.parent if exe_dir.name.lower() == "exe" else exe_dir
    else:
        admin_root = Path(__file__).resolve().parent

    os.environ.setdefault("SEOIMPULS_ADMIN_PASSWORD", "h74o63")
    os.environ.setdefault("SEOIMPULS_ADMIN_PORT", "8787")
    os.environ.setdefault("SEOIMPULS_ADMIN_PORT_FALLBACK", "1")
    sys.path.insert(0, str(admin_root))

    import server

    server.run()


if __name__ == "__main__":
    main()
