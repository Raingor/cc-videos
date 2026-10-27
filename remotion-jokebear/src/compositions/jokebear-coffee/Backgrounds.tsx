import React from "react";
import { COLORS } from "./constants";

export const EntranceBackground: React.FC = () => (
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="entranceSky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={COLORS.skyTop} />
        <stop offset="100%" stopColor={COLORS.skyBottom} />
      </linearGradient>
      <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="6" />
        <feOffset dx="0" dy="6" result="offsetblur" />
        <feComponentTransfer>
          <feFuncA type="linear" slope="0.2" />
        </feComponentTransfer>
        <feMerge>
          <feMergeNode />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>

    {/* Sky */}
    <rect width="1920" height="1080" fill="url(#entranceSky)" />

    {/* Sun glow */}
    <circle cx="1600" cy="200" r="120" fill={COLORS.sun} opacity="0.4" />

    {/* Distant buildings */}
    <rect x="100" y="350" width="300" height="500" fill={COLORS.buildingShadow} />
    <rect x="450" y="300" width="260" height="550" fill={COLORS.building} />
    <rect x="1200" y="320" width="350" height="530" fill={COLORS.buildingShadow} />
    <rect x="1600" y="380" width="250" height="470" fill={COLORS.building} />

    {/* Main building */}
    <rect x="560" y="150" width="800" height="800" fill={COLORS.building} />
    <rect x="560" y="150" width="800" height="40" fill={COLORS.buildingShadow} />
    <rect x="540" y="140" width="840" height="25" rx="5" fill={COLORS.buildingShadow} />

    {/* Door */}
    <rect x="860" y="420" width="200" height="530" fill="#8D6E63" />
    <rect x="875" y="435" width="170" height="500" fill="#A1887F" />
    <circle cx="1030" cy="680" r="6" fill="#5D4037" />

    {/* Steps */}
    <rect x="760" y="820" width="400" height="30" fill={COLORS.step} />
    <rect x="740" y="850" width="440" height="35" fill={COLORS.stepEdge} />
    <rect x="720" y="885" width="480" height="40" fill={COLORS.step} />

    {/* Sidewalk */}
    <rect x="0" y="925" width="1920" height="155" fill={COLORS.sidewalk} />
    <line x1="0" y1="925" x2="1920" y2="925" stroke={COLORS.buildingShadow} strokeWidth="4" />

    {/* Potted plant */}
    <g transform="translate(1320, 780)">
      <rect x="0" y="80" width="60" height="70" rx="4" fill="#8D6E63" />
      <circle cx="30" cy="60" r="50" fill={COLORS.tree} />
      <circle cx="10" cy="50" r="25" fill={COLORS.grass} />
      <circle cx="50" cy="45" r="28" fill={COLORS.grass} />
    </g>

    {/* Soft golden light overlay */}
    <rect width="1920" height="1080" fill={COLORS.yellow} opacity="0.08" />
  </svg>
);

export const StreetBackground: React.FC = () => (
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="streetSky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#FFAB91" />
        <stop offset="50%" stopColor={COLORS.skyTop} />
        <stop offset="100%" stopColor={COLORS.skyBottom} />
      </linearGradient>
    </defs>

    {/* Sky */}
    <rect width="1920" height="1080" fill="url(#streetSky)" />

    {/* Sun */}
    <circle cx="1600" cy="350" r="140" fill={COLORS.sun} opacity="0.5" />

    {/* Distant city silhouette */}
    <rect x="0" y="500" width="220" height="300" fill={COLORS.buildingShadow} opacity="0.8" />
    <rect x="240" y="480" width="180" height="320" fill={COLORS.buildingShadow} opacity="0.7" />
    <rect x="450" y="520" width="200" height="280" fill={COLORS.buildingShadow} opacity="0.8" />
    <rect x="1300" y="490" width="250" height="310" fill={COLORS.buildingShadow} opacity="0.7" />
    <rect x="1580" y="510" width="200" height="290" fill={COLORS.buildingShadow} opacity="0.8" />
    <rect x="1800" y="540" width="120" height="260" fill={COLORS.buildingShadow} opacity="0.7" />

    {/* Road */}
    <rect x="0" y="760" width="1920" height="320" fill={COLORS.road} />
    <line x1="0" y1="780" x2="1920" y2="780" stroke="#607D8B" strokeWidth="4" />

    {/* Sidewalks */}
    <rect x="0" y="700" width="1920" height="60" fill={COLORS.sidewalk} />
    <rect x="0" y="1080" width="1920" height="0" fill={COLORS.sidewalk} />

    {/* Road center dashed line */}
    {Array.from({ length: 20 }).map((_, i) => (
      <rect key={i} x={i * 120} y="905" width="60" height="10" fill="#FFF" opacity="0.6" />
    ))}

    {/* Trees along sidewalk */}
    {Array.from({ length: 6 }).map((_, i) => (
      <g key={i} transform={`translate(${220 + i * 320}, 620)`}>
        <rect x="18" y="60" width="14" height="60" fill="#8D6E63" />
        <circle cx="25" cy="40" r="45" fill={COLORS.tree} />
        <circle cx="5" cy="50" r="30" fill={COLORS.grass} />
        <circle cx="45" cy="45" r="32" fill={COLORS.grass} />
      </g>
    ))}

    {/* Warm light overlay */}
    <rect width="1920" height="1080" fill={COLORS.yellow} opacity="0.06" />
  </svg>
);

export const DeliveryHandBackground: React.FC = () => (
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="handSky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={COLORS.skyTop} />
        <stop offset="100%" stopColor={COLORS.skyBottom} />
      </linearGradient>
    </defs>

    <rect width="1920" height="1080" fill="url(#handSky)" />
    <circle cx="1500" cy="180" r="120" fill={COLORS.sun} opacity="0.35" />

    {/* Soft building wall */}
    <rect x="300" y="100" width="1320" height="900" fill={COLORS.building} />
    <rect x="300" y="100" width="1320" height="20" fill={COLORS.buildingShadow} />

    {/* Doorway */}
    <rect x="840" y="380" width="240" height="620" fill="#8D6E63" />
    <rect x="860" y="400" width="200" height="600" fill="#A1887F" />

    {/* Sidewalk */}
    <rect x="0" y="900" width="1920" height="180" fill={COLORS.sidewalk} />

    <rect width="1920" height="1080" fill={COLORS.yellow} opacity="0.08" />
  </svg>
);
