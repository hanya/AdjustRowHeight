#! /bin/sh

NAME=AdjustRowHeight
VERSION=0.0.1

zip -9 -o $NAME-$VERSION.oxt \
  META-INF/* \
  description.xml \
  descriptions/* \
  registration.components \
  pythonpath/**/*.py pythonpath/**/**/*.py \
  *.xcu *.xcs registration.py \
  *.py \
  LICENSE CHANGES NOTICE README.md
