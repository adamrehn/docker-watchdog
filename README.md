Docker Idle Watchdog
====================

The docker-watchdog Python package provides a background service that monitors Docker container hosts for periods of inactivity and performs an automatic shutdown of the host after a predefined idle threshold is reached. In a similar manner to the [shutdown-if-idle](https://github.com/PolicyStat/shutdown-if-idle) package, the intended use case is the automatic shutdown of cloud VMs that have been started on demand as part of a Continuous Integration (CI) pipeline, albeit with a focus on Docker container hosts.

The key features of the package include:

- Supports Windows, macOS, and Linux
- Provides easy service installation under all supported operating systems
- Takes cloud provider billing granularity into account to ensure shutdown decisions are cost-effective


## Contents

- [Installation](#installation)
  - [Requirements](#requirements)
  - [Package installation](#package-installation)
  - [Service installation](#service-installation)
  - [Installation scripts for cloud servers](#installation-scripts-for-cloud-servers)
- [Configuration](#configuration)
- [Legal](#legal)


## Installation

### Requirements

The docker-watchdog package requires the following:

- Python 3.5 or newer
- Under macOS and Linux, the [pleaserun](https://github.com/jordansissel/pleaserun) Ruby gem needs to be installed to perform service installation

### Package installation

To install the docker-watchdog Python package itself, simply run:

```
pip3 install docker-watchdog
```

(You may need to prefix this command with `sudo` under macOS and Linux.)

Once the package is installed, you can run the watchdog via either of these commands:

```bash
# Uses the wrapper generated by pip
docker-watchdog

# Invokes the package directly via the Python interpreter
python3 -m docker_watchdog
```

### Service installation

To install the startup service for docker-watchdog, ensure you have any [necessary dependencies](#requirements) installed and run the following command with elevated privileges:

```
docker-watchdog --install
```

The background service will then start automatically the next time the host system boots up.

### Installation scripts for cloud servers

To simplify the setup process for cloud servers, the [scripts](https://github.com/adamrehn/docker-watchdog/tree/master/scripts) directory contains installation scripts for common Docker container host platforms. The scripts automatically install docker-watchdog and its dependencies, and register the docker-watchdog startup service.

Scripts are provided for the following platforms:

- **Windows Server**: [scripts/install_windows_server.ps1](https://github.com/adamrehn/docker-watchdog/blob/master/scripts/install_windows_server.ps1)
  
  Installs the [Chocolatey](https://chocolatey.org/) package manager, uses Chocolatey to install Python and docker-watchdog, and registers the docker-watchdog startup service.
  
  To use this script, run the following command from an elevated PowerShell prompt:
  
  ```powershell
  Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/adamrehn/docker-watchdog/master/scripts/install_windows_server.ps1'))
  ```

- **Debian-based Linux distros**: [scripts/install_debian.sh](https://github.com/adamrehn/docker-watchdog/blob/master/scripts/install_debian.sh)
  
  Installs Python, Ruby, pleaserun, and docker-watchdog, and registers the docker-watchdog startup service.
  
  To use this script, run the following command with root priveleges:
  
  ```bash
  curl -fsSL 'https://raw.githubusercontent.com/adamrehn/docker-watchdog/master/scripts/install_debian.sh' | bash
  ```


## Configuration

The watchdog can be configured either via a JSON configuration file or via environment variables. These two methods can also be used together, in which case values from the configuration file will take precedence over values from environment variables. Any settings for which a value has not been specified will fallback to using a sane default.

The location of the JSON configuration file is based on the operating system and runtime environment:

- Under Windows: `%APPDATA%\docker-watchdog\config.json`
- Under macOS and Linux:
  - If the `$HOME` environment variable is available: `$HOME/.config/docker-watchdog/config.json`
  - If the `$HOME` environment variable is not available: `/etc/docker-watchdog/config.json`

The available configuration settings are as follows:

|JSON Key     |Environment Variable                   |Default |Description                                                                                                                                   |
|-------------|---------------------------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------|
|`sleep`      |`DOCKER_WATCHDOG_SLEEP_INTERVAL`       |60      |Specifies the interval (in seconds) to sleep for between sampling runs.                                                                       |
|`timeout`    |`DOCKER_WATCHDOG_IDLE_TIMEOUT`         |600     |Specifies the period of inactivity (in seconds) required to consider the system idle.                                                         |
|`billing`    |`DOCKER_WATCHDOG_BILLING_GRANULARITY`  |0       |Specifies the billing granularity (in seconds) if the host is a cloud VM, or zero otherwise.                                                  |
|`percentage` |`DOCKER_WATCHDOG_EFFECTIVE_PERCENTAGE` |0.9     |Specifies the minimum percentage (0.0 to 1.0) of the current billing unit that must have elapsed to consider a shutdown to be cost-effective. |


## Legal

Copyright &copy; 2019, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](https://github.com/adamrehn/docker-watchdog/blob/master/LICENSE) for details.

Development of this package was funded by [Deepdrive, Inc](https://deepdrive.io/).
