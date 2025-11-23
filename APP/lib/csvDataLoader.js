// CSV Data Loader - Loads and manages CSV knowledge base
import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';

class CSVDataLoader {
  constructor() {
    this.recruitment = null;
    this.employees = null;
    this.training = null;
    this.engagement = null;
    this.isLoaded = false;
    this.loadAttempted = false;
  }

  async loadAllData() {
    if (this.loadAttempted) return;
    this.loadAttempted = true;

    try {
      const basePath = process.cwd();
      
      console.log(`[TalentPilot KB] Loading CSV files from: ${basePath}`);
      
      // Load all 4 CSV files
      const recruitmentPath = path.join(basePath, 'recruitment_data.csv');
      const employeePath = path.join(basePath, 'employee_data.csv');
      const trainingPath = path.join(basePath, 'training_and_development_data.csv');
      const engagementPath = path.join(basePath, 'employee_engagement_survey_data.csv');

      this.recruitment = this.loadCSV(recruitmentPath, 'recruitment_data.csv');
      this.employees = this.loadCSV(employeePath, 'employee_data.csv');
      this.training = this.loadCSV(trainingPath, 'training_and_development_data.csv');
      this.engagement = this.loadCSV(engagementPath, 'employee_engagement_survey_data.csv');

      const recruitmentCount = this.recruitment?.length || 0;
      const employeeCount = this.employees?.length || 0;
      const trainingCount = this.training?.length || 0;
      const engagementCount = this.engagement?.length || 0;

      console.log(`[TalentPilot KB] Data loaded successfully:`);
      console.log(`  - Recruitment: ${recruitmentCount} records`);
      console.log(`  - Employees: ${employeeCount} records`);
      console.log(`  - Training: ${trainingCount} records`);
      console.log(`  - Engagement: ${engagementCount} records`);

      this.isLoaded = true;
    } catch (error) {
      console.error('[TalentPilot KB] Error loading CSV data:', error);
      this.isLoaded = false;
    }
  }

  loadCSV(filePath, fileName) {
    try {
      if (!fs.existsSync(filePath)) {
        console.warn(`[TalentPilot KB] File not found: ${fileName} at ${filePath}`);
        return [];
      }

      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const records = parse(fileContent, {
        columns: true,
        skip_empty_lines: true,
        trim: true,
      });

      console.log(`[TalentPilot KB] Loaded ${fileName}: ${records.length} records`);
      return records;
    } catch (error) {
      console.error(`[TalentPilot KB] Error parsing ${fileName}:`, error.message);
      return [];
    }
  }

  // Search for applicant by name
  searchApplicant(firstName, lastName) {
    if (!this.recruitment) return null;

    return this.recruitment.find(
      (record) =>
        record['First Name']?.toLowerCase() === firstName.toLowerCase() &&
        record['Last Name']?.toLowerCase() === lastName.toLowerCase()
    );
  }

  // Search for applicants by job title
  searchApplicantsByJobTitle(jobTitle) {
    if (!this.recruitment) return [];

    return this.recruitment.filter((record) =>
      record['Job Title']?.toLowerCase().includes(jobTitle.toLowerCase())
    );
  }

  // Get common job titles
  getCommonJobTitles() {
    if (!this.recruitment) return [];

    const titleCounts = {};
    this.recruitment.forEach((record) => {
      const title = record['Job Title'];
      if (title) {
        titleCounts[title] = (titleCounts[title] || 0) + 1;
      }
    });

    return Object.entries(titleCounts)
      .map(([title, count]) => ({ title, count }))
      .sort((a, b) => b.count - a.count);
  }

  // Get applicants by status
  getApplicantsByStatus(status) {
    if (!this.recruitment) return [];

    return this.recruitment.filter(
      (record) =>
        record['Status']?.toLowerCase() === status.toLowerCase()
    );
  }

  // Search for employee by name
  searchEmployee(firstName, lastName) {
    if (!this.employees) return null;

    return this.employees.find(
      (record) =>
        record['FirstName']?.toLowerCase() === firstName.toLowerCase() &&
        record['LastName']?.toLowerCase() === lastName.toLowerCase()
    );
  }

  // Get employees by department
  getEmployeesByDepartment(department) {
    if (!this.employees) return [];

    return this.employees.filter((record) =>
      record['DepartmentType']?.toLowerCase().includes(department.toLowerCase())
    );
  }

  // Get training records by employee ID
  getTrainingByEmployeeId(employeeId) {
    if (!this.training) return [];

    return this.training.filter(
      (record) => record['Employee ID']?.toString() === employeeId.toString()
    );
  }

