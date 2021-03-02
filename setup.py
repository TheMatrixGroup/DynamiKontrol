import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DynamiKontrol",
    version="0.0.1",
    author="Taehee Lee",
    author_email="kairess87@gmail.com",
    description="DynamiKontrol Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://m47rix.com",
    license='MIT',
    install_requires=['pyserial>=3.5'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows, MacOS and Linux",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
