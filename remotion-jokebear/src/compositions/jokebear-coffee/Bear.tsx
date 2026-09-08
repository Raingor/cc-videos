import React from "react";
import { COLORS, BearPose, BearExpression } from "./constants";

interface BearProps {
  pose: BearPose;
  expression: BearExpression;
  helmet?: boolean;
  scale?: number;
  pattingBelly?: boolean;
  holdingPhone?: boolean;
  holdingBag?: boolean;
}

// Tiny bear logo used on vest, helmet and scooter sticker
const BearLogo: React.FC<{ x: number; y: number; size?: number }> = ({
  x,
  y,
  size = 1,
}) => (
  <g transform={`translate(${x}, ${y}) scale(${size})`}>
    <circle cx="0" cy="0" r="10" fill={COLORS.bear} stroke={COLORS.black} strokeWidth="1" />
    <circle cx="-3" cy="-2" r="1.5" fill={COLORS.black} />
    <circle cx="3" cy="-2" r="1.5" fill={COLORS.black} />
    <ellipse cx="0" cy="2" rx="2.5" ry="2" fill={COLORS.black} />
  </g>
);

const Face: React.FC<{ expression: BearExpression }> = ({ expression }) => {
  const renderEyes = () => {
    switch (expression) {
      case "sleepy":
        return (
          <>
            <line x1="-25" y1="-8" x2="-10" y2="-8" stroke={COLORS.black} strokeWidth="3" strokeLinecap="round" />
            <line x1="10" y1="-8" x2="25" y2="-8" stroke={COLORS.black} strokeWidth="3" strokeLinecap="round" />
          </>
        );
      case "tired":
      case "sad":
        return (
          <>
            <circle cx="-18" cy="-5" r="3.5" fill={COLORS.black} />
            <circle cx="18" cy="-5" r="3.5" fill={COLORS.black} />
            <path d="M -30 -15 Q -18 -20 -6 -15" stroke={COLORS.black} strokeWidth="2" fill="none" strokeLinecap="round" />
            <path d="M 6 -15 Q 18 -20 30 -15" stroke={COLORS.black} strokeWidth="2" fill="none" strokeLinecap="round" />
          </>
        );
      case "slight-smile":
        return (
          <>
            <circle cx="-18" cy="-5" r="4" fill={COLORS.black} />
            <circle cx="18" cy="-5" r="4" fill={COLORS.black} />
          </>
        );
      case "neutral":
      default:
        return (
          <>
            <circle cx="-18" cy="-5" r="4" fill={COLORS.black} />
            <circle cx="18" cy="-5" r="4" fill={COLORS.black} />
          </>
        );
    }
  };

  const renderMouth = () => {
    // Flat nose + small mouth, no protruding muzzle
    switch (expression) {
      case "sleepy":
      case "tired":
      case "sad":
        return (
          <>
            <ellipse cx="0" cy="8" rx="5" ry="4" fill={COLORS.black} />
            <path d="M -6 16 Q 0 12 6 16" stroke={COLORS.black} strokeWidth="2.5" fill="none" strokeLinecap="round" />
          </>
        );
      case "slight-smile":
        return (
          <>
            <ellipse cx="0" cy="8" rx="5" ry="4" fill={COLORS.black} />
            <path d="M -7 16 Q 0 21 7 16" stroke={COLORS.black} strokeWidth="2.5" fill="none" strokeLinecap="round" />
          </>
        );
      case "neutral":
      default:
        return (
          <>
            <ellipse cx="0" cy="8" rx="5" ry="4" fill={COLORS.black} />
            <path d="M -5 17 Q 0 15 5 17" stroke={COLORS.black} strokeWidth="2.5" fill="none" strokeLinecap="round" />
          </>
        );
    }
  };

  return (
    <g>
      {/* Head */}
      <ellipse cx="0" cy="0" rx="70" ry="62" fill={COLORS.bear} />
      {/* Ears */}
      <circle cx="-52" cy="-42" r="18" fill={COLORS.bear} />
      <circle cx="52" cy="-42" r="18" fill={COLORS.bear} />
      {renderEyes()}
      {renderMouth()}
      {/* tiny blush for cuteness */}
      <ellipse cx="-45" cy="10" rx="7" ry="4" fill={COLORS.sun} opacity="0.35" />
      <ellipse cx="45" cy="10" rx="7" ry="4" fill={COLORS.sun} opacity="0.35" />
    </g>
  );
};

const Helmet: React.FC = () => (
  <g transform="translate(0, -58)">
    <path
      d="M -62 10 Q -62 -55 0 -55 Q 62 -55 62 10 Z"
      fill={COLORS.yellow}
      stroke={COLORS.yellowDark}
      strokeWidth="2"
    />
    <rect x="-66" y="8" width="132" height="10" rx="5" fill={COLORS.yellowDark} />
    <BearLogo x={28} y={-25} size={0.9} />
  </g>
);

const Vest: React.FC = () => (
  <g>
    <path
      d="M -38 -20 L 38 -20 L 42 55 L -42 55 Z"
      fill={COLORS.yellow}
      stroke={COLORS.yellowDark}
      strokeWidth="2"
    />
    <rect x="-35" y="-5" width="70" height="8" rx="2" fill={COLORS.vestReflective} opacity="0.9" />
    <rect x="-32" y="30" width="64" height="8" rx="2" fill={COLORS.vestReflective} opacity="0.9" />
    <BearLogo x={0} y={12} size={1.1} />
  </g>
);

