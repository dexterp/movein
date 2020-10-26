#!/usr/bin/env bash

test -e /usr/local/homebrew || echo "Installing homebrew..."
test -e /usr/local/homebrew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

echo "Installing python..."
brew install python

echo "Installing pip..."
brew install python
brew link --overwrite python

# Package doesn't reliabiliy link pip
pip="/usr/local/homebrew/bin/pip"
test -e $pip || ln -s ${pip}{3,}

export PATH="/usr/local/homebrew/bin:${PATH}"
hash -r

# Install requirements
pip install -r requirements-setup.in
