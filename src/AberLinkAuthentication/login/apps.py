"""Name of the application reuqired for settings

LoginConfig() name of the application
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Django website"
__deprecated__ = False

from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'login'
