import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import HeleniteFullLogo from "/helenite_full_logo.png";
import { loginActions } from "../store/login-slice.js";
import { userInfoActions } from "../store/user-info-slice.js";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

export default function MainNavigationBar() {
  const [inputSearchValue, setInputSearchValue] = useState("");

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  const dispatch = useDispatch();

  const navigate = useNavigate();

  async function handleLogout() {
    const token = localStorage.getItem("token");
    const response = await fetch(`${backendURL}/api/v1/logout/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      // TODO: fix bad request on logout.
    }

    dispatch(loginActions.logout());
    dispatch(userInfoActions.logout());

    navigate("/");
  }

  async function handleSubmitSearch(event) {
    event.preventDefault();

    if (inputSearchValue !== "") {
      // TODO: this
    }
  }

  const loginButtonClass =
    "bg-helenite-dark-blue text-helenite-white hover:bg-helenite-light-blue hover:text-gray-500 px-4 py-2 ";

  return (
    <header className="fixed w-full">
      <nav className="bg-helenite-dark-grey p-2 flex">
        <div>
          <ul className="text-helenite-light-blue flex">
            <li>
              <Link to="/">
                <img
                  src={HeleniteFullLogo}
                  alt="A green gem with 'Helenite' written by its side"
                  className="h-12"
                />
              </Link>
            </li>
          </ul>
        </div>
        {isLoggedIn && (
          <form
            className="flex m-auto"
            onSubmit={(event) => handleSubmitSearch(event)}
          >
            <div>
              <input
                type="text"
                placeholder="I'm looking for..."
                value={inputSearchValue}
                className="bg-helenite-white text-helenite-dark-grey focus:outline-none focus:border-0 focus:outline-helenite-light-blue h-12"
              />
            </div>
            <button className="bg-helenite-light-blue text-helenite-dark-grey hover:text-gray-500 ml-1 px-4 py-2">
              Search
            </button>
          </form>
        )}
        <div className="items-end">
          {isLoggedIn ? (
            <button className={loginButtonClass} onClick={handleLogout}>
              Logout
            </button>
          ) : (
            <button className={loginButtonClass + "fixed right-2"}>
              <a href="login">Login</a>
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}
