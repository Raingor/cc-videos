import { interpolate, spring, SpringConfig } from "remotion";

export const fade = (
  frame: number,
  start: number,
  end: number,
  values: [number, number] = [0, 1]
) =>
  interpolate(frame, [start, end], values, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const slideX = (
  frame: number,
  start: number,
  end: number,
  values: [number, number]
) =>
  interpolate(frame, [start, end], values, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const slideY = (
  frame: number,
  start: number,
  end: number,
  values: [number, number]
) =>
  interpolate(frame, [start, end], values, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const scale = (
  frame: number,
  start: number,
  end: number,
  values: [number, number]
) =>
  interpolate(frame, [start, end], values, {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const springScale = (
  frame: number,
  fps: number,
  config?: SpringConfig
) =>
  spring({
    frame,
    fps,
    config: config ?? { damping: 100, stiffness: 200, mass: 1 },
  });

// Bobbing motion for riding/walking
export const bob = (frame: number, speed: number, amplitude: number) =>
  Math.sin((frame / speed) * Math.PI * 2) * amplitude;
