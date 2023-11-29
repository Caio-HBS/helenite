import React from "react";
import { Link } from "react-router-dom";

export default function HomePage() {
  const buttonClass =
    "bg-helenite-light-blue hover:bg-helenite-dark-blue rounded-md p-2";

  return (
    <div
      id="main-element"
      className="flex flex-col h-screen items-center justify-center"
    >
      <div className="text-center p-10 rounded-md bg-helenite-dark-grey shadow-2xl text-helenite-white flex">
        <div className="flex flex-col">
          <label>Already have an account?</label>
          <Link to="/login">
            <button className={buttonClass}>Log in</button>
          </Link>
        </div>
        <div className="ml-4 flex flex-col">
          <label>Doesn't have an account?</label>
          <Link to="/register">
            <button className={buttonClass}>Sign up</button>
          </Link>
        </div>
      </div>
    </div>
  );
}
