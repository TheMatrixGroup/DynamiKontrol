import setuptools
import sys

if sys.version_info[0] > 2:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="DynamiKontrol",
    version="0.3.3",
    author="Taehee Lee",
    author_email="kairess87@gmail.com",
    description="DynamiKontrol Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/TheMatrixGroup/DynamiKontrol',
    license='MIT',
    install_requires=['pyserial>=3.5'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.4.2",
)
