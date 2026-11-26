import { Video } from "@remotion/media";
import {
  AbsoluteFill,
  Composition,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import captions from "./captions.json";

// Vídeo ya cortado (silencios y errores fuera), 1080x1920, 30 fps.
const DURATION_SECONDS = 82.23;

type Caption = { text: string; startMs: number; endMs: number };

const CaptionWord: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, durationInFrames: 4, config: { damping: 200 } });
  const scale = interpolate(pop, [0, 1], [0.8, 1]);
  return (
    <AbsoluteFill
      style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 1100 }}
    >
      <div
        style={{
          fontFamily: "Montserrat, 'Arial Black', sans-serif",
          fontWeight: 900,
          fontSize: text.length > 11 ? 92 : 112,
          color: "#FFE600",
          WebkitTextStroke: "14px #000",
          paintOrder: "stroke fill",
          textShadow: "0 6px 0 rgba(0,0,0,.55)",
          textTransform: "uppercase",
          whiteSpace: "nowrap",
          transform: `scale(${scale})`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

export const CincoMotivos: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Video
        name="Vídeo cortado"
        src={staticFile("footage.mp4")}
        // Corrección cálida, como el vídeo de referencia
        style={{ filter: "contrast(1.08) saturate(1.05) sepia(0.06) brightness(1.02)" }}
      />
      {(captions as Caption[]).map((c, i) => (
        <Sequence
          key={i}
          name={`Subtítulo: ${c.text}`}
          from={Math.round((c.startMs / 1000) * fps)}
          durationInFrames={Math.max(1, Math.round(((c.endMs - c.startMs) / 1000) * fps))}
          layout="none"
        >
          <CaptionWord text={c.text} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const MyComposition = () => {
  return (
    <Composition
      id="CincoMotivos"
      component={CincoMotivos}
      durationInFrames={Math.round(DURATION_SECONDS * 30)}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
