import React, { useEffect } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch } from "react-redux";

import { loginActions } from "../store/login-slice.jsx";

import MainNavigation from "../components/MainNavigationBar.jsx";
import MainFooter from "../components/MainFooter.jsx";

export default function RootLayout() {
  // const dispatch = useDispatch();

  // useEffect(() => {
  //   dispatch(loginActions.setLoginCredentials());
  // }, []);

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
