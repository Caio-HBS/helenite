import React from "react";
import Helmet from "react-helmet";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import ProfileComponent from "../components/ProfileComponent.jsx";

export default function ProfileDetailPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Profile</title>
      </Helmet>
      <div>
        <div className="pt-16 h-full pb-4 bg-stone-800">
          <ProfileComponent />
        </div>
      </div>
    </>
  );
}

export async function loader({ request, params }) {
  const token = localStorage.getItem("token");
  const profile = params.username;

  const response = await fetch(`${backendURL}/api/v1/profile/${profile}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    return response;
  }

  const resData = await response.json();
  return resData;
}
