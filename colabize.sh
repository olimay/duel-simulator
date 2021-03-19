#!/bin/bash

cat *.py | sed '/^from .*import .*/d' | sed '/^import .*/d'
