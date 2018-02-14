#!/bin/sh

die(){
    echo >&2 "$@"
    exit 1
}

find /input > /output/wrapup-command-was-here.txt || die "FAILED find /input > /output/wrapup-command-was-here.txt"
