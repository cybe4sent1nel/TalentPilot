// OpenRouter API Integration for TalentPilot
import { TALENTPILOT_SYSTEM_PROMPT } from './talentPilotSystemPrompt.js';

const OPENROUTER_API_KEY = process.env.NEXT_PUBLIC_OPENROUTER_API_KEY;
const MODEL = "kwaipilot/kat-coder-pro:free";
const API_URL = "https://openrouter.ai/api/v1/chat/completions";

const SYSTEM_PROMPT = TALENTPILOT_SYSTEM_PROMPT;

export async function sendMessage(messages) {
  if (!OPENROUTER_API_KEY) {
    throw new Error("OpenRouter API key not configured");
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
        "HTTP-Referer": window.location.origin,
        "X-Title": "TalentPilot",
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          {
            role: "system",
            content: SYSTEM_PROMPT,
          },
          ...messages,
        ],
        temperature: 0.7,
        max_tokens: 2048,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || "OpenRouter API error");
    }

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error("OpenRouter API error:", error);
    throw error;
  }
}
