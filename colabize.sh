#!/bin/bash

FILES='damage.py weaponsarmor.py cards.py player.py duel.py demo.py'

cat $FILES | sed '/^from .*import .*/d' | sed '/^import .*/d'
