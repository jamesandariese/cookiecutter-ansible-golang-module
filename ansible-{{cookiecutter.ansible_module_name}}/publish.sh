#!/bin/bash

cd "$(dirname "$0")"
set -e
set -x

BUILT_FILES=x"$(find .build -type f | wc -l | grep -o '[0-9]*')"
if [ "$BUILT_FILES" = x0 ];then
	./rebuild.sh
        BUILT_FILES=x"$(find .build -type f | wc -l | grep -o '[0-9]*')"
fi

if [ "$BUILT_FILES" = x1 ];then
	ansible-galaxy collection publish .build/*.tar.gz
else
	1>&2 echo "too many files in .build folder."
fi
