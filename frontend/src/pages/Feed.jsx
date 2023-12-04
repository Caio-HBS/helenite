import React from "react";
import { Helmet } from "react-helmet";
import { useSelector } from "react-redux";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import FeedComponent from "../components/Feed.jsx";

export default function FeedPage() {
  // const token = useSelector(state.login.token);

  return (
    <>
      <Helmet>
        <title>Helenite | Feed</title>
      </Helmet>
      <div>
        <div className="pt-16 bg-stone-800 h-fit">
          <FeedComponent />
        </div>
      </div>
    </>
  );
}

export async function loader() {
  const response = await fetch(`${backendURL}/api/v1/feed/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer 6cfa6de9e61a5c3ee43c56227cfa15a55797f833`,
    },
  });

  if (!response.ok) {
    throw json({ message: "Could not fetch events." }, { status: 500 });
  } else {
    const resData = await response.json();
    return resData;
  }
}
