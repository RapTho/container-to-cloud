# Building a container image

In this section, we’ll walk through how to containerize your previously developed Python app. Wherever you see `podman` instructions, you can also use `docker` instead.

## What is a Containerfile?

A `Containerfile` (also known as a `Dockerfile` in Docker contexts) is a script that contains a list of instructions used to build a container image. It defines:

- The **base image** to start from.
- Files and configurations to add or copy.
- System setup steps (e.g., creating directories, setting permissions).
- The **CMD** to run when the container starts.

Each instruction is executed in sequence, and the result is a lightweight, portable, and reproducible image.

## Build the Python container image

First, prepare your folder structure. It should look like this:

```
├── Containerfile
├── requirements.txt
├── app.py
```

## Containerfile explained

```Dockerfile
# Red Hat's Python minimal base image
FROM registry.access.redhat.com/ubi9/python-312-minimal

# Set the working directory in the container
WORKDIR /app

# Set a non-privileged user
USER 1001

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Set the default port to 8000
ENV PORT=8000

# Expose the port
EXPOSE $PORT

# Run the command to start the development server
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
```

### Key instructions

- `FROM registry.access.redhat.com/ubi9/python-312-minimal`: Uses the Red Hat's Python minimal base image.
- `WORKDIR`: Sets the working directory inside the container.
- `USER 1001`: Ensures the app runs as a non-root user.
- `COPY`: Copies files from the host into the Container
- `RUN pip3 ...`: executes commands during the build such as installing dependencies.
- `ENV`: Sets default environment variables
- `EXPOSE`: Declares which ports are used.
- `CMD`: Specifies the command that runs when the container starts.

## Build the container image

A **manifest** groups multiple platform-specific container images under one tag, allowing cross-architecture support (e.g., `amd64`, `arm64`).
Use the following command to build your manifest:

```bash
podman build --jobs 2 --platform linux/amd64,linux/arm64 --manifest backend:1.0 --layers=false /path/to/Containerfile
```

- `--jobs 2` runs 2 stages in parallel
- `--platform linux/amd64,linux/arm64` ensures the image runs on both standard x86 and ARM-based systems. This is important because **newer MacBooks use Apple Silicon (ARM64)**
- `--manifest` creates the manifest
- `--layers=false` avoids caching intermediate images during the build process

Replace `/path/to/Containerfile` with the actual path the folder containing the Containerfile.

### OPTIONAL: Test locally

To test your image locally, run:

```bash
podman run -d -p 8000:8000 -e UN=myUsername -e PW=myPassword --name backend backend:1.0
```

- `-d` starts the container in the background. Use `podman ps` to display running containers. Add the `-a` option to also display stopped and crashed containers.
- The `-p 8000:8000` flag mapps host port to the container port where `<hostPort>:<containerPort>`.

With this setup, you’ll have a fully functional, portable mosquitto broker container, secured and ready for use in development environments.
