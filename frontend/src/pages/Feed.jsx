import React from "react";
import { Helmet } from "react-helmet";

import FeedComponent from "../components/Feed.jsx";
import ParticlesComponent from "../components/Particles.jsx";

export default function FeedPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Feed</title>
      </Helmet>
      <div>
        <div className="pt-16">

          <FeedComponent />
        </div>
      </div>
    </>
  );
}
