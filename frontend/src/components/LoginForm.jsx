import React, { useState } from "react";

export default function LoginForm() {
  const [showPassword, setShowPassowrd] = useState(false);

  const inputClass =
    "p-1 focus:outline-none focus:border-0 focus:outline-helenite-light-blue";

  function showPasswordHandler() {
    setShowPassowrd((oldState) => !oldState);
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const fd = new FormData(event.target);
    const data = Object.fromEntries(fd.entries());

    const response = await fetch("http://localhost:8000/api/v1/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      // TODO: this.
    }

    const responseData = await response.json();
    const token = responseData.token

    console.log(token);
  }

  return (
    <form
      id="main-element"
      className="flex flex-col h-screen items-center justify-center"
      onSubmit={handleSubmit}
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
            onClick={showPasswordHandler}
          >
            Show password
          </button>
        </div>
      </div>
    </form>
  );
}
