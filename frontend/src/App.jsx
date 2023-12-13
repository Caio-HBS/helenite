import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Helmet } from "react-helmet";

import ProtectedRoutes from "./components/ProtectedRoutes.jsx";

import SettingsPage, {
  loader as settingsLoader,
  action as settingsAction,
} from "./pages/Settings.jsx";
import PostDetailPage, {
  loader as postDetailLoader,
} from "./pages/PostDetail.jsx";
import ProfileDetailPage, {
  loader as profileLoader,
} from "./pages/ProfileDetail.jsx";
import DiscoverPage, { loader as discoverLoader } from "./pages/Discover.jsx";
import SearchPage, { loader as searchLoader } from "./pages/Search.jsx";
import FeedPage, { loader as feedLoader } from "./pages/Feed.jsx";
import AboutUsPage from "./pages/AboutUs.jsx";
import FriendsPage from "./pages/Friends.jsx";
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
      {
        path: ":username",
        element: <ProfileDetailPage />,
        loader: profileLoader,
      },
      {
        path: ":username/settings",
        element: <SettingsPage />,
        loader: settingsLoader,
        action: settingsAction,
      },
      {
        path: ":username/friends",
        element: <FriendsPage />,
      },
    ],
  },
  {
    path: "/post",
    element: <ProtectedRoutes />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: ":postId",
        element: <PostDetailPage />,
        loader: postDetailLoader,
      },
    ],
  },
  {
    path: "/search",
    element: <ProtectedRoutes />,
    errorElement: <ErrorPage />,
    children: [{ index: true, element: <SearchPage />, loader: searchLoader }],
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
