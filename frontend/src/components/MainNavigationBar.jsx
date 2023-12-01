import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import HeleniteFullLogo from "/helenite_full_logo.png";
import { loginActions } from "../store/login-slice.jsx";

export default function MainNavigationBar() {
  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  const dispatch = useDispatch();

  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("expiration");

    dispatch(loginActions.logout());

    navigate("/");
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
          <div className="flex m-auto">
            <div>
              <input
                type="text"
                placeholder="I'm looking for..."
                className="bg-helenite-white text-helenite-dark-grey focus:outline-none focus:border-0 focus:outline-helenite-light-blue h-12"
              />
            </div>
            <button className="bg-helenite-light-blue text-helenite-dark-grey hover:text-gray-500 ml-1 px-4 py-2">
              Search
            </button>
          </div>
        )}
        <div className="items-end">
          {isLoggedIn ? (
            <button className={loginButtonClass} onClick={handleLogout}>
              Logout
            </button>
          ) : (
            <button className={loginButtonClass + "fixed right-2"}>
              <a href="/login">Login</a>
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}
