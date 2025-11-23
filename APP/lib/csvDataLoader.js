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
  }

  async loadAllData() {
    if (this.isLoaded) return;

    try {
      const basePath = process.cwd();
      
      // Load recruitment data
      this.recruitment = this.loadCSV(
        path.join(basePath, 'recruitment_data.csv')
      );
      
      // Load employee data
      this.employees = this.loadCSV(
        path.join(basePath, 'employee_data.csv')
      );
      
      // Load training data
      this.training = this.loadCSV(
        path.join(basePath, 'training_and_development_data.csv')
      );
      
      // Load engagement data
      this.engagement = this.loadCSV(
        path.join(basePath, 'employee_engagement_survey_data.csv')
      );

      this.isLoaded = true;
      console.log('CSV data loaded successfully');
    } catch (error) {
      console.error('Error loading CSV data:', error);
      this.isLoaded = false;
    }
  }

  loadCSV(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${filePath}`);
        return [];
      }

      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const records = parse(fileContent, {
        columns: true,
        skip_empty_lines: true,
      });

      return records;
    } catch (error) {
      console.error(`Error parsing ${filePath}:`, error);
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

  // Get training records by employee
  getTrainingByEmployee(firstName, lastName) {
    if (!this.training) return [];

    return this.training.filter(
      (record) =>
        record['First Name']?.toLowerCase() === firstName.toLowerCase() &&
        record['Last Name']?.toLowerCase() === lastName.toLowerCase()
    );
  }

  // Get engagement data by employee
  getEngagementByEmployee(employeeId) {
    if (!this.engagement) return null;

    return this.engagement.find(
      (record) => record['Employee ID']?.toString() === employeeId.toString()
    );
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
