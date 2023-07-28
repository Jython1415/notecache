rm -r dist/*
source .venv/bin/activate
python -m build
python -m twine upload dist/*
echo "Install with: python -m pip install notecache==[version]"