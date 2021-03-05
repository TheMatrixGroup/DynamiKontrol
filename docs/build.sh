#!/bin/bash
rm -rf build/*
sphinx-apidoc -f -o source/ ../dynamikontrol ../dynamikontrol/Protocol.py ../dynamikontrol/helpers
make html
