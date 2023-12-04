import React, { useEffect } from "react";
import { useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";

import ParticlesComponent from "../components/Particles.jsx";

export default function HomePage() {
  const navigate = useNavigate();

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  useEffect(() => {
    if (isLoggedIn) {
      navigate("/login");
    }
  }, []);

  const buttonClass =
    "bg-helenite-light-blue hover:bg-helenite-dark-blue hover:text-helenite-white rounded-md p-2";

  return (
    <>
      <div className="pt-16">
        <ParticlesComponent />
        <div
          id="main-element"
          className="flex flex-col h-screen items-center justify-center"
        >
          <div>
            <p className="text-3xl m-2 text-helenite-light-blue relative">
              <strong>Welcome to Helenite!</strong>
            </p>
          </div>
          <div className="text-center p-10 rounded-md bg-helenite-dark-grey shadow-2xl  flex relative">
            <div className="flex flex-col">
              <label className="text-white">Already have an account?</label>
              <Link to="/login">
                <button className={buttonClass}>Log in</button>
              </Link>
            </div>
            <div className="ml-4 flex flex-col">
              <label className="text-white">Doesn't have an account?</label>
              <Link to="/register">
                <button className={buttonClass}>Sign up</button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
