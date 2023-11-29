import React from "react";
import { Outlet } from "react-router-dom";

import MainNavigation from "../components/MainNavigationBar.jsx";
import MainFooter from "../components/MainFooter.jsx";

export default function RootLayout() {
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
