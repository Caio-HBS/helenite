import React from "react";
import { countryCodeEmoji } from "country-code-emoji";
import { getCode } from "country-list";

export default function BirthplaceWithFlag({ birth_place }) {
  const countryCode = getCode(birth_place) || null;

  if (countryCode !== null) {
    const countryEmoji = [countryCode].map(countryCodeEmoji);

    return (
      <p className="text-center pb-2 text-helenite-white">
        From: {birth_place + " " + countryEmoji}
      </p>
    );
  }

  return <p>{birth_place}</p>;
}
