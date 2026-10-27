#!/bin/zsh
# Build the audio track for jokebear-coffee video (30s) and mux it into the final MP4.
# SFX timeline (aligned with Remotion frames @30fps):
#   3.0s  phone notification ding-ding (phone vibrates at frame 90)
#   15s   scooter hum starts, fades out ~22-24s (ride scene 15-25s)
#   25.5s paper rustle on handover
#   0-30s soft urban ambience throughout

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

mkdir -p output/audio

# 1. Phone notification: two-tone ding (E6 then G6) with exponential decay
ffmpeg -y -f lavfi -i "aevalsrc=0.45*exp(-14*t)*sin(2*PI*1318*t):s=44100:d=0.35" -ac 1 output/audio/ding1.wav
ffmpeg -y -f lavfi -i "aevalsrc=0.45*exp(-10*t)*sin(2*PI*1568*t):s=44100:d=0.5" -ac 1 output/audio/ding2.wav

# 2. Urban ambience: soft filtered pink noise, gentle evening vibe
ffmpeg -y -f lavfi -i "anoisesrc=color=pink:amplitude=0.5:seed=42:d=30" -af "lowpass=f=550,highpass=f=90,volume=0.35" -ac 1 output/audio/ambience.wav

# 3. Scooter hum: layered sines (82Hz base + harmonics) + road noise, 10s with fade in/out
ffmpeg -y -f lavfi -i "aevalsrc=0.16*(sin(2*PI*82*t)+0.4*sin(2*PI*164*t)+0.2*sin(2*PI*246*t)+0.1*sin(2*PI*328*t)):s=44100:d=10" -f lavfi -i "anoisesrc=color=pink:amplitude=0.3:seed=7:d=10" -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0,lowpass=f=900,afade=t=in:d=1.2,afade=t=out:st=8:d=2" -ac 1 output/audio/scooter.wav

# 4. Paper/bag rustle for handover: short bandpassed noise burst
ffmpeg -y -f lavfi -i "anoisesrc=color=white:amplitude=0.6:seed=7:d=0.4" -af "bandpass=f=2600:w=1800,volume=0.55,afade=t=in:d=0.06,afade=t=out:st=0.2:d=0.2" -ac 1 output/audio/rustle.wav

# 5. Mix everything at the right timestamps
ffmpeg -y -i output/audio/ambience.wav -i output/audio/ding1.wav -i output/audio/ding2.wav -i output/audio/scooter.wav -i output/audio/rustle.wav -filter_complex "[1:a]adelay=3000[a1];[2:a]adelay=3180[a2];[3:a]adelay=15000[a3];[4:a]adelay=25500[a4];[0:a][a1][a2][a3][a4]amix=inputs=5:normalize=0:duration=first,alimiter=limit=0.85,atrim=0:30,afade=t=out:st=29:d=1" -ar 44100 output/audio/final-mix.wav

# 6. Mux audio into the rendered video (video stream copied, no re-encode)
ffmpeg -y -i output/jokebear-coffee.mp4 -i output/audio/final-mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest output/jokebear-coffee-final.mp4

echo "Done: output/jokebear-coffee-final.mp4"
