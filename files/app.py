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