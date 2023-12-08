import React from "react";
import { Helmet } from "react-helmet";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import SinglePost from "../components/SinglePost.jsx";

export default function PostDetailPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Post</title>
      </Helmet>
      <div>
        <div className="pt-16 bg-stone-800">
          <SinglePost />
        </div>
      </div>
    </>
  );
}

export async function loader({ request, params }) {
  const token = localStorage.getItem("token");
  const postId = params.postId;

  const response = await fetch(`${backendURL}/api/v1/profile/post/${postId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  const resData = await response.json();
  return resData;
}
