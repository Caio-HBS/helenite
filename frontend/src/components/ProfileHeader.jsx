import React from "react";
import { useLoaderData } from "react-router-dom";
import { format, parseISO } from "date-fns";

import BirthplaceWithFlag from "./BirthplaceWithFlag.jsx";

export default function ProfileHeader() {
  const response = useLoaderData();

  const parsedBirthday = parseISO(response.birthday);
  const formattedBirthday = format(parsedBirthday, "MM/dd/yyyy");

  const currentDate = new Date();
  const formattedCurrentDate = format(currentDate, "MM/dd/yyyy");

  return (
    <div className="flex flex-col items-center justify-center mx-40 m-5 rounded-lg bg-helenite-dark-grey">
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
    </div>
  );
}
