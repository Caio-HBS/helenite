import React from "react";
import { Helmet } from "react-helmet";

import obiWan from "/obiwan.jpg";

import MainFooter from "../components/MainFooter.jsx";
import MainNavigationBar from "../components/MainNavigationBar.jsx";

export default function ErrorPage() {
  return (
    <>
      <MainNavigationBar />
      <Helmet>
        <title>Helenite | Error</title>
      </Helmet>
      <main>
        <div
          className="bg-cover bg-center h-screen "
          style={{ backgroundImage: `url(${obiWan})` }}
        >
          <div
            id="main-element"
            className="flex flex-col h-screen items-start py-24 px-8 text-helenite-white"
          >
            <h1 className="text-7xl"><strong>404 Error:</strong> page not found :(</h1>
          </div>
        </div>
        <MainFooter />
      </main>
    </>
  );
}
