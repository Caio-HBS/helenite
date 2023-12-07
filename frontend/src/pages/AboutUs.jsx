import React from "react";
import { Helmet } from "react-helmet";

import ParticlesComponent from "../components/Particles.jsx";

export default function AboutUsPage() {
  const h2Class = "text-2xl py-3 text-helenite-light-blue";
  const pClass = "text-lg py-2";
  const aClass = "underline hover:text-helenite-green";

  const links = [
    "https://en.wikipedia.org/wiki/Helenite",
    "https://react.dev/",
    "https://www.django-rest-framework.org/",
    "https://www.postgresql.org/",
    "https://www.docker.com/",
  ];

  return (
    <>
      <Helmet>
        <title>Helenite | About us</title>
      </Helmet>
      <div className="pt-16">
        <ParticlesComponent />
        <div
          id="main-element"
          className="flex flex-col h-screen items-center justify-center"
        >
          <div
            id="items-container"
            className="w-1/2 bg-helenite-light-grey p-3 text-helenite-white text-justify rounded-lg relative"
          >
            <div id="first-paragraph">
              <h2 className={h2Class}>
                <strong>About us</strong>
              </h2>
              <p className={pClass}>
                Welcome to Helenite, a social network for people by people. Our
                mission is to connect people, spark creativity, and prioritize
                privacy and security. Join us in building a vibrant online
                community.
              </p>
            </div>
            <div id="second-paragraph">
              <h2 className={h2Class}>
                <strong>Name</strong>
              </h2>
              <p className={pClass}>
                Our name, Helenite, draws inspiration from the gemstone{" "}
                <a
                  href={links[0]}
                  className={aClass}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  helenite
                </a>
                . This name was chosen not only for the sheer beauty of the gem
                itself, but also for its unique creation, much like our
                platform. Helenite is a man-made gem created from the volcanic
                eruption of Mount St. Helens. Similarly, our website has been
                meticulously crafted by human ingenuity, bringing together
                React, Django-DRF, PostgreSQL, and Docker to create a platform
                where connections and creativity flourish.
              </p>
            </div>
            <div id="third-paragraph">
              <h2 className={h2Class}>
                <strong>Developer's note</strong>
              </h2>
              <p className={pClass}>
                As said above, this project is powered by{" "}
                <a
                  href={links[1]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={aClass}
                >
                  React.js
                </a>
                ,{" "}
                <a
                  href={links[2]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={aClass}
                >
                  Django-DRF,
                </a>{" "}
                <a
                  href={links[3]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={aClass}
                >
                  PostgreSQL
                </a>{" "}
                and{" "}
                <a
                  href={links[4]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={aClass}
                >
                  Docker
                </a>{" "}
                and aims to give me a better understanding of JavaScript's
                frameworks as well improve my overall skills as a developer.
              </p>
            </div>
            <div id="fourth-paragraph">
              <h2 className={h2Class}>
                <strong>Contact us</strong>
              </h2>
              <p className={pClass}>
                Have questions, suggestions, or feedback? I'd love to hear from
                you! Feel free to reach out to me at caiohbs23@gmail.com.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
