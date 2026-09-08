import React from "react";
import { Composition } from "remotion";
import { JokebearCoffeeComposition } from "./compositions/jokebear-coffee/VideoComposition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="jokebear-coffee"
        component={JokebearCoffeeComposition}
        durationInFrames={900}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    </>
  );
};
