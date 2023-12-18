import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";

import {
  isBirthplace,
  isDate,
  isEmail,
  isSlug,
  isValidName,
  isValidPassword,
} from "../utils/validation.js";
const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import LoadingButton from "./LoadingButton.jsx";

export default function RegisterForm() {
  const [showPassword, setShowPassowrd] = useState(false);
  const [sendingRequest, setSendingRequest] = useState(false);
  const [validation, setValidation] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [profileSlug, setProfileSlug] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [birthday, setBirthday] = useState("");
  const [showBirthday, setShowBirthday] = useState(true);
  const [birthPlace, setBirthPlace] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [privateProfile, setpPivateProfile] = useState(false);

  const navigate = useNavigate();

  const inputClass =
    "w-full py-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue";

  const divClass = "py-1";

  function showPasswordHandler() {
    setShowPassowrd((oldState) => !oldState);
  }

  async function handleRegistration(event) {
    event.preventDefault();

    const formData = new FormData();

    const user = username;
    if (user !== "" && isValidName(user)) {
      formData.append("username", user);
    } else {
      setValidation(false);
      setErrorMsg("Username is not valid.");
      return;
    }

    const userEmail = email;
    if (userEmail !== "" && isEmail(userEmail)) {
      formData.append("email", userEmail);
    } else {
      setValidation(false);
      setErrorMsg("Email is not valid.");
      return;
    }

    const slug = profileSlug;
    if (slug !== "" && isSlug(slug)) {
      formData.append("custom_slug_profile", slug);
    } else {
      setValidation(false);
      setErrorMsg("Custom path to profile is not valid.");
      return;
    }

    const fName = firstName;
    const lName = lastName;
    if (
      fName !== "" &&
      lName !== "" &&
      isValidName(fName) &&
      isValidName(fName)
    ) {
      formData.append("first_name", fName);
      formData.append("last_name", lName);
    } else {
      setValidation(false);
      setErrorMsg("First or last name not valid.");
      return;
    }

    const date = birthday;
    if (date !== "" && isDate(date)) {
      formData.append("birthday", date);
    } else {
      setValidation(false);
      setErrorMsg("Birthday is not valid.");
      return;
    }

    const showBirth = showBirthday;
    formData.append("show_birthday", showBirth);

    const place = birthPlace;
    if (place !== "" && isBirthplace(place)) {
      formData.append("birth_place", birthPlace);
    } else {
      setValidation(false);
      setErrorMsg("Not a valid country.");
      return;
    }

    const pass = password;
    const confirmPass = confirmPassword;
    if (pass !== "" && confirmPass !== "") {
      if (
        pass === confirmPass &&
        isValidPassword(pass) &&
        isValidPassword(confirmPass)
      ) {
        formData.append("password", pass);
        formData.append("confirmation_password", confirmPass);
      } else {
        setValidation(false);
        setErrorMsg("Passwords don't match.");
        return;
      }
    } else {
      setValidation(false);
      setErrorMsg("Please choose valid passwords.");
      return;
    }

    const privProfile = privateProfile;
    formData.append("private_profile", privProfile);

    setSendingRequest(true);

    const response = await fetch(`${backendURL}/api/v1/register/`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const resError = await response.json();
      toast.error(resError.message, {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      setSendingRequest(false);
    }

    const resData = await response.json();
    console.log(resData);
    toast.success(resData.detail, {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
    });
    setSendingRequest(false);
    const delayNavigate = setTimeout(() => {
      clearTimeout(delayNavigate);
      navigate("/login");
    }, 5000);
  }

  return (
    <>
      <ToastContainer />
      <form
        onSubmit={(event) => handleRegistration(event)}
        className="flex flex-col h-screen items-center justify-center relative"
      >
        <div className="text-left p-10 rounded-md bg-helenite-dark-grey shadow-md shadow-stone-900">
          <div>
            <p className="text-2xl text-center pb-1 text-helenite-light-blue">
              <strong>Enter the world of Helenite!</strong>
            </p>
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="username"
              placeholder="Your username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="email"
              name="email"
              placeholder="Your email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="slug"
              name="custom_slug_profile"
              placeholder="Path for your profile (blank for username)"
              value={profileSlug}
              onChange={(event) => setProfileSlug(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="first_name"
              placeholder="Your First Name"
              value={firstName}
              onChange={(event) => setFirstName(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="last_name"
              placeholder="Your Last Name"
              value={lastName}
              onChange={(event) => setLastName(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="date"
              name="birthday"
              value={birthday}
              onChange={(event) => setBirthday(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="checkbox"
              id="show_birthday"
              onChange={(event) => setShowBirthday(event.target.value)}
              className="py-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
            />
            <label htmlFor="show_birthday" className="pl-2 text-helenite-white">
              Make my birthday public
            </label>
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="birth_place"
              placeholder="Where were you born? (Country)"
              value={birthPlace}
              onChange={(event) => setBirthPlace(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className="mt-2 text-helenite-dark-grey">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              minLength={8}
              placeholder="Your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className={inputClass}
              required
            />
          </div>
          <div className="mt-2 text-helenite-dark-grey">
            <input
              type={showPassword ? "text" : "password"}
              name="confirmation_password"
              minLength={8}
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              className={inputClass}
              required
            />
            <button
              className="text-md text-helenite-light-blue hover:text-helenite-dark-blue text-justify"
              type="button"
              onClick={showPasswordHandler}
            >
              Show passwords
            </button>
          </div>
          <div className={divClass}>
            <input
              type="checkbox"
              id="private_profile"
              onChange={(event) => setpPivateProfile(event.target.value)}
              className="py-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
            />
            <label
              htmlFor="private_profile"
              className="pl-2 text-helenite-white"
            >
              Make my profile private
            </label>
          </div>
          {!validation && (
            <p className="text-red-600">
              <strong>{errorMsg}</strong>
            </p>
          )}
          <div className="pt-2 text-center">
            {sendingRequest && (
              <LoadingButton
                buttonText="Loading..."
                textColor="text-helenite-white"
                buttonColor="bg-helenite-dark-blue"
                padding="px-5 py-2.5 text-lg"
              />
            )}
            {!sendingRequest && (
              <button className="p-2 text-xl rounded-lg bg-helenite-light-blue hover:bg-helenite-dark-blue hover:text-helenite-white">
                Take me to Helenite!
              </button>
            )}
          </div>
        </div>
      </form>
    </>
  );
}
