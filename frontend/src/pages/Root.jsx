import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import { loginActions } from "../store/login-slice.js";

import MainNavigation from "../components/MainNavigationBar.jsx";
import MainFooter from "../components/MainFooter.jsx";

export default function RootLayout() {
  const location = useLocation();

  const dispatch = useDispatch();
  dispatch(loginActions.setLoginCredentials());

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  if (isLoggedIn && location.pathname !== "/about-us") {
    return <Navigate to="/feed" />;
  }

  return (
    <>
      <MainNavigation />
      <main>
        <Outlet />
      </main>
      <MainFooter />
    </>
  );
}
