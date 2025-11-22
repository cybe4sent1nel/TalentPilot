// Sample Prompts for TalentPilot Demo
export const samplePrompts = [
  {
    category: "Recruitment",
    prompts: [
      "What are the most common job titles in our current applicant pipeline?",
      "Analyze our recruitment data - what's the average years of experience for applicants?",
      "Show me a summary of applicant statuses - how many are interviewing vs offered?",
      "What's the salary range expectations from our current candidates?",
    ],
  },
  {
    category: "Employee Management",
    prompts: [
      "What are the top performing departments based on employee performance scores?",
      "Analyze our employee data - what's the breakdown by employment type?",
      "Show me trends in employee tenure and retention",
      "Which divisions have the highest concentration of employees?",
    ],
  },
  {
    category: "Training & Development",
    prompts: [
      "What training programs have the highest completion rates?",
      "Analyze training outcomes - which types of training are most effective?",
      "Which departments have invested most in employee training?",
      "Show me the ROI of our training programs based on program type and outcome",
    ],
  },
  {
    category: "Engagement & Culture",
    prompts: [
      "What's the overall employee engagement score trend?",
      "Analyze work-life balance scores across the organization",
      "Which departments have the highest satisfaction scores?",
      "Provide insights on employee engagement patterns and recommendations",
    ],
  },
  {
    category: "Strategic HR",
    prompts: [
      "Help me design a talent acquisition strategy for high-growth roles",
      "What are best practices for improving employee engagement?",
      "Draft a performance improvement plan template for underperforming employees",
      "Create a competitive compensation strategy for our organization",
    ],
  },
];

export function getRandomSamplePrompt() {
  const flatPrompts = samplePrompts.flatMap(category => category.prompts);
  return flatPrompts[Math.floor(Math.random() * flatPrompts.length)];
}

export function getPromptsByCategory(category) {
  const found = samplePrompts.find(c => c.category === category);
  return found ? found.prompts : [];
}
