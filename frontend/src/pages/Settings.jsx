import React from "react";
import { Helmet } from "react-helmet";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import SettingsComponent from "../components/Settings.jsx";

export default function SettingsPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Settings</title>
      </Helmet>
      <div>
        <div className="pt-16 min-h-screen bg-stone-800">
          <SettingsComponent />
        </div>
      </div>
    </>
  );
}

export async function loader({ request, params }) {
  const token = localStorage.getItem("token");
  const currentUser = localStorage.getItem("user-username");

  const response = await fetch(
    `${backendURL}/api/v1/profile/${currentUser}/change-settings/`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  // Profile doesn't belong to user.
  if (response.status === 403) {
    return {};
  }

  if (!response.ok) {
    const resData = await response.json();
    return resData;
  }

  const resData = await response.json();
  return resData;
}

export async function action({ request, params }) {}
