#!/bin/sh

die(){
    echo >&2 "$@"
    exit 1
}

#/tree.sh
mkdir -p /output/wrapup-command-was-here/
cp -r /input/* /output/wrapup-command-was-here/
find /input > /output/wrapup-command-was-here.txt || die "FAILED find /input > /output/wrapup-command-was-here.txt"
