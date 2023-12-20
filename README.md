# Welcome to Helenite

![Helenite logo](assets/helenite_full_logo.png)
A network for people, by people.

## Demo

![Helenite demo](assets/helenite_demo.gif)

---

## About

Helenite is a social media built as an exercise of fullstack development. Complete with a React.js front-end, a Django/DjangoDRF back-end, a Postgres database, and a CI/CD workflow for deployment, all that in a totally dockerized environment.

## Goals

With this project, my goals were to improve my abilities as a programmer, especifically with CI/CD workflows, but also learn the basic for Javascript UI development in React.

## Features

- Coming soon.

## Usage

The build process consists of two parts, setting up two `.env` files, and actually deploying:

### Setting up the `.env` files

You'll need two files named ".env" to be able to deploy the project locally. The first one will be put in the front-end project folder:

#### Front-end.
```sh
cd frontend
echo -e "VITE_REACT_BACKEND_URL=http://localhost:8000" >> .env
```

Please note that if you for whatever reason want to change the local port out of which Django is operating, you will also need to change the port on the .env.

#### Backend

```sh
cd ../backend

echo "DJANGO_SECRET_KEY=placeholder" >> .env
echo "DJANGO_DEBUG_STATUS=True" >> .env
echo "ALGOLIA_APPLICATION_ID=placeholder" >> .env
echo "ALGOLIA_API_KEY=placeholder" >> .env
echo "POSTGRES_DB=django" >> .env
echo "POSTGRES_USER=postgres" >> .env
echo "POSTGRES_PASSWORD=postgres" >> .env
echo "POSTGRES_HOST=localhost" >> .env
echo "POSTGRES_PORT=5432" >> .env

# OR use the one-liner:

echo "DJANGO_SECRET_KEY=placeholder\nDJANGO_DEBUG_STATUS=True\n\nALGOLIA_APPLICATION_ID=placeholder\nALGOLIA_API_KEY=placeholder\nPOSTGRES_DB=placeholder\nPOSTGRES_USER=django\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_HOST=localhost\nPOSTGRES_PORT=5432" >> .env
```

Please note that you will need to provide all of the `placeholders` (including the Algolia project ones) in that command with valid tokens, otherwise the application will not work.

[You can use this to generate a Django secret key](https://djecrety.ir/)

### Deploying

To finally deploy the application locally, **you will need [Docker](https://www.docker.com/) installed on your machine**, then just follow these steps:

```sh
cd Helenite # Or whatever you name the cloned repository has.
docker-compose build
docker-compose up
```

If the build process was successfull, you can just navigate to "http://localhost:5173/" to see the front-end application in action, and "http://localhost:8000/admin" to handle view and edit the database as well as access the backend.

## License

This project is licensed under the MIT License.
