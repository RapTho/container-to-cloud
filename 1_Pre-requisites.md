# Prerequisites

Before starting the course, please ensure you have the following tools installed on your machine. This guide provides installation instructions for **both macOS and Windows** platforms.

## 1. Podman or Docker

You only need **one** of these container runtimes. Container runtimes allow you to build, run and publish container images locally.

### Podman

Podman is a daemonless and rootless alternative to Docker, which enhances the security. Podman is fully compatible with the _docker_ CLI commands and OCI standards.

#### macOS

```
brew install podman
podman machine init
podman machine start
```

#### Windows

Download and install from the official site: [https://podman.io/getting-started/installation](https://podman.io/getting-started/installation)

### Docker

#### macOS & Windows

Download Docker Desktop from: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

> **Note:** Docker Desktop requires a free Docker account.

## 2. IBM Cloud CLI

Download and install from: [https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases/](https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases/)

After installation, verify with:

```
ibmcloud version
```

Optionally, you can also enable the autocompletion:<br />
[https://cloud.ibm.com/docs/cli?topic=cli-shell-autocomplete](https://cloud.ibm.com/docs/cli?topic=cli-shell-autocomplete)

## 3. Bruno (API test client)

Bruno is a lightweight API client, ideal for working with REST APIs. In later chapters you'll interact with the IBM Cloudant Database APIs. Bruno will come in handy to test the APIs before implementing them in your code.

Download the latest release for your OS :  
[https://www.usebruno.com/downloads](https://www.usebruno.com/downloads)

Install the version appropriate for your system.

## 4. Python (version 3.8 or higher)

### macOS

```
brew install python
```

### Windows

Download and install from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

> **Note:** During installation, make sure to select **"Add Python to PATH"**.

## 5. Code editor (VS Code or any other)

Recommended is using [Visual Studio Code](https://code.visualstudio.com/) for this course but any other editor will also do the job.

### macOS & Windows

Download from: [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)

> You can use any other editor you're comfortable with.

## Verification checklist

After installation, you should be able to run the following commands in your terminal or command prompt:

```bash
podman --version       # or docker --version
ibmcloud version
python --version
```

## Environment variables

Throught the workshop, we'll be using environment variables to configure our applications and execute commands. How to set those environment variables will depend on your operating system and Command Line Interface.
Below you find instructions for macOS/Linux and Windows. The rest of the lab is primarely documented for macOS/Linux. Come back here to see how you'd adapt the instructions for Windows.

### macOS & Linux

```bash
# Setting variables
export VARIABLE_NAME=value
export ANOTHER_VAR="value with spaces"

# Using variables
echo $VARIABLE_NAME
command --param=${VARIABLE_NAME}

# Setting multiple variables inline for a single command
VARIABLE1=value1 VARIABLE2=value2 command
```

### Windows (Powershell)

```powershell
# Setting variables
$env:VARIABLE_NAME = "value"
$env:ANOTHER_VAR = "value with spaces"

# Using variables
echo $env:VARIABLE_NAME
command --param=$env:VARIABLE_NAME

# Setting multiple variables for a command (must be set before running command)
$env:VARIABLE1 = "value1"
$env:VARIABLE2 = "value2"
command
```

### WIndows (Command Prompt)

```bat
:: Setting variables
set VARIABLE_NAME=value
set ANOTHER_VAR=value with spaces

:: Using variables
echo %VARIABLE_NAME%
command --param=%VARIABLE_NAME%

:: Setting multiple variables for a command (must be set before running command)
set VARIABLE1=value1
set VARIABLE2=value2
command
```

Once everything is installed and working, you're ready to begin!
