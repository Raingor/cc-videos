import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { StreetBackground, DeliveryHandBackground } from "./Backgrounds";
import { Bear } from "./Bear";
import { Scooter } from "./Scooter";
import { CoffeeBag } from "./Assets";
import { fade, slideX, slideY, bob } from "./animations";

export const Scene2: React.FC = () => {
  const frame = useCurrentFrame();

  // 0-60: place bag on scooter
  // 60-240: ride through street (parallax)
  // 240-360: arrive, park, walk to building
  // 360-420: hand over to customer
  // 420-450: walk back exhausted but relieved

  const rideBob = bob(frame, 12, 4);
  const scooterX = slideX(frame, 60, 240, [-300, 2220]);

  const walkBob = bob(frame, 20, 5);
  const bearWalkX = slideX(frame, 260, 360, [500, 980]);

  const customerHandOpacity = fade(frame, 360, 380);
  const handoverY = slideY(frame, 360, 390, [40, 0]);

  return (
    <AbsoluteFill>
      {frame < 240 ? <StreetBackground /> : <DeliveryHandBackground />}

      {/* Riding sequence */}
      {frame < 240 && (
        <div
          style={{
            position: "absolute",
            left: scooterX,
            top: 760 + rideBob,
            transform: "translate(-50%, -50%)",
          }}
        >
          <svg width="700" height="500" viewBox="-350 -250 700 500">
            <g transform="scale(1.6)">
              <Scooter hasBag={frame >= 30} scale={1} />
              <g transform="translate(-35, -95)">
                <Bear
                  pose="riding-side"
                  expression={frame < 120 ? "tired" : "neutral"}
                  helmet
                  scale={0.85}
                />
              </g>
            </g>
          </svg>
        </div>
      )}

      {/* Parallax street elements for motion feeling */}
      {frame >= 60 && frame < 240 && (
        <div
          style={{
            position: "absolute",
            left: 2000 - ((frame - 60) * 12) % 2200,
            top: 620,
            opacity: 0.8,
          }}
        >
          <svg width="120" height="120" viewBox="0 0 120 120">
            <rect x="45" y="60" width="14" height="60" fill="#8D6E63" />
            <circle cx="52" cy="40" r="45" fill="#AED581" />
          </svg>
        </div>
      )}

      {/* Arrival / walking to building */}
      {frame >= 240 && frame < 450 && (
        <>
          {/* Scooter parked */}
          <div
            style={{
              position: "absolute",
              left: 450,
              top: 820,
              transform: "translate(-50%, -50%) scale(1.4)",
              opacity: fade(frame, 240, 270),
            }}
          >
            <svg width="500" height="300" viewBox="-250 -150 500 300">
              <Scooter hasBag={frame < 340} scale={1} />
            </svg>
          </div>

          {/* Bear walking */}
          <div
            style={{
              position: "absolute",
              left: bearWalkX,
              top: 780 + walkBob,
              transform: "translate(-50%, -50%)",
              opacity: fade(frame, 250, 280),
            }}
          >
            <svg width="400" height="400" viewBox="-200 -200 400 400">
              <g transform="scale(1.3)">
                <Bear
                  pose={frame < 360 ? "standing-side-right" : "standing-front"}
                  expression={frame < 420 ? "tired" : "slight-smile"}
                  helmet
                  holdingBag={frame < 380}
                />
              </g>
            </svg>
          </div>

          {/* Coffee bag on scooter while handing over */}
          {frame >= 340 && frame < 380 && (
            <div
              style={{
                position: "absolute",
                left: 430,
                top: 760,
                transform: "translate(-50%, -50%) scale(0.8)",
                opacity: fade(frame, 340, 360),
              }}
            >
              <CoffeeBag width={130} />
            </div>
          )}

          {/* Customer hand */}
          {frame >= 360 && frame < 420 && (
            <div
              style={{
                position: "absolute",
                left: 1180,
                top: 740 + handoverY,
                transform: "translate(-50%, -50%)",
                opacity: customerHandOpacity,
              }}
            >
              <svg width="160" height="160" viewBox="-80 -80 160 160">
                <ellipse cx="0" cy="20" rx="35" ry="45" fill="#FFCCBC" />
                <rect x="-25" y="-40" width="50" height="70" rx="10" fill="#FFCCBC" />
                <ellipse cx="0" cy="25" rx="25" ry="8" fill="#FFAB91" />
              </svg>
            </div>
          )}

          {/* Coffee bag being handed */}
          {frame >= 370 && frame < 400 && (
            <div
              style={{
                position: "absolute",
                left: 1080,
                top: 720,
                transform: "translate(-50%, -50%)",
                opacity: fade(frame, 370, 385) - fade(frame, 390, 400),
              }}
            >
              <CoffeeBag width={120} />
            </div>
          )}
        </>
      )}
    </AbsoluteFill>
  );
};
