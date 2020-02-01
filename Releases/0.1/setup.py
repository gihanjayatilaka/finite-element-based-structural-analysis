import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdn-struct-biteCode",
    version="0.1",
    author="Team biteCode",
    author_email="bitecode@eng.pdn.ac.lk",
    description="A structural analysis software package",
    long_description="A structural analysis software developed by Department of Computer Engineering, University of Peradeniya in colloboration with the Department of Civil Enginneing, University of Peradeniya",
    long_description_content_type="text/markdown",
    url="https://github.com/TeambiteCode/finite-element-based-structural-analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)