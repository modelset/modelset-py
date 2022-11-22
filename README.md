
# ModelSet Python Library

This is a library to easily integrate ModelSet with Python.
ModelSet is a **labelled dataset of software models**. You can find more information in [its repo](https://github.com/modelset/modelset-dataset). 


## Install from pip 

Simply:

```bash
pip install modelset-py
python -m modelset.downloader
```

## Requirements

- Python 3.6 or higher

## Install from sources

To install from sources, clone this repository and run:

```bash
cd modelset-py
python -m pip install .
python -m modelset.downloader
```

## Usage without installing

This option is useful if you are making changes to the source code of the library while you build an application. 

In this case, you can do the following:

```bash
pip install -r requirements.txt
python src/modelset/downloader.py
```

To import the library, you have to place this in your Python script:

```python
sys.path.append("/path/to/modelset-py/src")
from modelset import load
```

## Running the tests

To be able to execute the tests placed in the `tests` folder, the dataset has to be in you computer (i.e., 
you should have executed either `python -m modelset.downloader` or `python src/modelset/downloader.py`).

```python
python -m unittest discover
```

### Examples

Please, checkout http://github.com/modelset/modelset-apps and the tutorial about how to use ModelSet to infer the category Ecore meta-models: https://github.com/modelset/modelset-apps/tree/master/python

## Contributing

If you want to contribute to this repository, please review our [contribution guidelines](CONTRIBUTING.md) and our [governance model](GOVERNANCE.md).

Note that we have a [code of conduct](CODE_OF_CONDUCT.md) that we expect project participants to adhere to. Please read it before contributing.

## License

This dataset is licensed under the [GNU Lesser General Public License v3.0](LICENSE.md).
