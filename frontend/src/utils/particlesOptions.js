export default {
  name: "Link Triangles",
  particles: {
    number: {
      value: 80,
      density: {
        enable: true,
      },
    },
    color: {
      value: "#0fc8ba",
      
    },
    shape: {
      type: "circle",
    },
    opacity: {
      value: 0.5,
    },
    size: {
      value: {
        min: 1,
        max: 3,
      },
    },
    links: {
      enable: true,
      distance: 150,
      color: "#0fc8ba",
      opacity: 0.4,
      width: 1,
      triangles: {
        enable: true,
        color: "#3b3b3b",
        opacity: 0.1,
      },
    },
    move: {
      enable: true,
      speed: 2,
    },
  },
  fullScreen: false,
  background: {
    color: "#000000",
  },
};
