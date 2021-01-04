from setuptools import setup, find_packages
import pathlib

GITHUB_URL = "https://github.com/fffelix-jan/emailsanta-py"

setup(
    name="emailsanta",
    version="1.0.3",
    packages=find_packages(exclude=["tests*"]),
    license="AGPLv3",
    description="Python module to simulate emailing the legendary Christmas character Santa, powered by Alan Kerr's emailSanta.com.",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=["bs4", "html2text", "requests"],
    url=GITHUB_URL,
    author="Félix An",
    author_email="fffelix.jan.yt@gmail.com",
    python_requires=">= 3.5",
    project_urls={
        "Documentation": GITHUB_URL,
        "Funding": "https://paypal.me/fffelixjan",
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Other/Nonlisted Topic",
    ],
)