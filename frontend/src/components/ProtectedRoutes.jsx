import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import { loginActions } from "../store/login-slice.js";

import MainNavigation from "../components/MainNavigationBar.jsx";
import MainFooter from "./MainFooter.jsx";

export default function ProtectedRoutes() {
  const dispatch = useDispatch();
  dispatch(loginActions.setLoginCredentials());

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  if (isLoggedIn) {
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

  return <Navigate to="/login" />;
}
