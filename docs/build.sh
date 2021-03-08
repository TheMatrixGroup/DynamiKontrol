#!/bin/bash
rm -rf build/*
sphinx-apidoc -f -o source/ ../dynamikontrol ../dynamikontrol/Protocol.py ../dynamikontrol/BaseLED.py ../dynamikontrol/helpers
make html

cd source
sphinx-build -b gettext ./ ../build/gettext
sphinx-intl update -p ../build/gettext -l ko_KR
sphinx-build -b html -D language=ko_KR ./ ../build/html/ko_KR
