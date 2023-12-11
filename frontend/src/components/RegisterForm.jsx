import React, { useState } from "react";

import LoadingButton from "./LoadingButton.jsx";

export default function RegisterForm() {
  const [showPassword, setShowPassowrd] = useState(false);
  const [validation, setValidation] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  function showPasswordHandler() {
    setShowPassowrd((oldState) => !oldState);
  }

  const inputClass =
    "w-full py-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue";

  const divClass = "py-1";

  return (
    // TODO: add functionality.
    // TODO: implement validarotors.

    <>
      <form className="flex flex-col h-screen items-center justify-center relative">
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
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="email"
              name="email"
              placeholder="Your email"
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="slug"
              name="custom_slug_profile"
              placeholder="Path for your profile (blank for username)"
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="first_name"
              placeholder="Your First Name"
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="last_name"
              placeholder="Your Last Name"
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="date"
              name="birthday"
              className={inputClass}
              required
            />
          </div>
          <div className={divClass}>
            <input
              type="checkbox"
              name="show_birthday"
              className="py-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
            />
            <label className="pl-2 text-helenite-white">
              Make my birthday public
            </label>
          </div>
          <div className={divClass}>
            <input
              type="text"
              name="birth_place"
              placeholder="Where were you born?"
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
              name="private_profile"
              className="py-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
            />
            <label className="pl-2 text-helenite-white">
              Make my profile private
            </label>
          </div>
          {!validation && (
            <p className="text-red-600">
              <strong>{errorMsg}</strong>
            </p>
          )}
          <div className="pt-2 text-center">
            {showPassword && (
              <LoadingButton
                buttonText="Loading..."
                textColor="text-helenite-white"
                buttonColor="bg-helenite-dark-blue"
                padding="px-5 py-2.5 text-lg"
              />
            )}
            {!showPassword && (
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
