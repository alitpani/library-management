import environ


environ.Env.read_env()  #
env = environ.Env()

DJANGO_DATABASE_URL = env("DATABASE_URL")