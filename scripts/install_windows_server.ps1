# Install Chocolatey
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Make `refreshenv` available immediately (code from here: <https://stackoverflow.com/a/46760714>)
$env:ChocolateyInstall = Convert-Path "$((Get-Command choco).path)\..\.."
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"

# Install Python and pip
choco install -y python

# Refresh the PATH environment variable so we can run `pip`
refreshenv

# Install docker-watchdog
pip install "setuptools>=38.6.0"
pip install docker-watchdog

# Install the docker-watchdog startup service
docker-watchdog --install
