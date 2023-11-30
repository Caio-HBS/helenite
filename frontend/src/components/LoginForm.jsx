import React, { useState } from "react";
import { Form } from "react-router-dom";

export default function LoginForm() {
  const [showPassword, setShowPassowrd] = useState(false);

  const inputClass =
    "p-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue";

  function showPasswordHandler() {
    setShowPassowrd((oldState) => !oldState);
  }

  return (
    <Form
      action="/login"
      method="POST"
      className="flex flex-col h-screen items-center justify-center"
    >
      <div className="text-center p-10 rounded-md bg-helenite-dark-grey shadow-2xl">
        <div className="flex">
          <input
            type="text"
            name="username"
            placeholder="Your username"
            className={inputClass}
            required
          />
          <button className="rounded-md m-auto px-6 py-1 bg-helenite-light-blue text-stone-500 hover:bg-helenite-dark-blue hover:text-helenite-white">
            Login
          </button>
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
      </div>
    </Form>
  );
}
