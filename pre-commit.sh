#!/bin/bash

# install
mybasename=`basename $0`
if [ -e .git ] ; then
    if [ ! -e .git/hooks/pre-commit ] ; then
        ln -s ../../${mybasename} .git/hooks/pre-commit && echo "installed pre-commit hook"
        exit
    fi
fi

#
# check that there aren't any
# set_trace() left in the code
#
set_traces=$(git diff --cached | grep -r "set_trace" src/ | grep '^\+')
if [[ ! -z "$set_traces" ]] ; then
    echo  "You have pdb.set_trace() in your code! Commit aborted!"
    git diff --cached --name-only | xargs grep --color --with-filename -n set_trace
    exit 1
fi

flake8_warnings=$(flake8 scripts/ confirm/)
if [[ $? -gt 0 ]] ; then
    flake8 scripts/ confirm/
    exit 1
fi
