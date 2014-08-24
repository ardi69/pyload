#!/bin/sh

PYLOAD="../pyload"  # Check ~/pyload/pyload directory
clonedigger -o cpd.xml --cpd-output --fast --ignore-dir="lib" --ignore-dir="remote" $PYLOAD
