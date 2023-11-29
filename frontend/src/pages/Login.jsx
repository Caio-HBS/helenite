import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { Helmet } from "react-helmet";

import LoginForm from "../components/LoginForm.jsx";

export default function LoginPage() {
  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);
  const navigate = useNavigate();

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
      <LoginForm />
    </>
  );
}
