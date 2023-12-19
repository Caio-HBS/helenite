import React from "react";
import { Helmet } from "react-helmet";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import SearchList from "../components/SearchList.jsx";

export default function SearchPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Search</title>
      </Helmet>
      <div>
        <div className="pt-16 bg-stone-800">
          <SearchList isFriends={false} />
        </div>
      </div>
    </>
  );
}

export async function loader({ request, params }) {
  const url = new URL(request.url);
  const searchTerms = url.searchParams.get("q");
  const termsArray = searchTerms.split(" ");
  const queryURL = `${backendURL}/api/v1/search/?q=${termsArray[0]}${
    termsArray[1] ? "+" + termsArray[1] : ""
  }`;

  const token = localStorage.getItem("token");

  // Only two parameters are accepted for query.
  const response = await fetch(queryURL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status === 204) {
    return [];
  }

  if (!response.ok) {
    return [];
  }

  const resData = await response.json();
  return resData;
}
