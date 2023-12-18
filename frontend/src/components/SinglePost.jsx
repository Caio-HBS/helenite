import React from "react";
import { useSelector } from "react-redux";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import TransformDate from "./TransformDate.jsx";
import NewComment from "./NewComment.jsx";
import Sidebar from "./Sidebar.jsx";

export default function SinglePost() {
  const token = localStorage.getItem("token");

  const response = useLoaderData();

  const navigate = useNavigate();

  const currentUser = useSelector((state) => state.userInfo.username);

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

  async function handleDeletePost(event) {
    event.preventDefault();

    const fetchDeleteResponse = await fetch(
      `${backendURL}${response.endpoint}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!fetchDeleteResponse.ok) {
      toast.error("Error while trying to delete post, please try again.", {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
    }

    const resData = await fetchDeleteResponse.json();
    navigate("/feed");
  }

  return (
    <>
      <div className="flex min-h-screen h-full">
        <Sidebar />
        <div className="flex-1 p-4 flex mx-52">
          <div
            id="posts-container"
            className="bg-helenite-dark-grey rounded-md items-start p-4 min-w-full"
          >
            {currentUser === response.profile.username && (
              <form
                className="text-right px-2"
                onSubmit={(event) => handleDeletePost(event)}
              >
                <button className="rounded-sm p-1 bg-red-600 hover:bg-red-800 text-helenite-white">
                  <strong>Delete post</strong>
                </button>
              </form>
            )}
            {
              <div
                id="single-post-container"
                className="p-2 m-2 bg-helenite-light-grey rounded-lg text-white"
              >
                <div id="post-header" className="flex">
                  <img
                    src={response.profile.pfp}
                    className="rounded-full w-20 h-20 object-cover"
                  />
                  <div id="name-username" className="m-1">
                    <h2 className="hover:underline text-lg">
                      <strong>{response.profile.get_full_name}</strong>
                    </h2>
                    <h3 className="text-base">@{response.profile.username}</h3>
                    <TransformDate date={response.post_publication_date} />
                  </div>
                </div>
                <div id="post-info">
                  <img
                    src={response.post_image}
                    className="max-w-2xl object-cover rounded-lg my-2 mr-2"
                  />
                  <p className="ml-1 text-justify">{response.post_text}</p>
                </div>
                <div id="post-likes-comments" className="ml-1 flex">
                  <form
                    onSubmit={(event) =>
                      handleLike(event, response.endpoint.slice(21, -1))
                    }
                  >
                    <button
                      className={
                        response.likes.includes(currentUser)
                          ? "text-helenite-green hover:text-white hover:underline"
                          : "hover:text-helenite-green hover:underline"
                      }
                    >
                      <strong>
                        {response.likes_count} like
                        {response.likes_count > 1 ? "s" : ""}
                      </strong>
                    </button>
                  </form>
                </div>
              </div>
            }
            <div id="comment-title">
              <p className="m-2 text-2xl text-helenite-white">
                <strong>Comments:</strong>
              </p>
            </div>
            <div id="comment-section" className="m-2">
              {response.comments && response.comments.length > 0 ? (
                response.comments.map((comment) => (
                  <Link
                    to={`${response.profile.endpoint}`}
                    key={comment.comment_text}
                  >
                    <div
                      id="single-comment"
                      className="flex p-2 my-2 w-fit rounded-lg text-justify max-w-screen-2xl bg-helenite-light-grey"
                    >
                      <h3 className="text-xl text-helenite-light-blue hover:underline">
                        <strong>@{comment.comment_user}:</strong>
                      </h3>
                      <p className="text-lg ml-2 text-helenite-white">
                        {comment.comment_text}
                      </p>
                    </div>
                  </Link>
                ))
              ) : (
                <p className="p-2 w-fit rounded-lg text-md bg-helenite-light-grey text-helenite-white">
                  There are no comments here yet.
                </p>
              )}
              <NewComment
                navigate={navigate}
                currentUser={currentUser}
                token={token}
                endpoint={response.endpoint}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
