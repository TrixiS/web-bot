import os
import platform

from pathlib import Path

WINDOWS = platform.system() == "Windows"


def deps():
    scripts_path = Path(__file__).parent
    root_path = scripts_path.parent

    os.chdir(str(root_path))
    install_script = scripts_path / ("install.bat" if WINDOWS else "install.sh")
    deps_install_exit_code = os.system(install_script.read_text(encoding="utf-8"))

    if deps_install_exit_code != 0:
        raise Exception("Intallation exit code != 0")
