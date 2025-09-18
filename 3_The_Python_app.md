# The Python app

This sample app is an API wrapper around the chucknorris API available at: [https://api.chucknorris.io/](https://api.chucknorris.io/)

The app's supposed to provide a single protected GET endpoint that fetches a joke from the chucknorris API and forwards it to the user.

## OPTIONAL: Create virtual environment

You can create virtual environments to avoid installing Python dependencies globally. Createa a new virtual environment and activate it to install the dependencies in there.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

To activate the environment in windows, use

```cmd
.venv\Scripts\activate.bat
```

## Python app

Create a `requirements.txt` file with the following Python dependencies

```bash
fastapi==0.116.2
requests==2.32.5
uvicorn==0.35.0
```

Install the dependencies

```bash
pip install -r requirements.txt
```

Copy the following code into a file called `app.py`

```python
import os
import sys
import requests
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

# Fetch username and password from environment variables
UN = os.environ.get("UN")
PW = os.environ.get("PW")
PORT = os.environ.get("PORT", 8000)

if not UN or not PW:
    print("Error: Both USERNAME and PASSWORD environment variables must be defined.", flush=True)
    sys.exit(1)

@app.get("/")
def get_joke(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != UN or credentials.password != PW:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"}, )
    response = requests.get("https://api.chucknorris.io/jokes/random")
    if response.status_code != 200:
        raise HTTPException( status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to fetch joke" )
    joke = response.json().get("value", "No joke found")
    return joke

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

Start the Python app locally

on MacOS / Linux

```bash
USERNAME=myUsername PASSWORD=myPassword python app.py
```

on Windows

```powershell
$Env:UN = "myUsername"
$Env:PW = "myPassword"
python app.py
```
