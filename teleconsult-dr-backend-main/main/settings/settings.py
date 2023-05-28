from main.settings.base import *
from main.configurations import *

import logging.config
import environ
import os

################################################################################################
# READ VARIABLES FROM ENV
################################################################################################
env = environ.Env()

# ENVIRONMENT DETAILS
env.read_env(os.path.join(BASE_DIR, ".env"))
DOMAIN = os.getenv("DJANGO_CSRF_ALLOWED_HOSTS", "http://127.0.0.1:8000")
print("DOMAIN: ", DOMAIN)

current_env = env.str("ENVIRONMENT", "").strip()
print("ENVIRONMENT: ", current_env)

valid_envs = [
    Environments.PROD.value,
    Environments.LOCAL.value
]

if current_env not in valid_envs:
    print(current_env)
    print("Invalid ENVIRONMENT in config %s" % current_env)
    print("VALID_ENVIRONMENTS ", valid_envs)
    exit(-1)

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "cki2iFfPosWv4P1RdpSvdzCSP3Eb1aNpR5qnNnGa3W9rItsYk1c1HgEVWyEa6bqf",
)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_ALLOWED_HOSTS", default=["http://*.127.0.0.1"]
)

print("ALLOWED_HOSTS: ", ALLOWED_HOSTS)
print("CSRF_TRUSTED_ORIGINS:", CSRF_TRUSTED_ORIGINS)

configurations = get_configurations(env)

API_DOMAIN_URL = configurations[current_env]['api_domain']
DEBUG = configurations[current_env]['is_debug_mode']

######################################################################################################
# SETUP DATABASE
######################################################################################################
"""
 Read the user name and password from the env file for local environments.
 If not exists, check if there is aws secret details, fetch details from there.
"""

DATABASES = {
    "default": configurations[current_env]['database_details']
}
######################################################################################################


print(f"FP Business Dashboard started and connected to - {current_env}")
