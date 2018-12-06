import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="intralinks",
    version="0.1.0",
    author="Olivier Mangez",
    author_email="olivier.mangez@gmail.com",
    description="A SDK for intralinks.com (for educational purpose only)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilapi/intralinks-api-python",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'bs4', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)