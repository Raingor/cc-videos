import React from "react";
import { staticFile } from "remotion";
import { COLORS } from "./constants";

interface ScooterProps {
  scale?: number;
  hasBag?: boolean;
}

const BearSticker: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g transform={`translate(${x}, ${y})`}>
    <circle cx="0" cy="0" r="8" fill={COLORS.bear} stroke={COLORS.black} strokeWidth="1" />
    <circle cx="-2.5" cy="-2" r="1.2" fill={COLORS.black} />
    <circle cx="2.5" cy="-2" r="1.2" fill={COLORS.black} />
    <ellipse cx="0" cy="2" rx="2" ry="1.6" fill={COLORS.black} />
  </g>
);

export const Scooter: React.FC<ScooterProps> = ({ scale = 1, hasBag = false }) => {
  return (
    <g transform={`scale(${scale})`}>
      {/* Rear wheel */}
      <circle cx="-90" cy="55" r="32" fill={COLORS.scooterDark} />
      <circle cx="-90" cy="55" r="18" fill={COLORS.scooterBody} />
      {/* Front wheel */}
      <circle cx="90" cy="55" r="32" fill={COLORS.scooterDark} />
      <circle cx="90" cy="55" r="18" fill={COLORS.scooterBody} />
      {/* Body frame */}
      <path
        d="M -90 55 L -40 20 L 40 20 L 90 55"
        stroke={COLORS.scooterDark}
        strokeWidth="10"
        fill="none"
        strokeLinecap="round"
      />
      <path d="M -40 20 L -50 -15 L 30 -15" stroke={COLORS.scooterDark} strokeWidth="10" fill="none" strokeLinecap="round" />
      {/* Foot deck */}
      <rect x="-55" y="15" width="90" height="14" rx="4" fill={COLORS.scooterBody} stroke={COLORS.scooterDark} strokeWidth="2" />
      {/* Seat */}
      <path d="M -60 -15 L -20 -15 Q -10 -15 -10 -25 L -10 -30 Q -10 -38 -20 -38 L -55 -38 Q -65 -38 -65 -28 L -65 -22 Q -65 -15 -60 -15" fill={COLORS.scooterSeat} />
      {/* Front column & handlebar */}
      <rect x="82" y="-35" width="10" height="85" rx="3" fill={COLORS.scooterDark} />
      <path d="M 72 -35 L 110 -35" stroke={COLORS.scooterDark} strokeWidth="8" strokeLinecap="round" />
      <circle cx="75" cy="-35" r="5" fill={COLORS.black} />
      <circle cx="108" cy="-35" r="5" fill={COLORS.black} />
      {/* Headlight */}
      <circle cx="92" cy="-8" r="8" fill={COLORS.yellow} stroke={COLORS.yellowDark} strokeWidth="2" />
      {/* Bear sticker */}
      <BearSticker x={0} y={-5} />
      {/* Coffee delivery bag on foot deck — uses provided reference image */}
      {hasBag && (
        <g transform="translate(-10, -18)">
          <image
            href={staticFile("assets/coffee-bag.jpg")}
            x="-28"
            y="-55"
            width="56"
            height="70"
            preserveAspectRatio="xMidYMid meet"
          />
        </g>
      )}
    </g>
  );
};
