import React from "react";
import { formatDistanceToNow, format } from "date-fns";

export default function TransformDate({ date }) {
  const originalDate = new Date(date);
  const today = new Date();

  if (
    originalDate.getDate() === today.getDate() &&
    originalDate.getMonth() === today.getMonth() &&
    originalDate.getFullYear() === today.getFullYear()
  ) {
    const difference = formatDistanceToNow(originalDate, { addSuffix: true });
    return <p className="text-xs">{difference}</p>;
  }

  const resultDate = format(originalDate, "MMM. dd, HH:mm");
  return <p className="text-xs">{resultDate}</p>;
}
