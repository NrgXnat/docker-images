import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xnatjsession", 
    version="0.1",
    author="Brian Holt",
    author_email="beholt@radiologics.com",
    description="Utility functions for using XNAT JSESSION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/radiologics/docker-images",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2"
    ],
    python_requires='>=2.6',
    install_requires=[
        "requests>=2.18.4"
    ]
)
