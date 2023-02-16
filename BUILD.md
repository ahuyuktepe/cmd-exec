### 1 Building Artifact
#### 1.1 Run Tests
python run-tests.py

#### 1.2 Building Package
- Use following command to compile package
```
python -m pip install --upgrade build
```
- Use following commmand to generate package file.

```
python -m build
```

### 2 Publishing on PyPi
Before publishing on production PyPi account, we should publish it on TestPyPi account.

#### 2.1 Publishing on TestPyPi
```py -m twine upload --repository testpypi dist/*```

#### 2.2 Publishing on PyPi
```py -m twine upload dist/*```

### 3 Installing Package Manually

Use following command to install given package locally vi pip.
```
python -m pip install /path/to/package.tar.gz
```