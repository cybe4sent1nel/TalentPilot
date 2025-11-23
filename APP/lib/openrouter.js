// OpenRouter API Integration for TalentPilot
import { TALENTPILOT_SYSTEM_PROMPT } from './talentPilotSystemPrompt.js';

const OPENROUTER_API_KEY = process.env.NEXT_PUBLIC_OPENROUTER_API_KEY;
const MODEL = "kwaipilot/kat-coder-pro:free";
const API_URL = "https://openrouter.ai/api/v1/chat/completions";

// Enhanced system prompt with knowledge base context
const SYSTEM_PROMPT = `${TALENTPILOT_SYSTEM_PROMPT}

---

## IMPORTANT: KNOWLEDGE BASE INTEGRATION

You have access to a knowledge base containing CSV data with:
- Recruitment applicant records (recruitment_data.csv)
- Employee records (employee_data.csv)
- Training records (training_and_development_data.csv)
- Engagement survey data (employee_engagement_survey_data.csv)

When users ask questions about:
- Specific applicants (e.g., "What's the status of Melissa Hicks?") → Search recruitment data
- Specific employees (e.g., "Tell me about John Smith") → Search employee data
- Training records (e.g., "What training has Sarah completed?") → Search training data
- Engagement metrics (e.g., "What's the engagement score?") → Search engagement data
- Job title trends (e.g., "Most common job titles") → Analyze recruitment data
- Department statistics (e.g., "How many in Sales?") → Analyze employee data

ALWAYS respond with "Let me search our knowledge base for this information..." before providing answers from the CSV data.

The knowledge base API is available to the frontend application. When the user's question requires CSV data lookup, provide your response as if you have already queried the data (the frontend will handle the actual API call).

For applicant searches, the recruitment_data.csv contains: Applicant ID, First Name, Last Name, Job Title, Status, Desired Salary, Years of Experience, Education Level, and more.

For employee searches, employee_data.csv contains: EmpID, FirstName, LastName, Title, Department, EmployeeStatus, Performance Score, and more.`;

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
