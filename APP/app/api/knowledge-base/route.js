// API Route for Knowledge Base Queries
import { getDataLoader } from '@/lib/csvDataLoader';

export async function POST(request) {
  try {
    const { query, queryType, searchParams } = await request.json();

    if (!query || !queryType) {
      return new Response(
        JSON.stringify({
          error: 'query and queryType are required',
        }),
        { status: 400 }
      );
    }

    const dataLoader = await getDataLoader();

    let results = null;

    switch (queryType) {
      case 'search_applicant':
        // search_applicant with { firstName, lastName }
        results = dataLoader.searchApplicant(
          searchParams.firstName,
          searchParams.lastName
        );
        break;

      case 'search_applicants_by_job_title':
        // search_applicants_by_job_title with { jobTitle }
        results = dataLoader.searchApplicantsByJobTitle(searchParams.jobTitle);
        break;

      case 'get_common_job_titles':
        // No params needed
        results = dataLoader.getCommonJobTitles();
        break;

      case 'get_applicants_by_status':
        // get_applicants_by_status with { status }
        results = dataLoader.getApplicantsByStatus(searchParams.status);
        break;

      case 'search_employee':
        // search_employee with { firstName, lastName }
        results = dataLoader.searchEmployee(
          searchParams.firstName,
          searchParams.lastName
        );
        break;

      case 'get_employees_by_department':
        // get_employees_by_department with { department }
        results = dataLoader.getEmployeesByDepartment(searchParams.department);
        break;

      case 'get_training_by_employee_id':
        // get_training_by_employee_id with { employeeId }
        results = dataLoader.getTrainingByEmployeeId(searchParams.employeeId);
        break;

      case 'get_training_by_employee_name':
        // get_training_by_employee_name with { firstName, lastName }
        results = dataLoader.getTrainingByEmployeeName(
          searchParams.firstName,
          searchParams.lastName
        );
        break;

      case 'get_engagement_by_employee_id':
        // get_engagement_by_employee_id with { employeeId }
        results = dataLoader.getEngagementByEmployeeId(searchParams.employeeId);
        break;

      case 'get_engagement_by_employee_name':
        // get_engagement_by_employee_name with { firstName, lastName }
        results = dataLoader.getEngagementByEmployeeName(
          searchParams.firstName,
          searchParams.lastName
        );
        break;

      case 'get_top_training_programs':
        // get_top_training_programs with optional { limit }
        results = dataLoader.getTopTrainingPrograms(searchParams.limit || 5);
        break;

      case 'get_training_statistics':
        // No params needed
        results = dataLoader.getTrainingStatistics();
        break;

      case 'get_engagement_statistics':
        // No params needed
        results = dataLoader.getEngagementStatistics();
        break;

      case 'get_summary':
        // No params needed
        results = dataLoader.getSummary();
        break;

      default:
        return new Response(
          JSON.stringify({
            error: `Unknown queryType: ${queryType}`,
          }),
          { status: 400 }
        );
    }

    return new Response(
      JSON.stringify({
        success: true,
        queryType,
        results,
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Knowledge base API error:', error);
    return new Response(
      JSON.stringify({
        error: error.message,
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
