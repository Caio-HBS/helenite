import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";

import { userInfoActions } from "../store/user-info-slice.js";

export default function Sidebar() {
  const profilePicture = useSelector((state) => state.userInfo.pfp);
  const username = useSelector((state) => state.userInfo.username);
  const fullName = useSelector((state) => state.userInfo.fullname);
  const profileSlug = useSelector((state) => state.userInfo.profileSlug);

  const dispatch = useDispatch();
  dispatch(userInfoActions.setUserInfo());

  const buttonClass =
    "m-1 p-2 rounded-2xl text-xl text-helenite-light-grey bg-helenite-light-blue hover:text-helenite-white hover:bg-helenite-dark-blue";

  return (
    <div className="fixed h-full flex items-center justify-center">
      <div className="bg-helenite-light-grey p-4 ml-4 rounded-md shadow-black shadow-sm">
        <Link to={`/profile/${profileSlug}`}>
          <div className="p-1 hover:bg-stone-500 rounded-full">
            <img
              src={profilePicture}
              alt="authenticated user profile picture"
              className="rounded-full w-20 h-20 mx-auto object-cover"
            />
          </div>
          <div className="text-center text-helenite-white">
            <h2 className="hover:underline">
              <strong>{fullName}</strong>
            </h2>
            <p className="hover:underline">@{username}</p>
          </div>
        </Link>
        <ul className="text-center">
          <li>
            <button className={buttonClass}>
              <Link to={`/profile/${profileSlug}/friends`}>
                <strong>Friends</strong>
              </Link>
            </button>
          </li>
          <li>
            <button className={buttonClass}>
              <Link to={`/profile/${profileSlug}/settings`}>
                <strong>Settings</strong>
              </Link>
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
}
