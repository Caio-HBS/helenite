import React from "react";
import { Helmet } from "react-helmet";

import LoginForm from "../components/LoginForm.jsx";
import ParticlesComponent from "../components/Particles.jsx";

export default function LoginPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Log in</title>
      </Helmet>
      <div>
        <div className="pt-16">
          <ParticlesComponent />

          <LoginForm />
        </div>
      </div>
    </>
  );
}
