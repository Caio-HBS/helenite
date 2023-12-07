import React from "react";
import { Helmet } from "react-helmet";

import ParticlesComponent from "../components/Particles.jsx";
import RegisterForm from "../components/RegisterForm.jsx";

export default function RegisterPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Register</title>
      </Helmet>
      <div>
        <div className="pt-16">
          <ParticlesComponent />

          <RegisterForm />
        </div>
      </div>
    </>
  );
}
