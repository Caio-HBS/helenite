import React from "react";
import { useDispatch } from "react-redux";

import { loginActions } from "../store/login-slice.jsx";
import { Helmet } from "react-helmet";

export default function FeedPage() {
  return (
    <>
      <Helmet>
        <title>Helenite | Feed</title>
      </Helmet>
    </>
  );
}
