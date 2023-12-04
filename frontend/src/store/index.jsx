import { configureStore } from "@reduxjs/toolkit";

import loginSlice from "./login-slice.jsx";
import userInfoSlice from "./user-info-slice.jsx";

const store = configureStore({
  reducer: {
    login: loginSlice.reducer,
    userInfo: userInfoSlice.reducer,
  },
});

export default store;
