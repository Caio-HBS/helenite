import { createSlice } from "@reduxjs/toolkit";

const loginSlice = createSlice({
  name: "login",
  initialState: {
    isLoggedIn: false,
    token: null,
  },
  reducers: {
    login() {
      // TODO: this.
    },
    logout() {
      // TODO: this.
    },
  },
});

export const loginActions = loginSlice.actions;

export default loginSlice;
