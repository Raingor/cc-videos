import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate } from "remotion";
import { Scene1 } from "./Scene1";
import { Scene2 } from "./Scene2";
import { TIMING } from "./constants";

export const JokebearCoffeeComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // Crossfade at the transition between scene 1 and scene 2
  const scene1Opacity = interpolate(
    frame,
    [TIMING.scene1Duration - TIMING.transitionDuration, TIMING.scene1Duration],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const scene2Opacity = interpolate(
    frame,
    [TIMING.scene1Duration - TIMING.transitionDuration, TIMING.scene1Duration],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={TIMING.scene1Duration + TIMING.transitionDuration}>
        <div style={{ opacity: scene1Opacity }}>
          <Scene1 />
        </div>
      </Sequence>
      <Sequence from={TIMING.scene1Duration - TIMING.transitionDuration} durationInFrames={TIMING.scene2Duration + TIMING.transitionDuration}>
        <div style={{ opacity: scene2Opacity }}>
          <Scene2 />
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
