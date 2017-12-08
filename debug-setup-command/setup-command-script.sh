#!/bin/sh

die(){
    echo >&2 "$@"
    exit 1
}

mkdir /output/setup-command-was-here || die "FAILED mkdir /output/setup-command-was-here"
cp -r /input/* /output/setup-command-was-here || die "FAILED cp -r /input/* /setup-command-was-here"
