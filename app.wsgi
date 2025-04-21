# app.wsgi
import sys
import logging

sys.path.insert(0, "/var/www/food.roga.tw")

from app import app as application

logging.basicConfig(stream=sys.stderr)
