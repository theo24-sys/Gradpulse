import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

print(f"RECAPTCHA_PUBLIC_KEY: {env('RECAPTCHA_PUBLIC_KEY', default='NOT FOUND')}")
print(f"RECAPTCHA_PRIVATE_KEY: {env('RECAPTCHA_PRIVATE_KEY', default='NOT FOUND')}")
