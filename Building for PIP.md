# Quick Guide to using Pip

```bash
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
