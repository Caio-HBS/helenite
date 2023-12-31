import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { ToastContainer, toast } from "react-toastify";

import HeleniteFullLogo from "/helenite_full_logo.png";
import algoliaLogo from "/Algolia-logo-white.svg";
import { loginActions } from "../store/login-slice.js";
import { userInfoActions } from "../store/user-info-slice.js";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

export default function MainNavigationBar() {
  const [inputSearchValue, setInputSearchValue] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  const dispatch = useDispatch();

  const navigate = useNavigate();

  const token = localStorage.getItem("token");

  function handleInputChange(event) {
    // Prevents users from searching more than two words.
    const value = event.target.value;
    const words = value.split(" ");
    const uniqueWords = [...new Set(words)].slice(0, 2);
    const newValue = uniqueWords.join(" ");

    setInputSearchValue(newValue);
  }

  function handleToggleDropdown() {
    setShowDropdown(!showDropdown);
  }

  async function handleLogout() {
    const response = await fetch(`${backendURL}/api/v1/logout/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      toast.error("Error while trying to logout, please try again.", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      return;
    }

    dispatch(loginActions.logout());
    dispatch(userInfoActions.logout());

    navigate("/");
  }

  async function handleSubmitSearch(event) {
    event.preventDefault();
    setShowDropdown(!showDropdown);

    if (inputSearchValue !== "") {
      const searchUrl = `/search?q=${encodeURIComponent(inputSearchValue)}`;

      navigate(searchUrl);
    }
  }

  const loginButtonClass =
    "bg-helenite-dark-blue text-helenite-white hover:bg-helenite-light-blue hover:text-gray-500 px-4 py-2 ";

  return (
    <header className="fixed w-full">
      <ToastContainer />
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
                onChange={handleInputChange}
                onClick={handleToggleDropdown}
                className="bg-helenite-white text-helenite-dark-grey focus:outline-none focus:border-0 focus:outline-helenite-light-blue h-12"
              />
              {showDropdown && (
                <div className="flex absolute mt-2 p-2 h-12 rounded-sm border bg-helenite-dark-grey">
                  <p className="text-sm pr-2 text-white">powered by:</p>
                  <img src={algoliaLogo} alt="Algolia Logo" />
                </div>
              )}
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
