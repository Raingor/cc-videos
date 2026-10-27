// ===== EDITABLE CONSTANTS =====
export const VIDEO = {
  width: 1920,
  height: 1080,
  fps: 30,
  durationInFrames: 900, // 30 seconds
};

export const COLORS = {
  bear: "#FFFFFF",
  bearShadow: "#E8E4DF",
  yellow: "#FFD54F",
  yellowDark: "#FBC02D",
  vestReflective: "#FFF59D",
  black: "#1A1A1A",
  eye: "#1A1A1A",
  scooterBody: "#ECEFF1",
  scooterDark: "#455A64",
  scooterSeat: "#263238",
  building: "#F5F0E8",
  buildingShadow: "#E3DED4",
  step: "#D7CCC8",
  stepEdge: "#A1887F",
  skyTop: "#FFCC80",
  skyBottom: "#FFF3E0",
  sun: "#FFAB91",
  road: "#78909C",
  sidewalk: "#D7CCC8",
  grass: "#C5E1A5",
  tree: "#AED581",
};

export const TIMING = {
  scene1Duration: 450, // 15s
  scene2Start: 450,
  scene2Duration: 450,
  transitionDuration: 20, // ~0.67s crossfade
};

export type BearPose =
  | "sitting"
  | "standing-front"
  | "standing-side-left"
  | "standing-side-right"
  | "standing-back"
  | "riding-side";

export type BearExpression = "sleepy" | "tired" | "sad" | "neutral" | "slight-smile";
