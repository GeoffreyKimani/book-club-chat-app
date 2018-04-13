from setuptools import setup
from chat_app.constants import APP_NAME

setup(
    name=APP_NAME,
    version='1.0.0',
    description='A book club chatting application',
    packages=['chat_app'],
    entry_points={
        'console_scripts': ['chat_app = chat_app.__main__:main']
    },
)
