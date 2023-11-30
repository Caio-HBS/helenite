import React, { useEffect } from "react";
import { useSelector } from "react-redux";
import { useNavigate, json, redirect } from "react-router-dom";
import { Helmet } from "react-helmet";

import LoginForm from "../components/LoginForm.jsx";

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
      <LoginForm />
    </>
  );
}

export async function action({ request }) {
  const data = await request.formData();
  const authData = {
    username: data.get("username"),
    password: data.get("password"),
  };

  const response = await fetch("http://localhost:8000/api/v1/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(authData),
  });

  if (!response.ok) {
    throw json({ message: "Could not authenticate user." }, { status: 500 });
  }

  const resData = await response.json();
  const token = resData.token;

  localStorage.setItem("token", token);

  const expiration = new Date();
  expiration.setHours(expiration.getHours() + 1);

  localStorage.setItem("expiration", expiration.toISOString());

  return redirect("/feed");
}
