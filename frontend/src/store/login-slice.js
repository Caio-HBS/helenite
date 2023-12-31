import { createSlice } from "@reduxjs/toolkit";

const loginSlice = createSlice({
  name: "login",
  initialState: {
    isLoggedIn: false,
    token: null,
    expirationDate: null,
  },
  reducers: {
    setLoginCredentials(state) {
      state.token = localStorage.getItem("token") || null;
      state.expirationDate = localStorage.getItem("expiration") || null;
      state.isLoggedIn = state.token && state.expirationDate ? true : false;
    },
    logout(state) {
      state.isLoggedIn = false;
      localStorage.removeItem("token");
      state.token = null;
      localStorage.removeItem("expiration");
      state.expirationDate = null;
    },
  },
});

export const loginActions = loginSlice.actions;

export default loginSlice;
