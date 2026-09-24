# This file is needed only for bot-hosting.net !!!

import runpy
import sys

if "." not in sys.path:
    sys.path.insert(0, ".")

runpy.run_module("heroku", run_name="__main__")

""" THIS is only test : CustomTelegramClient ok ok"""