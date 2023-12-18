import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

export default function NewComment({ navigate, currentUser, token, endpoint }) {
  const [commentText, setCommentText] = useState("");

  async function handleSubmitComment(event) {
    event.preventDefault();

    if (commentText !== "") {
      const formData = new FormData();
      formData.append("comment_text", commentText);
      formData.append("comment_user", currentUser);

      const response = await fetch(`${backendURL}${endpoint}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        toast.error("Error while trying to submit comment, please try again.", {
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

      navigate(0);
    }
  }

  return (
    <form className="pt-3" onSubmit={(event) => handleSubmitComment(event)}>
      <textarea
        placeholder="Want to be part of this discussion?"
        name="comment_text"
        className="flex w-full h-28 resize-none rounded-lg bg-helenite-light-grey text-helenite-white focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
        maxLength={500}
        required
        onChange={(e) => setCommentText(e.target.value)}
      />
      <div className="text-right pt-2">
        <button className="rounded-md p-1 bg-helenite-light-blue hover:bg-helenite-dark-blue hover:text-helenite-white">
          Post Comment
        </button>
      </div>
    </form>
  );
}
