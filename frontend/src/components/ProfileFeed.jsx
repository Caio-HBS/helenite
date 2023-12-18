import React from "react";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { ToastContainer, toast } from "react-toastify";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import TransformDate from "./TransformDate.jsx";
import NewPost from "./NewPost.jsx";

export default function ProfileFeed() {
  const token = localStorage.getItem("token");
  const currentUser = useSelector((state) => state.userInfo.username);

  const response = useLoaderData();

  const navigate = useNavigate();

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
      toast.error("Error while trying to like post, please try again.", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      return;
    }

    navigate(0);
  }

  return (
    <div className="flex justify-center mx-40 m-5 min-h-screen h-full rounded-lg bg-helenite-dark-grey">
      <ToastContainer />
      <div
        id="posts-container"
        className="bg-helenite-dark-grey rounded-md w-full items-start p-4"
      >
        {currentUser === response.username && <NewPost />}
        <div>
          {response.posts.length > 0 ? (
            response.posts.map((post) => (
              <div
                id="single-post-container"
                className="p-2 m-2 bg-helenite-light-grey rounded-lg text-white"
                key={post.endpoint}
              >
                <div id="post-header" className="flex">
                  <img
                    src={response.pfp}
                    className="rounded-full w-20 h-20 object-cover"
                  />
                  <div id="name-username" className="m-1">
                    <h2 className="hover:underline text-lg">
                      <strong>{response.get_full_name}</strong>
                    </h2>
                    <h3 className="text-base">@{response.username}</h3>
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
            ))
          ) : (
            <div>
              <p className="text-2xl text-helenite-white">
                <strong>This user hasn't made a post yet.</strong>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
