import React from "react";
import { Helmet } from "react-helmet";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import SearchList from "../components/SearchList.jsx";

export default function FriendsPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Friends</title>
      </Helmet>
      <div>
        <div className="pt-16 bg-stone-800">
          <SearchList isFriends={true} />
        </div>
      </div>
    </>
  );
}

export async function loader({ request, params }) {
  const token = localStorage.getItem("token");
  const profile = params.username;

  const response = await fetch(`${backendURL}/api/v1/profile/${profile}/friends/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    return {};
  }

  const resData = await response.json();
  return resData.results[0].friends;
}
