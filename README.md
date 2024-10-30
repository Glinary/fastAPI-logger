# FB Messenger FastAPI Logger

## Set up
1. Type `Ctrl+Shift+P` on vscode
1. Select the python interpreter and use requirements.txt to install dependencies
1. Create a .env file with the variables `VERIFICATION_TOKEN` and `PAGE_ACCESS_TOKEN` for the FB webhook
1. Add environemnt variables `REGION_NAME` and `TABLE_NAME` for AWS dynamoDB

## How to run
1. Run the backend code `python -m app.main`

## Dockerize
1. Build the docker image `docker build -t fastapi-app .`
1. Run the docker container `docker run -d --name my-fastapi-app -p 8000:8000 fastapi-app`

## Technologies
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248.svg?style=for-the-badge&logo=MongoDB&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style=for-the-badge&logo=Pydantic&logoColor=white)
![CloudFlare](https://img.shields.io/badge/Cloudflare-F38020.svg?style=for-the-badge&logo=Cloudflare&logoColor=white)
