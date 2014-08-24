#!/bin/sh

PROJECT="../pyload"  # Check ~/pyload/pyload directory

echo "Running sloccount ..."
REPORT="sloccount.sc"
sloccount --duplicates --wide --details $PROJECT > $REPORT && echo "Done. Report saved to $REPORT"

echo "Running pep8 ..."
REPORT="pep8.txt"
pep8 $PROJECT > $REPORT && echo "Done. Report saved to $REPORT"

echo "Running pylint ..."
REPORT="pylint.txt"
pylint --reports=no $PROJECT > $REPORT && echo "Done. Report saved to $REPORT"

#echo "Running pyflakes ..."
#REPORT="pyflakes.txt"
#{
   # pyflakes to pylint syntak
#  find $PROJECT -type f -name "*.py" | egrep -v '^\./lib' | xargs pyflakes  > pyflakes.log || :
   # Filter warnings and strip ./ from path
#  cat pyflakes.log | awk -F\: '{printf "%s:%s: [E]%s\n", $1, $2, $3}' | grep -i -E -v "'_'|pypath|webinterface" > $REPORT
#  sed -i 's/^.\///g' $REPORT
#} && echo "Done. Report saved to $REPORT"
