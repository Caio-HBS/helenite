import React, { useCallback } from "react";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";

import particlesOptions from "../utils/particlesOptions.js";

export default function ParticlesComponent() {
  const particlesInit = useCallback(async (engine) => {
    await loadFull(engine);
  }, []);

  const particlesLoaded = useCallback(async (container) => {
    // await console.log(container);
  }, []);

  return (
    <Particles
      id="particles-component"
      className="bg-cover bg-center h-screen absolute"
      init={particlesInit}
      loaded={particlesLoaded}
      options={particlesOptions}
    />
  );
}
