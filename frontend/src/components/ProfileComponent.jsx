import React from "react";
import { useLoaderData } from "react-router-dom";

import ProfileHeader from "./ProfileHeader.jsx";
import ProfileFeed from "./ProfileFeed.jsx";

export default function ProfileComponent() {
  const response = useLoaderData();

  return (
    <>
      <div>
        <ProfileHeader />
      </div>
      <div>
        <div>
          <ProfileFeed />
        </div>
      </div>
    </>
  );
}
