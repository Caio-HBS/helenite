import { configureStore } from "@reduxjs/toolkit";

import loginSlice from "./login-slice.js";
import userInfoSlice from "./user-info-slice.js";

const store = configureStore({
  reducer: {
    login: loginSlice.reducer,
    userInfo: userInfoSlice.reducer,
  },
});

export default store;
