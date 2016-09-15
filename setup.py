from setuptools import setup

with open("requirements.txt") as f:
    reqs = f.read()

setup(
    name="tessera",
    version="1.0.0",
    description="Open Source Bug Tracking and Ticketing System.",
    author="Mathew Robinson",
    author_email="mathew.robinson3114@gmail.com",
    url="https://github.com/chasinglogic/tessera",
    license="AGPLv3",
    install_requires=[reqs.split("\n")],
    packages=["tessera"]
)
