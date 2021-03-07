#!/bin/bash
rm -rf build/*
sphinx-apidoc -f -o source/ ../dynamikontrol ../dynamikontrol/Protocol.py ../dynamikontrol/helpers
make html

cd source
sphinx-build -b gettext ./ ../build/gettext
sphinx-intl update -p ../build/gettext -l ko
sphinx-build -b html -D language=ko ./ ../build/html/ko
