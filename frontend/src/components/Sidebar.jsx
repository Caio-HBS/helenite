import React from "react";

import defaultPFP from "../../../backend/uploads/profile_pictures/default_pfp.png"; //TODO: change this.

export default function Sidebar() {
  const buttonClass = "m-1 p-2 rounded-2xl bg-helenite-green hover:text-red-500 hover:underline"; //TODO: change this.

  return (
    <div className="fixed h-full flex items-center justify-center">
      <div className="bg-gray-200 p-4 ml-4 rounded-md shadow-black shadow-sm">
        <a href="#">
          <div className="p-2">
            <img
              src={defaultPFP}
              alt="authenticated user profile picture"
              className="rounded-full w-20 h-20"
            />
          </div>
          <div className="text-center hover:underline">
            <h2 className="">Caio Bianchi</h2>
            <p className="">@caiohbs</p>
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
