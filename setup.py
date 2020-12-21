from setuptools import setup, find_packages

setup(
    name="emailsanta",
    version="1.0.0",
    packages=find_packages(exclude=["tests*"]),
    license="AGPL",
    description="Python module to simulate emailing the legendary Christmas character Santa, powered by Alan Kerr's emailSanta.com.",
    long_description=open("README.md").read(),
    install_requires=["bs4", "html2text", "requests"],
    url="https://github.com/fffelix-jan",
    author="Félix An",
    author_email="fffelix.jan.yt@gmail.com"
)