import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

import Sidebar from "./Sidebar.jsx";

export default function FeedComponent() {
  const navigate = useNavigate();

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);

  // useEffect(() => {
  //   if (isLoggedIn) {
  //     navigate("/login");
  //   }
  // }, []);

  return (
    <>
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 p-4 flex ml-52">
          <div
            id="posts-container"
            className="bg-helenite-green rounded-md items-start p-4"
          >
            <div id="single-post-container" className="">
              <div id="post-header">
                <img />
                <div>
                  <h2>Caio Bianchi</h2>
                  <h3>@caiohbs</h3>
                </div>
              </div>
              <div id="post-info">
                <img />
                <p>
                  Lorem, ipsum dolor sit amet consectetur adipisicing elit.
                  Voluptate a necessitatibus numquam. Repellat provident omnis
                  possimus tempora architecto dolore doloribus totam, eveniet
                  at, et, maiores aperiam aliquam veniam sint ducimus.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
