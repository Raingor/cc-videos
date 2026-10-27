import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { EntranceBackground } from "./Backgrounds";
import { Bear } from "./Bear";
import { CoffeeBag, CoffeeCup } from "./Assets";
import { fade, slideX, slideY, bob } from "./animations";

export const Scene1: React.FC = () => {
  const frame = useCurrentFrame();

  // 0-90: sitting & patting belly
  // 90-180: phone vibrates, opens eyes, checks phone
  // 180-300: reluctant, sighs, stands, prepares coffee
  // 300-450: puts on helmet, grabs bag, walks to scooter

  const patFrame = frame % 60;
  const patY = bob(patFrame, 30, 6);

  const bearX = slideX(frame, 360, 450, [960, 1400]);
  const bearY = slideY(frame, 180, 240, [760, 650]);
  const bearScale = slideX(frame, 180, 240, [1.4, 1.55]);

  const phoneOpacity = fade(frame, 85, 100);
  const phoneShake = frame >= 90 && frame < 120 ? Math.sin(frame * 1.2) * 3 : 0;

  const bagOpacity = fade(frame, 220, 240);
  const cupOpacity = fade(frame, 250, 270) - fade(frame, 290, 305);
  const cupY = slideY(frame, 250, 300, [620, 720]);
  const bagScale = slideX(frame, 280, 310, [0.8, 1]);

  const helmetOpacity = fade(frame, 320, 340);

  return (
    <AbsoluteFill>
      <EntranceBackground />

      {/* Food containers */}
      <div
        style={{
          position: "absolute",
          left: 700,
          top: 790,
          opacity: fade(frame, 0, 20),
        }}
      >
        <svg width="140" height="80" viewBox="0 0 140 80">
          <rect x="0" y="20" width="70" height="50" rx="4" fill="#EF5350" stroke="#B71C1C" strokeWidth="2" />
          <rect x="10" y="0" width="50" height="25" rx="3" fill="#EF5350" stroke="#B71C1C" strokeWidth="2" />
          <rect x="75" y="30" width="55" height="45" rx="4" fill="#FF7043" stroke="#BF360C" strokeWidth="2" />
        </svg>
      </div>

      {/* Bear group */}
      <div
        style={{
          position: "absolute",
          left: bearX,
          top: bearY,
          transform: "translate(-50%, -50%)",
          opacity: fade(frame, 0, 30),
        }}
      >
        <svg width="600" height="600" viewBox="-300 -300 600 600">
          <g transform={`translate(0, ${frame < 180 ? patY : 0}) scale(${bearScale})`}>
            <Bear
              pose={frame < 180 ? "sitting" : frame < 240 ? "standing-front" : "standing-side-right"}
              expression={
                frame < 90
                  ? "sleepy"
                  : frame < 180
                  ? "tired"
                  : frame < 280
                  ? "sad"
                  : "neutral"
              }
              helmet={frame >= 340}
              holdingPhone={frame >= 100 && frame < 220}
              holdingBag={frame >= 370}
              pattingBelly={frame < 90}
            />
          </g>
        </svg>
      </div>

      {/* Phone vibration */}
      {frame >= 80 && frame < 180 && (
        <div
          style={{
            position: "absolute",
            left: 1010,
            top: 670,
            transform: `translate(-50%, -50%) rotate(${phoneShake}deg)`,
            opacity: phoneOpacity,
          }}
        >
          <svg width="60" height="80" viewBox="0 0 60 80">
            <rect x="0" y="0" width="60" height="80" rx="6" fill="#37474F" />
            <rect x="5" y="8" width="50" height="55" rx="2" fill="#E0F7FA" />
            <circle cx="30" cy="70" r="4" fill="#B0BEC5" />
          </svg>
        </div>
      )}

      {/* Coffee cup being placed into bag */}
      {frame >= 240 && frame < 310 && (
        <>
          <div
            style={{
              position: "absolute",
              left: 1120,
              top: 720,
              opacity: bagOpacity,
              transform: `translate(-50%, -50%) scale(${bagScale})`,
            }}
          >
            <CoffeeBag width={130} />
          </div>
          <div
            style={{
              position: "absolute",
              left: 1120,
              top: cupY,
              opacity: cupOpacity,
              transform: "translate(-50%, -50%)",
            }}
          >
            <CoffeeCup width={70} />
          </div>
        </>
      )}

      {/* Coffee bag held by bear after packing */}
      {frame >= 310 && (
        <div
          style={{
            position: "absolute",
            left: 1080,
            top: 700,
            transform: "translate(-50%, -50%)",
            opacity: fade(frame, 310, 330),
          }}
        >
          <CoffeeBag width={120} />
        </div>
      )}

      {/* Notification bubble */}
      {frame >= 95 && frame < 160 && (
        <div
          style={{
            position: "absolute",
            left: 1080,
            top: 520,
            opacity: fade(frame, 95, 110) - fade(frame, 140, 160),
            transform: "translate(-50%, -50%)",
          }}
        >
          <svg width="140" height="80" viewBox="0 0 140 80">
            <rect x="0" y="0" width="140" height="70" rx="12" fill="white" stroke="#CFD8DC" strokeWidth="2" />
            <polygon points="30,70 40,80 50,70" fill="white" stroke="#CFD8DC" strokeWidth="2" />
            <rect x="10" y="10" width="30" height="30" rx="4" fill="#42A5F5" />
            <rect x="50" y="15" width="70" height="8" rx="2" fill="#37474F" />
            <rect x="50" y="32" width="50" height="6" rx="2" fill="#90A4AE" />
          </svg>
        </div>
      )}
    </AbsoluteFill>
  );
};
