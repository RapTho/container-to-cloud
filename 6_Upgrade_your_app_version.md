# Upgrade your app's version

This guide walks you through the process of upgrading your application to a new version, rebuilding the container image, publishing it to IBM Container Registry, and updating the deployment on IBM Code Engine.

## Change parts of your code

When upgrading your application, you'll typically need to modify your code to add new features, fix bugs, or update dependencies. Here are some common changes you might make:

### Update the application code (app.py)

For this example, let's add a new endpoint to our FastAPI application that returns the application version and a health status:

```python
# Add this near the top of app.py, after the existing imports
from fastapi.responses import JSONResponse

# Add this after the existing environment variable definitions
VERSION = os.environ.get("VERSION", 2)

# Add this new endpoint
@app.get("/health")
def health_check():
    return JSONResponse({
        "status": "healthy",
        "version": VERSION
    })
```

## Rebuild the container image

After making changes to your code, you need to rebuild your container image with a new version tag:

1. Set environment variables (update the IMAGE_TAG to reflect the new version):

```bash
export RESOURCE_GROUP=iot-digital-engineering
export CR_NAMESPACE=hslu-iot-digital-engineering
export IMAGE_NAME=backend-${USER}
export IMAGE_TAG=2.0  # Updated from 1.0 to 2.0
```

For Windows PowerShell users:

```powershell
$env:RESOURCE_GROUP = "iot-digital-engineering"
$env:CR_NAMESPACE = "hslu-iot-digital-engineering"
$env:IMAGE_NAME = "backend-${USER}"
$env:IMAGE_TAG = "2.0"  # Updated from 1.0 to 2.0
```

2. Build the new container image:

```bash
# Build the images with the new tag
podman build --jobs 2 --platform linux/amd64,linux/arm64 --manifest backend:2.0 --layers=false /path/to/Containerfile
```

3. Verify the new image was created:

```bash
podman images
```

You should see your new image with the tag "2.0".

## Publish your new container images

Now you need to push your updated container image to IBM Container Registry.

1. Ensure you're logged in to IBM Cloud and Container Registry:

If you need to redo this step, check the docs at [Deploy_on_IBM-Cloud](./5_Deploy_on_IBM-Cloud.md)

2. Tag and push your new image:

```bash
# Tag the image with the IBM Container Registry URL
podman tag backend:${IMAGE_TAG} de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}

# Push the image to IBM Container Registry
podman manifest push de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
```

## Update the app's version on IBM Code Engine

Finally, you need to update your application on IBM Code Engine to use the new container image.

1. Select your Code Engine project:

```bash
ibmcloud ce project select --name myProjectName
```

2. Update the application with the new image:

```bash
ibmcloud ce app update --name backend-${USER} \
  --image de.icr.io/${CR_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
```

For Windows PowerShell users:

```powershell
ibmcloud ce app update --name backend-$env:USERNAME `
  --image de.icr.io/$env:CR_NAMESPACE/$env:IMAGE_NAME:$env:IMAGE_TAG
```

3. Verify the application is running with the new version:

```bash
# Get the application URL
ibmcloud ce app get --name backend-${USER} --output url
```

Test your new endpoint adding the endpoint `/health` to your app url. You should see a response like:

```json
{ "status": "healthy", "version": "2.0" }
```

Congratulations! You've successfully upgraded your application to a new version and deployed it to IBM Code Engine.
