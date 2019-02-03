#!/usr/bin/env bash
set -e
set -x

# Install Python and Ruby
apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ruby

# Install pleaserun
gem install pleaserun

# Install docker-watchdog
pip3 install 'setuptools>=38.6.0'
pip3 install docker-watchdog

# Install and enable the docker-watchdog startup service
docker-watchdog --install
systemctl enable docker-watchdog
