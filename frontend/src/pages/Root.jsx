import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import { loginActions } from "../store/login-slice.jsx";

import MainNavigation from "../components/MainNavigationBar.jsx";
import MainFooter from "../components/MainFooter.jsx";

export default function RootLayout() {
  const dispatch = useDispatch();
  dispatch(loginActions.setLoginCredentials());

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  if (isLoggedIn) {
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
