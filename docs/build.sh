#!/bin/bash
sphinx-apidoc -f -o source/ ../dynamikontrol
make html
