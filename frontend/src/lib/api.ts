import type { DetectResponse, HumanizeResponse, HumanizerMode, IntensityType } from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const detectAI = (text: string): Promise<DetectResponse> =>
  post<DetectResponse>("/api/v1/detect", { text });

export const humanizeText = (
  text: string,
  intensity: IntensityType = "balanced",
  mode: HumanizerMode = "rules"
): Promise<HumanizeResponse> =>
  post<HumanizeResponse>("/api/v1/humanize", { text, intensity, mode });
