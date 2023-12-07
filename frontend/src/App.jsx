import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Helmet } from "react-helmet";

import DiscoverPage, { loader as discoverLoader } from "./pages/Discover.jsx";
import FeedPage, { loader as feedLoader } from "./pages/Feed.jsx";
import ProtectedRoutes from "./components/ProtectedRoutes.jsx";
import ProfileDetailPage from "./pages/ProfileDetail.jsx";
import PostDetailPage from "./pages/PostDetail.jsx";
import SettingsPage from "./pages/Settings.jsx";
import AboutUsPage from "./pages/AboutUs.jsx";
import Register from "./pages/Register.jsx";
import RootLayout from "./pages/Root.jsx";
import ErrorPage from "./pages/Error.jsx";
import LoginPage from "./pages/Login.jsx";
import HomePage from "./pages/Home.jsx";

const router = createBrowserRouter([
  {
    // Unprotected.
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "login", element: <LoginPage /> },
      { path: "register", element: <Register /> },
      { path: "about-us", element: <AboutUsPage /> },
    ],
  },
  // Protected.
  {
    path: "/feed",
    element: <ProtectedRoutes />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <FeedPage />, loader: feedLoader },
      { path: "discover", element: <DiscoverPage />, loader: discoverLoader },
    ],
  },
  {
    path: "/profile",
    element: <ProtectedRoutes />,
    errorElement: <ErrorPage />,
    children: [
      { path: ":username", element: <ProfileDetailPage /> },
      { path: ":username/settings", element: <SettingsPage /> },
    ],
  },
  {
    path: "/post",
    element: <ProtectedRoutes />,
    errorElement: <ErrorPage />,
    children: [{ path: ":postId", element: <PostDetailPage /> }],
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
