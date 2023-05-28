from enum import Enum
from environ.environ import Env


class Environments(Enum):
    LOCAL = "local"
    PROD = "prd"


def get_configurations(env: Env) -> dict:
    return {
        Environments.LOCAL.value: {
            'database_details': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'doctor_app',
                'USER': 'doctor_app_user',
                'PASSWORD': 'DoctorAppBackendDatabase1@',
                'HOST': 'localhost',
                'PORT': '5432',
            },
            'api_domain': 'https://dd46-103-13-42-134.ngrok-free.app/',
            'is_debug_mode': True
        },
        Environments.PROD.value: {
            'database_details': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'doctor_app',
                'USER': 'doctor_app_user',
                'PASSWORD': 'DoctorAppBackendDatabase1@',
                'HOST': 'localhost',
                'PORT': '5432',
            },
            'api_domain': 'http://65.1.74.196/',
            'is_debug_mode': env.bool("DEBUG", False)
        },
    }
