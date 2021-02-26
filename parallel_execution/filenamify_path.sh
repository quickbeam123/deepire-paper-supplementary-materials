#!/bin/bash
echo $1 | sed 's/\//_/g' | sed 's/^\.//g'