  // Get training records by employee name (from employee data)
  getTrainingByEmployeeName(firstName, lastName) {
    if (!this.employees || !this.training) return [];

    // First find the employee
    const employee = this.employees.find(
      (e) =>
        e['FirstName']?.toLowerCase() === firstName.toLowerCase() &&
        e['LastName']?.toLowerCase() === lastName.toLowerCase()
    );

    if (!employee) return [];

    // Then get all training records for that employee
    return this.training.filter(
      (record) => record['Employee ID']?.toString() === employee['EmpID']?.toString()
    );
  }

  // Get engagement data by employee ID
  getEngagementByEmployeeId(employeeId) {
    if (!this.engagement) return null;

    return this.engagement.find(
      (record) => record['Employee ID']?.toString() === employeeId.toString()
    );
  }

  // Get all engagement data for an employee by name
  getEngagementByEmployeeName(firstName, lastName) {
    if (!this.employees || !this.engagement) return null;

    // Find the employee
    const employee = this.employees.find(
      (e) =>
        e['FirstName']?.toLowerCase() === firstName.toLowerCase() &&
        e['LastName']?.toLowerCase() === lastName.toLowerCase()
    );

    if (!employee) return null;

    // Get engagement data
    return this.engagement.find(
      (record) => record['Employee ID']?.toString() === employee['EmpID']?.toString()
    );
  }

  // Get top training programs by enrollment
  getTopTrainingPrograms(limit = 5) {
    if (!this.training) return [];

    const programCounts = {};
    this.training.forEach((record) => {
      const program = record['Training Program Name'];
      if (program) {
        programCounts[program] = (programCounts[program] || 0) + 1;
      }
    });

    return Object.entries(programCounts)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, limit);
  }

  // Get training statistics
  getTrainingStatistics() {
    if (!this.training) return {};

    const stats = {
      total: this.training.length,
      byOutcome: {},
      byType: {},
      averageCost: 0,
      averageDuration: 0,
    };

    let totalCost = 0;
    let totalDuration = 0;
    let costCount = 0;
    let durationCount = 0;

    this.training.forEach((record) => {
      const outcome = record['Training Outcome'] || 'Unknown';
      stats.byOutcome[outcome] = (stats.byOutcome[outcome] || 0) + 1;

      const type = record['Training Type'] || 'Unknown';
      stats.byType[type] = (stats.byType[type] || 0) + 1;

      const cost = parseFloat(record['Training Cost(Days)']) || 0;
      if (cost > 0) {
        totalCost += cost;
        costCount++;
      }

      const duration = parseInt(record['Training Duration(Days)']) || 0;
      if (duration > 0) {
        totalDuration += duration;
        durationCount++;
      }
    });

    stats.averageCost = costCount > 0 ? (totalCost / costCount).toFixed(2) : 0;
    stats.averageDuration = durationCount > 0 ? (totalDuration / durationCount).toFixed(2) : 0;

    return stats;
  }

  // Get engagement statistics
  getEngagementStatistics() {
    if (!this.engagement) return {};

    const stats = {
      total: this.engagement.length,
      averageEngagementScore: 0,
      averageSatisfactionScore: 0,
      averageWorkLifeBalance: 0,
    };

    let totalEngagement = 0;
    let totalSatisfaction = 0;
    let totalBalance = 0;

    this.engagement.forEach((record) => {
      const engagement = parseFloat(record['Engagement Score']) || 0;
      const satisfaction = parseFloat(record['Satisfaction Score']) || 0;
      const balance = parseFloat(record['Work-Life Balance Score']) || 0;

      totalEngagement += engagement;
      totalSatisfaction += satisfaction;
      totalBalance += balance;
    });

    stats.averageEngagementScore = (totalEngagement / this.engagement.length).toFixed(2);
    stats.averageSatisfactionScore = (totalSatisfaction / this.engagement.length).toFixed(2);
    stats.averageWorkLifeBalance = (totalBalance / this.engagement.length).toFixed(2);

    return stats;
  }

  // Get summary statistics
  getSummary() {
    return {
      recruitment: {
        total: this.recruitment?.length || 0,
        byStatus: this.getStatusCounts(),
      },
      employees: {
        total: this.employees?.length || 0,
        byDepartment: this.getDepartmentCounts(),
      },
      training: {
        total: this.training?.length || 0,
      },
      engagement: {
        total: this.engagement?.length || 0,
      },
    };
  }

  getStatusCounts() {
    const counts = {};
    (this.recruitment || []).forEach((record) => {
      const status = record['Status'] || 'Unknown';
      counts[status] = (counts[status] || 0) + 1;
    });
    return counts;
  }

  getDepartmentCounts() {
    const counts = {};
    (this.employees || []).forEach((record) => {
      const dept = record['DepartmentType'] || 'Unknown';
      counts[dept] = (counts[dept] || 0) + 1;
    });
    return counts;
  }
}

// Create singleton instance
let instance = null;

export async function getDataLoader() {
  if (!instance) {
    instance = new CSVDataLoader();
    await instance.loadAllData();
  }
  return instance;
}

export default CSVDataLoader;
