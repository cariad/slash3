from pathlib import Path

from setuptools import setup

from slash3 import __version__

readme_path = Path(__file__).parent / "README.md"

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Typing :: Typed",
]

if "a" in __version__:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in __version__:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.earth",
    classifiers=classifiers,
    description="Builds and navigates Amazon Web Services S3 URIs",
    include_package_data=True,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="slash3",
    packages=[
        "slash3",
    ],
    package_data={
        "slash3": ["py.typed"],
    },
    project_urls={
        "Documentation": "https://cariad.github.io/slash3/slash3.html",
        "Source": "https://github.com/cariad/slash3",
    },
    python_requires=">=3.9",
    version=__version__,
)
