# Deploying the app on IBM Cloud

In this guide, you'll learn how to:

- Push the previously built container image to **IBM Container Registry (ICR)**.
- Deploy the container to **IBM Code Engine**, a fully managed, serverless platform for running containers.

This workflow is ideal for hosting custom services like a secured API backend, built and maintained locally but deployed in the cloud.

## Prerequisites

- Python container image built (previous step)
- IBM Cloud CLI installed
- Logged in with `ibmcloud login --sso`

## Install required plugins

Install the Code Engine and Container Registry plugins:

```bash
ibmcloud plugin install code-engine container-registry
```

## Set environment variables

These variables make the rest of the commands easier to reuse. Choose a **unique** `IMAGE_NAME`

```bash
export RESOURCE_GROUP=rotkreuz-dibm
export CR_NAMESPACE=dibm
export IMAGE_NAME=backend-${USER}
export IMAGE_TAG=1.0
export PROJECT_NAME=dibm
```

> Note: These variables are only available in the current session.

#### Setting environment variables on Windows

Check the Windows command sections in the [pre-requisites](./1_Pre-requisites.md#environment-variables) chapter for instructions on how to execute this on Windows. The `USER` environment variable is automatically set to your username on macOS and Linux. Wherever you see `$USER`, use `USERNAME` on Windows. Below an example for Windows Powershell:

```powershell
$env:IMAGE_NAME = "backend-$env:USERNAME"
```

## Select IBM Cloud context

Select the correct resource group:

```bash
ibmcloud target -g ${RESOURCE_GROUP}
```

Select your Code Engine project:

```bash
ibmcloud ce project select --name ${PROJECT_NAME}
```

## Publish image to IBM Container Registry

Set region and log in:

```bash
ibmcloud cr region-set eu-central
ibmcloud cr login --client podman # or --client docker
```

Add namespace (skip if it already exists):

```bash
ibmcloud cr namespace-add ${CR_NAMESPACE}
```

A **manifest** groups multiple platform-specific container images under one tag, allowing cross-architecture support (e.g., `amd64`, `arm64`). We re-tag the image with the IBM Container Registry URL so it can be correctly identified and pushed to the registry.

```bash
podman tag backend:1.0 de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
podman manifest push de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
```

(Optional) Set image retention policy to keep only the last 2 versions:

```bash
ibmcloud cr retention-policy-set --images 3 ${CR_NAMESPACE}
```

## Create API key and registry access for Code Engine

Create an IBM Cloud API key:

> **Save the generated API key**, as it's only visible during creation time!

```bash
ibmcloud iam api-key-create backend-deploy-key-${USER} -d "API Key to deploy a Python backend on IBM Code Engine"
```

Copy and export the API key:

```bash
export API_KEY="myGeneratedAPIKey"
```

Create a registry access secret for Code Engine:

```bash
ibmcloud ce registry create --name ibm-container-registry-${USER} --server de.icr.io --username iamapikey --password ${API_KEY}
```

## Create the API credential secret

```bash
ibmcloud ce secret create --name api-credentials-${USER} --from-literal UN=myUsername --from-literal PW=myPassword
```

## Deploy the Python app to IBM Code Engine

Run the following to create and deploy the application:

```bash
ibmcloud ce app create --name backend-${USER} \
  --image de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG} \
  --registry-secret ibm-container-registry-${USER} \
  --env-from-secret api-credentials-${USER} \
  --port 8000 \
  --min-scale 1 \
  --max-scale 1 \
  --cpu 0.25 \
  --memory 0.5G
```

This will start your Python backend on IBM Code Engine.
