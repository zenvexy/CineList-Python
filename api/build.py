import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    scripts = Path(sys.executable).parent
    cache_dir = Path(".prisma-cache").resolve()

    environment = {
        **os.environ,
        "PATH": f"{scripts}{os.pathsep}{os.environ['PATH']}",
        "PRISMA_BINARY_CACHE_DIR": str(cache_dir),
    }

    subprocess.run(
        [sys.executable, "-m", "prisma", "generate", "--schema", "prisma/schema.prisma"],
        check=True,
        env=environment,
    )


if __name__ == "__main__":
    main()
