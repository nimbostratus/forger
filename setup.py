from setuptools import setup

setup(
    name="forger",
    version="0.1-dev",
    url="http://casts.nimbostratus.de",
    license="BSD",
    author="Sven Broeckling",
    author_email="sven@nimbostratus.de",
    scripts=['forger/forge.py'],
    description="",
    classifiers=[

    ],
    packages=['forger'],
    install_requires=['Jinja2', 'requests'],
    zip_safe=False
)