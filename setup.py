from setuptools import setup

setup(
    name="forge",
    version="0.1-dev",
    url="http://casts.nimbostratus.de",
    license="BSD",
    author="Sven Broeckling",
    author_email="sven@nimbostratus.de",
    scripts=['forge/forge.py'],
    description="",
    classifiers=[

    ],
    packages=['forge'],
    install_requires=['Jinja2', 'requests']
)