import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xnatbidsfns", 
    version="1.0",
    author="Radiologics/NRG",
    author_email="kate@radiologics.com",
    description="Utility functions for BIDS data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/radiologics/docker-images",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2"
    ],
    python_requires='>=2.6',
)
