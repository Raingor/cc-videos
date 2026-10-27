import React from "react";
import { Img, staticFile } from "remotion";

interface AssetProps {
  width?: number;
  style?: React.CSSProperties;
}

export const CoffeeBag: React.FC<AssetProps> = ({ width = 140, style }) => {
  return (
    <Img
      src={staticFile("assets/coffee-bag.jpg")}
      style={{
        width,
        height: "auto",
        objectFit: "contain",
        ...style,
      }}
    />
  );
};

export const CoffeeCup: React.FC<AssetProps> = ({ width = 80, style }) => {
  return (
    <Img
      src={staticFile("assets/coffee-cup.jpeg")}
      style={{
        width,
        height: "auto",
        objectFit: "contain",
        ...style,
      }}
    />
  );
};
