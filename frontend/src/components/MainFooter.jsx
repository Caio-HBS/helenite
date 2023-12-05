import React from "react";
import { Link } from "react-router-dom";

import GithubLogo from "/github-logo.png";

export default function MainFooter() {
  const repositoryLink = "https://github.com/Caio-HBS/helenite";
  const linkedInLink = "https://www.linkedin.com/in/caio-bianchi-94aa62206/";

  return (
    <>
      <footer className="bg-helenite-dark-grey text-helenite-light-blue p-2 ">
        <div className="text-center">
          <Link
            to="/about-us"
            className="underline hover:text-helenite-dark-blue text-lg"
          >
            About us
          </Link>
          <p>
            Helenite is a social media built as an exercise of fullstack
            development. Complete with a React.js front-end, a Django/DjangoDRF
            back-end, a Postgres database, and a CI/CD workflow for deployment
            powered by Github Actions and a search engine provided by Algolia,
            all that in a totally dockerized environment.
          </p>
        </div>
        <div className="text-right">
          <p>
            Made by:{" "}
            <a href={linkedInLink} target="_blank" rel="noopener noreferrer">
              <strong className="underline hover:text-helenite-dark-blue">
                Caio Bianchi
              </strong>
            </a>{" "}
            - 2023
          </p>
        </div>
        <div>
          <a
            href={repositoryLink}
            target="_blank"
            rel="noopener noreferrer"
            className="flex justify-end p-1"
          >
            <img src={GithubLogo} alt="Github logo" className="h-6 mr-2" />
            <p>Code Repository</p>
          </a>
        </div>
      </footer>
    </>
  );
}
