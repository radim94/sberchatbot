#!/bin/bash

CUR_DIR=`dirname $0`

if [[ $CUR_DIR != *"devops/scripts" ]]; then
    echo "You should run script from root project dir!"
    echo "example:       sh ./devops/scripts/start.sh      "
    exit 1;
fi

if [[ $# > 0 ]]; then

    while [ -n "$1" ]
    do
    case "$1" in

    start)
    python3 -m pip install virtualenv --user &&
    python3 -m virtualenv venv
    source ./venv/bin/activate
    ;;

    run)
    echo "run"
    ;;

    build)
    echo "build"
    ;;

    *) echo "Incorrect arg!";;
    esac
    shift
    done

else

echo "USAGE:"
echo "start  --- prepare workspace"
echo "run  --- run server"
echo "build  --- run server"
fi


