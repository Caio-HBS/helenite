import { createSlice } from "@reduxjs/toolkit";

const userInfoSlice = createSlice({
  name: "userInfo",
  initialState: {
    fullname: "",
    username: "",
    pfp: "",
    userPK: "",
  },
  reducers: {
    setUserInfo(state) {
      state.fullname = localStorage.getItem("user-fullname") || "";
      state.username = localStorage.getItem("user-username") || "";
      state.pfp = localStorage.getItem("user-pfp") || "";
      state.userPK = localStorage.getItem("user-pk") || "";
    },
    logout(state) {
      state.fullname = "";
      localStorage.removeItem("user-fullname");
      state.username = "";
      localStorage.removeItem("user-username");
      state.pfp = "";
      localStorage.removeItem("user-pfp");
      state.userPK = "";
      localStorage.removeItem("user-pk");
    },
  },
});

export const userInfoActions = userInfoSlice.actions;

export default userInfoSlice;
