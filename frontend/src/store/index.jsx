import { configureStore } from "@reduxjs/toolkit";

import loginSlice from "./login-slice.jsx";

const store = configureStore({
  reducer: {
    login: loginSlice.reducer,
  },
});

export default store;
