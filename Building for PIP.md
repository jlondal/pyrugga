# Quick Guide to using Pip

```bash

# create a VM with python3
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
pyenv activate de_py3


# then run setup tools
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine


rm -f dist/*.*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*   
```
