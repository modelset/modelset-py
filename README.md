
# ModelSet Python Library

This is a library to easily integrate ModelSet with Python.

## Install

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
python src/modelset/downloader.py
```

```
sys.path.append("/path/to/modelset-py/src")
import modelset.dataset as ds
```

### Examples

Please, checkout http://github.com/modelset/modelset-apps

* Tutorial to use ModelSet to infer the category Ecore meta-models: https://github.com/modelset/modelset-apps/tree/master/python
