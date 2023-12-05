import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const backendURL = import.meta.env.VITE_REACT_BACKEND_URL;

export default function NewPost() {
  const addImageValid =
    "pr-2 hover:underline hover:cursor-pointer text-helenite-white hover:text-helenite-green";
  const addImageInvalid = "pr-2 hover:cursor-not-allowed text-red-600";

  const navigate = useNavigate();

  const [imageContent, setImageContent] = useState(null);
  const [textAreaContent, setTextAreaContent] = useState("");
  const [fileButtonValue, setFileButtonValue] = useState("Add image");
  const [addImageButtonClass, setAddImageButtonClass] = useState(addImageValid);

  async function handleSubmitNewPost(event) {
    event.preventDefault();

    const token = localStorage.getItem("token");

    const postText = textAreaContent;
    const postImage = imageContent;

    const formData = new FormData();

    if (postText !== "" || postImage !== null) {
      if (postText !== "") {
        formData.append("post_text", postText);
      }

      if (postImage !== null) {
        formData.append("post_image", postImage);
      }

      const response = await fetch(`${backendURL}/api/v1/feed/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        return response; // TODO: this.
      }

      navigate(0);
    }
  }

  function handleAddImage(event) {
    const selectedFile = event[0];

    setFileButtonValue(selectedFile.name);

    const allowedExtensions = ["jpg", "jpeg", "png"];
    const fileExtension = selectedFile.name.split(".").pop().toLowerCase();

    if (allowedExtensions.includes(fileExtension)) {
      setAddImageButtonClass(addImageValid);
      setImageContent(selectedFile);
    } else {
      setImageContent(null);
      setFileButtonValue("INVALID FILE TYPE");
      setAddImageButtonClass(addImageInvalid);
    }
  }

  return (
    <form id="new-post" className="p-2" onSubmit={handleSubmitNewPost}>
      <textarea
        placeholder="What's on my mind?"
        name="post_text"
        onChange={(event) => setTextAreaContent(event.target.value)}
        className="flex w-full h-28 resize-none rounded-lg bg-helenite-light-grey text-helenite-white focus:outline-none focus:border-0 focus:outline-helenite-light-blue"
      />
      <div className="text-right pt-3">
        <input
          type="file"
          id="input_image"
          name="post_image"
          accept="image"
          className="hidden"
          onChange={(event) => handleAddImage(event.target.files)}
        />
        <label htmlFor="input_image" className={addImageButtonClass}>
          {fileButtonValue}
        </label>
        <button className="rounded-sm p-1 bg-helenite-light-blue text-stone-800 hover:text-helenite-white hover:bg-helenite-dark-blue">
          New Post
        </button>
      </div>
    </form>
  );
}
