import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Helmet } from "react-helmet";

import ProfileDetailPage from "./pages/ProfileDetail.jsx";
import PostDetailPage from "./pages/PostDetail.jsx";
import SettingsPage from "./pages/Settings.jsx";
import AboutUsPage from "./pages/AboutUs.jsx";
import Register from "./pages/Register.jsx";
import RootLayout from "./pages/Root.jsx";
import ErrorPage from "./pages/Error.jsx";
import LoginPage, { action as loginAction } from "./pages/Login.jsx";
import HomePage from "./pages/Home.jsx";
import FeedPage from "./pages/Feed.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "/login", element: <LoginPage />, action: loginAction },
      { path: "/register", element: <Register /> },
      { path: "/about-us", element: <AboutUsPage /> },
      { path: "/post/:postId", element: <PostDetailPage /> },
      { path: "/profile/:username", element: <ProfileDetailPage /> },
      { path: "/profile/:username/settings", element: <SettingsPage /> },
    ],
  },
  {
    path: "/feed",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [{ index: true, element: <FeedPage /> }],
  },
]);

export default function App() {
  return (
    <>
      <Helmet>
        <title>Helenite | Home</title>
      </Helmet>
      <RouterProvider router={router} />
    </>
  );
}
