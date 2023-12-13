import React from "react";

export default function RadioButton({ buttonId, value1, value2, onChange }) {
  function handleRadioChange(event) {
    onChange(event.target.value);
  }

  return (
    <div id={buttonId} className="flex justify-center">
      <div className="flex items-center me-4">
        <input
          id={`${buttonId}-inline-radio`}
          type="radio"
          value={value1}
          name={`${buttonId}-radio-group`}
          onChange={(event) => handleRadioChange(event)}
          className="w-4 h-4 focus:bg-helenite-light-blue"
        />
        <label
          htmlFor={`${buttonId}-inline-radio`}
          className="ms-2 text-md text-helenite-white"
        >
          Yes
        </label>
      </div>
      <div className="flex items-center me-4">
        <input
          id={`${buttonId}-2-radio`}
          type="radio"
          value={value2}
          name={`${buttonId}-radio-group`}
          onChange={(event) => handleRadioChange(event)}
          className="w-4 h-4 focus:bg-helenite-light-blue"
        />
        <label
          htmlFor={`${buttonId}-2-radio`}
          className="ms-2 text-md text-helenite-white"
        >
          No
        </label>
      </div>
    </div>
  );
}
