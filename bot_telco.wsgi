activate_this = '/home/ubuntu/bot_telco/venv/bin/activate_this.py'
with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/bot_telco/")

from bot_telco.app import app as application
