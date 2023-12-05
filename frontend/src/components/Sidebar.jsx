import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { userInfoActions } from "../store/user-info-slice";

export default function Sidebar() {
  const profilePicture = useSelector((state) => state.userInfo.pfp);
  const username = useSelector((state) => state.userInfo.username);
  const fullName = useSelector((state) => state.userInfo.fullname);

  const dispatch = useDispatch();
  dispatch(userInfoActions.setUserInfo());

  const buttonClass =
    "m-1 p-2 rounded-2xl bg-helenite-light-blue hover:text-helenite-white hover:bg-helenite-dark-blue hover:underline";

  return (
    <div className="fixed h-full flex items-center justify-center">
      <div className="bg-helenite-light-grey p-4 ml-4 rounded-md shadow-black shadow-sm">
        <a href="#">
          <div className="p-2">
            <img
              src={profilePicture}
              alt="authenticated user profile picture"
              className="rounded-full w-20 h-20 mx-auto object-cover"
            />
          </div>
          <div className="text-center text-helenite-white hover:underline">
            <h2><strong>{fullName}</strong></h2>
            <p>@{username}</p>
          </div>
        </a>
        <ul className="text-center">
          <li>
            <button className={buttonClass}>
              <a href="#">Photos</a>
            </button>
          </li>
          <li>
            <button className={buttonClass}>
              <a href="#">Friends</a>
            </button>
          </li>
          <li>
            <button className={buttonClass}>
              <a href="#">Account Settings</a>
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
}
