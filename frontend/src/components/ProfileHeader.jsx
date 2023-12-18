import React from "react";
import { useSelector } from "react-redux";
import { useLoaderData } from "react-router-dom";
import { format, parseISO } from "date-fns";
import { ToastContainer, toast } from "react-toastify";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

import BirthplaceWithFlag from "./BirthplaceWithFlag.jsx";

export default function ProfileHeader() {
  const response = useLoaderData();
  console.log(response);

  const currentUser = useSelector((state) => state.userInfo.username);
  const friendRequests = JSON.parse(localStorage.getItem("friend-requests"));
  const token = localStorage.getItem("token");

  async function handleAddFriend(event) {
    event.preventDefault();
    const responseAddFriend = await fetch(
      `${backendURL}/api/v1/profile/${response.endpoint.slice(16, -1)}/`,
      {
        method: friendRequests.includes(response.username) ? "PUT" : "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (responseAddFriend.status === 400) {
      const resError = await responseAddFriend.json();
      toast.error(resError.message, {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "colored",
      });
      return;
    }

    const resData = await responseAddFriend.json();
    toast.success(resData.message, {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
    });
  }

  const parsedBirthday = parseISO(response.birthday);
  const formattedBirthday = format(parsedBirthday, "MM/dd/yyyy");

  const currentDate = new Date();
  const formattedCurrentDate = format(currentDate, "MM/dd/yyyy");

  return (
    <div className="flex flex-col items-center justify-center mx-40 m-5 rounded-lg bg-helenite-dark-grey">
      <ToastContainer />
      <img
        src={response.pfp}
        className="w-60 h-60 pt-2 rounded-full object-cover"
      />
      <div>
        <h2 className="text-4xl pt-2 text-helenite-light-blue">
          <strong>{response.get_full_name}</strong>
        </h2>
        <p className="text-center text-xl text-helenite-white">
          <strong>@{response.username}</strong>
        </p>
        <p className="pt-3 text-center text-md text-helenite-white">
          {formattedBirthday === formattedCurrentDate
            ? `Born in: ${formattedBirthday} 🎂`
            : `Born in: ${formattedBirthday}`}
        </p>
        <BirthplaceWithFlag birth_place={response.birth_place} />
      </div>
      {currentUser !== response.username && (
        <form className="m-2" onSubmit={(event) => handleAddFriend(event)}>
          <button className="p-2 rounded-lg bg-helenite-light-blue hover:bg-helenite-dark-blue hover:text-helenite-white">
            Add friend
          </button>
        </form>
      )}
    </div>
  );
}
