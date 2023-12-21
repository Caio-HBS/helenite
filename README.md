# Welcome to Helenite

![Helenite logo](assets/helenite_full_logo.png)
A network for people, by people.

## Demo

![Helenite demo](assets/helenite_demo.gif)

---

## About

Helenite is a social media built as an exercise of fullstack development. Complete with a React.js front-end, a Django/DjangoDRF back-end, a Postgres database, and a CI/CD workflow for deployment, all that in a totally dockerized environment.

## Goals

With this project, my goals were to improve my abilities as a developer, especifically with CI/CD workflows, but also learn the basic for Javascript UI development in React.

## Features

- A Backend written in Python 3+ using Django and Django DRF to provide ease of use and a robust security;
- A Frontend written in modern Java Script utilizing React for a better, easier user experience;
  - Complete with Tailwind CSS and Vite, allowing for a blazing fast development experience;
- Modern Docker support to provide a clean, predictable environment for use both in development, as well as production;
- A meticulously written [wiki](https://github.com/Caio-HBS/helenite/wiki) to allow developers to only use the backend in their projects if they want to;
- Completely free-to-use code.

## Usage

The build process consists of two parts, setting up two `.env` files, and actually deploying:

### Setting up the `.env` files

You'll need two files named ".env" to be able to deploy the project locally. The first one will be put in the front-end project folder:

#### Front-end
```sh
cd frontend
echo -e "VITE_REACT_BACKEND_URL=http://localhost:8000" >> .env
```

Please note that if you for whatever reason want to change the local port out of which Django is operating, you will also need to change the port on the .env.

---

And for the second file, which should be put in the back-end project folder:

#### Back-end

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

Please note that you will need to provide all of the `placeholders` (including the [Algolia](https://www.algolia.com/) ones) in this file with valid tokens, otherwise the application will not start.

- [You can use this to generate a Django secret key](https://djecrety.ir/)

---

### Deploying

To finally deploy the application locally, **you'll first need [Docker](https://www.docker.com/) installed on your machine**, then just follow these steps:

```sh
cd Helenite # Or whatever you named the cloned repository.
docker-compose build --no-cache
docker-compose up
```

If the build process was successfull, you can simply navigate to "http://localhost:5173/" to see the front-end application in action, and "http://localhost:8000/admin" to handle/view and edit the database, as well as access the backend.

## Still todos

- Implement unit tests for frontend;
- Clean frontend code;
- Implement k8s support;
- Improve CI to allow direct development with AWS.

## License

This project is licensed under the MIT License.
