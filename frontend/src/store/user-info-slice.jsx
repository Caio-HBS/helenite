import { createSlice } from "@reduxjs/toolkit";

const userInfoSlice = createSlice({
  name: "userInfo",
  initialState: {
    fullname: "",
    username: "",
    pfp: "",
  },
  reducers: {
    setUserInfo(state) {
      state.fullname = localStorage.getItem("user-fullname") || "";
      state.username = localStorage.getItem("user-username") || "";
      state.pfp = localStorage.getItem("user-pfp") || "";
    },
    logout(state) {
      state.fullname = "";
      state.username = "";
      state.pfp = "";
    },
  },
});

export const userInfoActions = userInfoSlice.actions;

export default userInfoSlice;
