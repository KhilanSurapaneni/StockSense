# Import the Celery application instance from the current package's celery module
from .celery import app as celery_app

# Define the public objects of the module. This makes 'celery_app' accessible
# when the module is imported with 'from <module> import *'.
# The __all__ attribute is a convention used to define a public API for the module.
__all__ = ("celery_app",)