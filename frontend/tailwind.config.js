/** @type {import('tailwindcss').Config} */

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "helenite-light-blue": "#05c8ba",
        "helenite-dark-blue": "#395e66",
        "helenite-dark-grey": "#313131",
        "helenite-light-grey": "#3b3b3b",
        "helenite-green": "#c3d350",
        "helenite-white": "#ece8ef",
      },
    },
  },
  plugins: [],
};
