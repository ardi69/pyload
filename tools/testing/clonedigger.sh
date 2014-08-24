#!/bin/sh

PROJECT="../pyload"  # Check ~/pyload/pyload directory
clonedigger -o cpd.xml --cpd-output --fast --ignore-dir="lib" --ignore-dir="remote" $PROJECT
