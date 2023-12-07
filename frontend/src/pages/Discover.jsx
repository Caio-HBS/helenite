import React from "react";
import { Helmet } from "react-helmet";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import FeedComponent from "../components/Feed.jsx";

export default function DiscoverPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Discover</title>
      </Helmet>
      <div>
        <div className="pt-16 bg-stone-800">
          <FeedComponent newPostComponent={false} />
        </div>
      </div>
    </>
  );
}

export async function loader() {
  const token = localStorage.getItem("token");

  const response = await fetch(`${backendURL}/api/v1/feed/discover/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw json({ message: "Could not fetch events." }, { status: 500 });
  } else {
    const resData = await response.json();
    return resData;
  }
}
