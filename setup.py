import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modelset-py",
    version="0.1.3",
    author="Jesús Sánchez Cuadrado",
    author_email="jesusc@um.es",
    description="A libray to handle the ModelSet dataset of software models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modelset/modelset-py",
    project_urls={
        "Bug Tracker": "https://github.com/modelset/modelset-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)
