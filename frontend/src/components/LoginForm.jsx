import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import { loginActions } from "../store/login-slice.js";
import { userInfoActions } from "../store/user-info-slice.js";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import LoadingButton from "./LoadingButton.jsx";

export default function LoginForm() {
  const [showPassword, setShowPassowrd] = useState(false);
  const [validation, setValidation] = useState(true);
  const [sendingRequest, setSendingRequest] = useState(false);

  const dispatch = useDispatch();

  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();

    const fd = new FormData(event.target);
    const data = Object.fromEntries(fd.entries());

    if (data.password.length < 8) {
      setValidation(false);
    }
    setSendingRequest(true);
    const response = await fetch(`${backendURL}/api/v1/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      setValidation(false);
      setSendingRequest(false);

      return response;
    }

    const resData = await response.json();
    const token = resData.token;

    localStorage.setItem("token", token);

    const expiration = new Date();
    expiration.setHours(expiration.getHours() + 1);
    localStorage.setItem("expiration", expiration.toISOString());

    dispatch(loginActions.setLoginCredentials());

    const userInfoRes = await fetch(
      `${backendURL}/api/v1/profile/${data.username}/`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!userInfoRes.ok) {
      setValidation(false);
      setSendingRequest(false);

      return response; //TODO: fix bad request on login.
    }

    const userInfoResData = await userInfoRes.json();

    localStorage.setItem("user-fullname", userInfoResData.get_full_name);
    localStorage.setItem("user-username", userInfoResData.username);
    localStorage.setItem("user-pfp", userInfoResData.pfp);

    dispatch(userInfoActions.setUserInfo());

    setSendingRequest(false);
    navigate("/feed");
  }

  function showPasswordHandler() {
    setShowPassowrd((oldState) => !oldState);
  }

  const inputClass =
    "p-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue";

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col h-screen items-center justify-center relative"
    >
      <div className="text-center p-10 rounded-md bg-helenite-dark-grey shadow-md shadow-stone-900">
        <div className="flex">
          <input
            type="text"
            name="username"
            placeholder="Your username"
            className={inputClass}
            required
          />
          {!sendingRequest && (
            <button className="rounded-md m-auto px-6 py-1 bg-helenite-light-blue text-stone-500 hover:bg-helenite-dark-blue hover:text-helenite-white">
              Login
            </button>
          )}
          {sendingRequest && (
            <LoadingButton
              buttonColor="bg-helenite-light-blue"
              buttonText="Wait"
              textColor="text-stone-800"
              padding="px-5 py-1 text-sm"
            />
          )}
        </div>
        <div className="mt-2 text-helenite-dark-grey">
          <input
            type={showPassword ? "text" : "password"}
            name="password"
            minLength={8}
            placeholder="Your password"
            className={inputClass}
            required
          />
          <button
            className="ml-2 text-helenite-light-blue hover:text-helenite-dark-blue text-sm"
            type="button"
            onClick={showPasswordHandler}
          >
            Show password
          </button>
        </div>
        {!validation && (
          <p className="text-left pt-1 pb-0 text-red-600">
            Username or password invalid.
          </p>
        )}
      </div>
    </form>
  );
}
