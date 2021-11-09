import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modelset-ml2",
    version="0.5.0",
    author="Jesús Sánchez Cuadrado",
    author_email="jesusc@um.es",
    description="A dataset for models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modelset/modelset-libpy",
    project_urls={
        "Bug Tracker": "https://github.com/modelset/modelset-libpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
