import React, { useEffect } from "react";
import { useSelector } from "react-redux";
import { useNavigate, json, redirect } from "react-router-dom";
import { Helmet } from "react-helmet";

import LoginForm from "../components/LoginForm.jsx";
import ParticlesComponent from "../components/Particles.jsx";

export default function LoginPage() {
  const navigate = useNavigate();

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  useEffect(() => {
    if (isLoggedIn) {
      navigate("/feed");
    }
  }, []);

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
