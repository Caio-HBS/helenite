import React from "react";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import Sidebar from "./Sidebar.jsx";
import TransformDate from "./TransformDate.jsx";
import NewPost from "./NewPost.jsx";

export default function FeedComponent({ newPostComponent }) {
  // BUG: user loses scroll position on like.
  const token = localStorage.getItem("token");

  const navigate = useNavigate();
  const currentUser = useSelector((state) => state.userInfo.username);
  const response = useLoaderData();

  async function handleLike(event, endpoint) {
    event.preventDefault();

    const response = await fetch(`${backendURL}/api/v1/feed/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        post_slug: `${endpoint}`,
      }),
    });

    if (!response.ok) {
      // TODO: fix bad request on like.
      return response;
    }

    navigate(0);
  }

  return (
    <>
      <div className="flex min-h-screen h-full">
        <Sidebar />
        <div className="flex-1 p-4 flex mx-52">
          <div
            id="posts-container"
            className="bg-helenite-dark-grey rounded-md items-start p-4"
          >
            {newPostComponent && <NewPost />}
            {response.results.map((post) => (
              <div
                id="single-post-container"
                className="p-2 m-2 bg-helenite-light-grey rounded-lg text-white"
                key={post.endpoint}
              >
                <div id="post-header" className="flex">
                  <Link to={`/profile/${post.profile.endpoint.slice(16, -1)}`}>
                    <img
                      src={post.profile.pfp}
                      className="rounded-full w-20 h-20 object-cover"
                    />
                  </Link>
                  <div id="name-username" className="m-1">
                    <Link
                      to={`/profile/${post.profile.endpoint.slice(16, -1)}`}
                    >
                      <h2 className="hover:underline text-lg">
                        <strong>{post.profile.get_full_name}</strong>
                      </h2>
                    </Link>
                    <h3 className="text-base">@{post.profile.username}</h3>
                    <TransformDate date={post.post_publication_date} />
                  </div>
                </div>
                <Link to={`/post/${post.endpoint.slice(21, -1)}`}>
                  <div id="post-info">
                    <img
                      src={post.post_image}
                      className="max-w-2xl object-cover rounded-lg my-2 mr-2"
                    />
                    <p className="ml-1 text-justify max-w-screen-2xl">
                      {post.post_text}
                    </p>
                  </div>
                </Link>
                <div id="post-likes-comments" className="ml-1 flex">
                  <form
                    onSubmit={(event) =>
                      handleLike(event, post.endpoint.slice(21, -1))
                    }
                  >
                    <button
                      className={
                        post.likes.includes(currentUser)
                          ? "text-helenite-green hover:text-white hover:underline"
                          : "hover:text-helenite-green hover:underline"
                      }
                    >
                      <strong>
                        {post.likes_count} like{post.likes_count > 1 ? "s" : ""}
                      </strong>
                    </button>
                  </form>
                  <p className="ml-1"> &#9830;</p>
                  <Link to={`/post/${post.endpoint.slice(21, -1)}`}>
                    <p className="ml-1">
                      {post.comments_count} comment
                      {post.comments_count > 1 ? "s" : ""}
                    </p>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
