import React from "react";
import { Link, useLoaderData } from "react-router-dom";

import Sidebar from "./Sidebar.jsx";

export default function SearchList({ isFriends }) {
  const response = useLoaderData();

  return (
    <>
      <div className="flex min-h-screen h-full">
        <Sidebar />
        <div className="flex-1 p-4 flex mx-52">
          <div
            id="posts-container"
            className="bg-helenite-dark-grey rounded-md items-start flex p-4 min-w-full h-fit"
          >
            {response.length === 0 && (
              <div>
                <p className="text-2xl text-helenite-white">
                  <strong>
                    {isFriends
                      ? "This user has no friends yet :("
                      : "Sorry, we couldn't find any matches."}
                  </strong>
                </p>
              </div>
            )}
            {response.length > 1 &&
              response.map((profile) => (
                <div
                  id="single-profile-container"
                  className="flex flex-col rounded-md p-1 hover:bg-helenite-light-grey"
                  key={profile.endpoint}
                >
                  <Link to={`/profile/${profile.endpoint.slice(16, -1)}`}>
                    <div id="profile-container">
                      <img
                        src={profile.pfp}
                        className="w-80 h-80 object-contain"
                      />
                      <h2 className="text-center text-xl pt-4 text-helenite-white hover:underline">
                        <strong>{profile.get_full_name}</strong>
                      </h2>
                      <h3 className="text-center text-helenite-white">
                        @{profile.username}
                      </h3>
                    </div>
                  </Link>
                </div>
              ))}
            {response.length === 1 && (
              <div
                id="single-profile-container"
                className="flex flex-col rounded-md p-1 hover:bg-helenite-light-grey"
              >
                <Link to={`/profile/${response[0].username}`}>
                  <div id="profile-container">
                    <img
                      src={response[0].pfp}
                      className="w-80 h-80 object-contain"
                    />
                    <h2 className="text-center text-xl pt-4 text-helenite-white hover:underline">
                      <strong>{response[0].get_full_name}</strong>
                    </h2>
                    <h3 className="text-center text-helenite-white">
                      @{response[0].username}
                    </h3>
                  </div>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
