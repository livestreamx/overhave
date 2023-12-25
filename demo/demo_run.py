import os
from demo_1 import _run_demo_admin, _get_overhave_settings_generator
from settings import OverhaveDemoAppLanguage

if __name__ == "__main__":
    settings = _get_overhave_settings_generator(OverhaveDemoAppLanguage.RU)
    _run_demo_admin(settings)