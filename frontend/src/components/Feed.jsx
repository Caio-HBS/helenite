import React from "react";
import { Link, useLoaderData } from "react-router-dom";

import Sidebar from "./Sidebar.jsx";
import TransformDate from "./TransformDate.jsx";
import NewPost from "./NewPost.jsx";

export default function FeedComponent({ newPostComponent }) {
  const response = useLoaderData();

  return (
    <>
      <div className="flex h-screen">
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
                  <Link to={`/profile/${post.profile.username}`}>
                    <img
                      src={post.profile.pfp}
                      className="rounded-full w-20 h-20 object-cover"
                    />
                  </Link>
                  <div id="name-username" className="m-1">
                    <Link to={`/profile/${post.profile.username}`}>
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
                      className=" rounded-lg my-2 mr-2"
                    />
                    <p className="ml-1 text-justify">{post.post_text}</p>
                  </div>
                  <div
                    id="post-likes-comments"
                    className="ml-1 flex hover:underline"
                  >
                    <p>
                      {post.likes_count} like{post.likes_count > 1 ? "s" : ""}
                    </p>
                    <p className="ml-2">
                      {post.comments_count} comment
                      {post.comments_count > 1 ? "s" : ""}
                    </p>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
