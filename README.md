
# ModelSet Python Library

This is a library to easily integrate ModelSet with Python.

## Install from pip

Simply:

```
pip install modelset-py
python -m modelset.downloader
```

## Install from Sources

To install from sources, follow these steps:

```
cd modelset-py
python -m pip install .
python -m modelset.downloader
```

## Usage without installing

This option is useful if you are making changes to the source code of the library while you build an application. 

In this case, you can do the following:

```
pip install -r requirements.txt
python src/modelset/downloader.py
```

To import the library, you have to place this in your Python script:

```
sys.path.append("/path/to/modelset-py/src")
from modelset import load
```

## Running the tests

To be able to execute the tests placed in the `tests` folder, the dataset has to be in you computer (i.e., 
you should have executed either `python -m modelset.downloader` or `python src/modelset/downloader.py`).

```
python -m unittest discover
```

### Examples

Please, checkout http://github.com/modelset/modelset-apps

* Tutorial to use ModelSet to infer the category Ecore meta-models: https://github.com/modelset/modelset-apps/tree/master/python
