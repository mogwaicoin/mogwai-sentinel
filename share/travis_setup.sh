#!/bin/bash
set -evx

mkdir ~/.mogwaicore

# safety check
if [ ! -f ~/.mogwaicore/.mogwai.conf ]; then
  cp share/mogwai.conf.example ~/.mogwaicore/mogwai.conf
fi
