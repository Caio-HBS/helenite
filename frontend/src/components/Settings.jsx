import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useLoaderData, useNavigate } from "react-router-dom";

import { loginActions } from "../store/login-slice.js";
import { userInfoActions } from "../store/user-info-slice.js";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import RadioButton from "./RadioButton.jsx";

export default function SettingsComponent() {
  const response = useLoaderData();

  const navigate = useNavigate();

  const dispatch = useDispatch();

  const [showPassword, setShowPassowrd] = useState(false);
  const [profilePicture, setprofilePicture] = useState(null);
  const [privateProfile, setPrivateProfile] = useState(null);
  const [showBirthday, setShowBirthday] = useState(null);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  function showPasswordHandler() {
    setShowPassowrd((oldState) => !oldState);
  }

  function handleAddImage(event) {
    const selectedFile = event[0];

    const allowedExtensions = ["jpg", "jpeg", "png"];
    const fileExtension = selectedFile.name.split(".").pop().toLowerCase();

    if (allowedExtensions.includes(fileExtension)) {
      setprofilePicture(selectedFile);
    } else {
      setprofilePicture(null);
    }
  }

  async function handleChangeSettings(event) {
    event.preventDefault();

    const token = localStorage.getItem("token");
    const currentUser = localStorage.getItem("profile-slug");

    const formData = new FormData();

    // Toggle private profile preference.
    const privProfile = privateProfile;
    if (privProfile !== null) {
      formData.append("private_profile", privProfile.toString());
    }

    // Toggle show birthday preference.
    const showBirth = showBirthday;
    if (showBirth !== null) {
      formData.append("show_birthday", showBirth.toString());
    }

    // Change password.
    const oldPass = oldPassword;
    const newPass = newPassword;
    const confirmPass = confirmPassword;
    if (oldPass !== "" && newPass !== "" && confirmPass !== "") {
      if (newPass !== oldPass && confirmPass !== oldPass) {
        if (newPass === confirmPass) {
          formData.append("old_password", oldPass);
          formData.append("new_password", newPass);
          formData.append("confirm_new_password", confirmPass);
        }
      }
    }

    // Change pfp.
    const newPfp = profilePicture;
    if (newPfp !== null) {
      formData.append("pfp", newPfp);
    }

    const response = await fetch(
      `${backendURL}/api/v1/profile/${currentUser}/change-settings/`,
      {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      }
    );

    if (!response.ok) {
      // TODO: fix bad request on settings.
    }

    const resData = await response.json();
    console.log(resData);

    dispatch(loginActions.logout());
    dispatch(userInfoActions.logout());

    navigate("/");
  }

  return (
    <>
      <div
        id="main-container"
        className="flex flex-col justify-center mx-40 m-5 rounded-lg bg-helenite-dark-grey"
      >
        <h2 className="text-center text-4xl pt-2 text-helenite-white">
          <strong>Change Settings</strong>
        </h2>
        <div id="settings container" className="p-4">
          <form onSubmit={(event) => handleChangeSettings(event)}>
            <div className="bg-helenite-light-grey m-1 rounded-lg p-4">
              <div>
                <p className="pr-2 text-2xl text-helenite-white">
                  <strong>Change profile picture:</strong>
                </p>
              </div>
              <div className="flex items-center justify-center">
                <p className="pr-4 text-helenite-white">
                  <strong>Current Picture:</strong>
                </p>
                <img
                  src={response.pfp}
                  className="rounded-full w-20 h-20 object-cover"
                />
                <input
                  type="file"
                  className="pl-10 text-helenite-white"
                  onChange={(event) => handleAddImage(event.target.files)}
                />
              </div>
            </div>
            <div className="bg-helenite-light-grey m-1 rounded-lg p-4">
              <div className="bg-helenite-light-grey">
                <p className="pr-2 text-2xl text-helenite-white">
                  <strong>Make profile private:</strong>
                </p>
              </div>
              <RadioButton
                buttonId="private-profile"
                value1={true}
                value2={false}
                onChange={(value) => setPrivateProfile(value)}
              />
            </div>
            <div className="bg-helenite-light-grey m-1 rounded-lg p-4">
              <div>
                <p className="pr-2 text-2xl text-helenite-white">
                  <strong>Show my Birthday:</strong>
                </p>
              </div>
              <RadioButton
                buttonId="show-birthday"
                value1={true}
                value2={false}
                onChange={(value) => setShowBirthday(value)}
              />
            </div>
            <div className="bg-helenite-light-grey m-1 rounded-lg p-4">
              <div>
                <p className="pr-2 text-2xl text-helenite-white">
                  <strong>Change password:</strong>
                </p>
              </div>
              <div className="flex items-center justify-center">
                <div className="px-4">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="old_password"
                    placeholder="Your OLD password"
                    value={oldPassword}
                    onChange={(event) => setOldPassword(event.target.value)}
                    className="bg-helenite-white text-helenite-dark-grey focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
                  />
                </div>
                <div className="px-4">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="new_password"
                    placeholder="Your NEW password"
                    value={newPassword}
                    onChange={(event) => setNewPassword(event.target.value)}
                    className="bg-helenite-white text-helenite-dark-grey focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
                  />
                </div>
                <div className="px-4">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="confirm_new_password"
                    placeholder="Confirm your NEW password"
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                    className="bg-helenite-white text-helenite-dark-grey focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
                  />
                </div>
              </div>
              <div className="flex items-center justify-center pt-2">
                <button
                  type="button"
                  onClick={showPasswordHandler}
                  className="text-helenite-light-blue hover:text-helenite-green hover:underline"
                >
                  Toggle passwords view
                </button>
              </div>
            </div>
            <div className="text-right">
              <button className="rounded-lg p-2 bg-helenite-light-blue hover:bg-helenite-dark-blue hover:text-helenite-white">
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
