#!/bin/python
rm -r doc
sphinx-apidoc -F -o ./doc ./roomai

cd doc
cat conf.py > tmp
echo "import os" > conf.py
echo "import sys" >> conf.py
echo "sys.path.insert(0, os.path.abspath('..'))" >> conf.py
cat tmp >> conf.py
rm tmp 
make html

cd ..
