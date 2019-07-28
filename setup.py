import setuptools

setuptools.setup(
    name="whatcha-readin",
    url="https://github.com/allisonking/whatcha-readin",
    author="Allison King",
    author_email="allisonjuliaking@gmail.com",
    classifers=["Programming Language :: Python :: 3.7"],
    license="MIT ",
    python_requires=">=3.5",
    version="0.0.1",
    description="githook for adding currently reading books to git commit messages",
    packages=setuptools.find_packages(),
    install_requires=[
        "certifi",
        "chardet",
        "Click",
        "idna",
        "python-dotenv",
        "requests",
        "urllib3",
        "xmltodict",
    ],
)