export const Bear: React.FC<BearProps> = ({
  pose,
  expression,
  helmet = false,
  scale = 1,
  pattingBelly = false,
  holdingPhone = false,
  holdingBag = false,
}) => {
  const renderBody = () => {
    switch (pose) {
      case "sitting":
        return (
          <g>
            {/* Body sitting */}
            <ellipse cx="0" cy="55" rx="58" ry="65" fill={COLORS.bear} />
            <Vest />
            {/* Legs tucked */}
            <ellipse cx="-35" cy="105" rx="22" ry="18" fill={COLORS.bear} />
            <ellipse cx="35" cy="105" rx="22" ry="18" fill={COLORS.bear} />
            {/* Arms */}
            {pattingBelly ? (
              <>
                <ellipse cx="-38" cy="45" rx="16" ry="28" fill={COLORS.bear} transform="rotate(20 -38 45)" />
                <ellipse cx="32" cy="48" rx="16" ry="24" fill={COLORS.bear} transform="rotate(-30 32 48)" />
              </>
            ) : (
              <>
                <ellipse cx="-42" cy="40" rx="16" ry="28" fill={COLORS.bear} transform="rotate(15 -42 40)" />
                <ellipse cx="42" cy="40" rx="16" ry="28" fill={COLORS.bear} transform="rotate(-15 42 40)" />
              </>
            )}
          </g>
        );

      case "standing-front":
        return (
          <g>
            <ellipse cx="0" cy="55" rx="52" ry="62" fill={COLORS.bear} />
            <Vest />
            <ellipse cx="-30" cy="120" rx="18" ry="28" fill={COLORS.bear} />
            <ellipse cx="30" cy="120" rx="18" ry="28" fill={COLORS.bear} />
            {holdingPhone ? (
              <>
                <ellipse cx="-40" cy="35" rx="16" ry="28" fill={COLORS.bear} transform="rotate(10 -40 35)" />
                <ellipse cx="35" cy="30" rx="16" ry="26" fill={COLORS.bear} transform="rotate(-25 35 30)" />
                {/* Phone */}
                <rect x="20" y="5" width="26" height="38" rx="3" fill={COLORS.scooterDark} />
                <rect x="23" y="8" width="20" height="28" rx="1" fill={COLORS.skyBottom} />
              </>
            ) : holdingBag ? (
              <>
                <ellipse cx="-45" cy="40" rx="16" ry="28" fill={COLORS.bear} transform="rotate(20 -45 40)" />
                <ellipse cx="45" cy="40" rx="16" ry="28" fill={COLORS.bear} transform="rotate(-20 45 40)" />
              </>
            ) : (
              <>
                <ellipse cx="-45" cy="35" rx="16" ry="28" fill={COLORS.bear} transform="rotate(10 -45 35)" />
                <ellipse cx="45" cy="35" rx="16" ry="28" fill={COLORS.bear} transform="rotate(-10 45 35)" />
              </>
            )}
          </g>
        );

      case "standing-side-left":
      case "standing-side-right":
        // standing-side-right faces right, standing-side-left faces left
        const dir = pose === "standing-side-right" ? -1 : 1;
        return (
          <g transform={`scale(${dir}, 1)`}>
            <ellipse cx="0" cy="55" rx="45" ry="60" fill={COLORS.bear} />
            <Vest />
            <ellipse cx="-18" cy="118" rx="16" ry="26" fill={COLORS.bear} />
            <ellipse cx="18" cy="118" rx="16" ry="26" fill={COLORS.bear} />
            <ellipse cx="-28" cy="38" rx="14" ry="24" fill={COLORS.bear} transform="rotate(15 -28 38)" />
            <ellipse cx="28" cy={holdingBag ? "32" : "38"} rx="14" ry="24" fill={COLORS.bear} transform={holdingBag ? "rotate(-35 28 32)" : "rotate(-15 28 38)"} />
          </g>
        );

      case "standing-back":
        return (
          <g>
            <ellipse cx="0" cy="55" rx="52" ry="60" fill={COLORS.bear} />
            {/* vest back */}
            <path d="M -36 -18 L 36 -18 L 40 52 L -40 52 Z" fill={COLORS.yellow} stroke={COLORS.yellowDark} strokeWidth="2" />
            <ellipse cx="-42" cy="35" rx="16" ry="28" fill={COLORS.bear} transform="rotate(10 -42 35)" />
            <ellipse cx="42" cy="35" rx="16" ry="28" fill={COLORS.bear} transform="rotate(-10 42 35)" />
            <ellipse cx="-28" cy="118" rx="18" ry="28" fill={COLORS.bear} />
            <ellipse cx="28" cy="118" rx="18" ry="28" fill={COLORS.bear} />
          </g>
        );

      case "riding-side":
        return (
          <g transform="scale(-1, 1)">
            <ellipse cx="0" cy="55" rx="45" ry="55" fill={COLORS.bear} />
            <Vest />
            <ellipse cx="-20" cy="110" rx="16" ry="24" fill={COLORS.bear} transform="rotate(45 -20 110)" />
            <ellipse cx="25" cy="100" rx="16" ry="22" fill={COLORS.bear} transform="rotate(-20 25 100)" />
            {/* Arms reaching handlebar */}
            <ellipse cx="-25" cy="38" rx="14" ry="24" fill={COLORS.bear} transform="rotate(35 -25 38)" />
            <ellipse cx="22" cy="32" rx="14" ry="22" fill={COLORS.bear} transform="rotate(-45 22 32)" />
          </g>
        );

      default:
        return null;
    }
  };

  return (
    <g transform={`scale(${scale})`}>
      {renderBody()}
      <Face expression={expression} />
      {helmet && <Helmet />}
    </g>
  );
};
