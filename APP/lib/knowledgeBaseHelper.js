// Knowledge Base Helper - Client-side helper to query the knowledge base API
// This is used by the chat component to access CSV data

export async function queryKnowledgeBase(queryType, searchParams = {}) {
  try {
    const response = await fetch('/api/knowledge-base', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: queryType,
        queryType,
        searchParams,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Knowledge base query failed');
    }

    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Knowledge base query error:', error);
    throw error;
  }
}

// Formatted helpers for common queries

export async function searchApplicant(firstName, lastName) {
  return queryKnowledgeBase('search_applicant', { firstName, lastName });
}

export async function searchApplicantsByJobTitle(jobTitle) {
  return queryKnowledgeBase('search_applicants_by_job_title', { jobTitle });
}

export async function getCommonJobTitles() {
  return queryKnowledgeBase('get_common_job_titles');
}

export async function getApplicantsByStatus(status) {
  return queryKnowledgeBase('get_applicants_by_status', { status });
}

export async function searchEmployee(firstName, lastName) {
  return queryKnowledgeBase('search_employee', { firstName, lastName });
}

export async function getEmployeesByDepartment(department) {
  return queryKnowledgeBase('get_employees_by_department', { department });
}

export async function getTrainingByEmployeeId(employeeId) {
  return queryKnowledgeBase('get_training_by_employee_id', { employeeId });
}

export async function getTrainingByEmployeeName(firstName, lastName) {
  return queryKnowledgeBase('get_training_by_employee_name', { firstName, lastName });
}

export async function getEngagementByEmployeeId(employeeId) {
  return queryKnowledgeBase('get_engagement_by_employee_id', { employeeId });
}

export async function getEngagementByEmployeeName(firstName, lastName) {
  return queryKnowledgeBase('get_engagement_by_employee_name', { firstName, lastName });
}

export async function getTopTrainingPrograms(limit = 5) {
  return queryKnowledgeBase('get_top_training_programs', { limit });
}

export async function getTrainingStatistics() {
  return queryKnowledgeBase('get_training_statistics');
}

export async function getEngagementStatistics() {
  return queryKnowledgeBase('get_engagement_statistics');
}

export async function getKnowledgeBaseSummary() {
  return queryKnowledgeBase('get_summary');
}
