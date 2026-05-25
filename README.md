# as-checker

## requirements
- Python 3
- ```pip install rich```

## build
```cmd
nuitka --standalone --onefile --windows-console-mode=force --lto=yes --jobs=4 --remove-output --assume-yes-for-downloads --output-dir=dist main.py
```
