\# Kiro Instructions



\## Project

CampusArchive is a centralized web-based digital archive for institutional academic projects. It allows students to submit projects and faculty guides to review, provide feedback, grade, and approve or reject submissions.



\## Technology Stack

\- Frontend: HTML, CSS, JavaScript, Bootstrap, Jinja2

\- Backend: Python Flask

\- Database: MySQL

\- Database Connector: PyMySQL

\- Authentication: Flask-based authentication

\- Version Control: Git and GitHub



\## User Roles

\### Student

\- Register/login

\- Create and submit projects

\- Upload project reports and source code

\- Add project title, abstract, technologies, and other metadata

\- Track project status

\- View faculty feedback and grades



\### Faculty

\- Login

\- View assigned/submitted projects

\- Review project details and files

\- Provide feedback

\- Assign grades

\- Approve or reject submissions



\### Admin

\- Manage users

\- Manage projects

\- Manage faculty and students

\- Monitor the overall archive

\- Manage system-level data



\## Core Features

\- User authentication and authorization

\- Role-based dashboards

\- Project submission

\- File uploads

\- Faculty review workflow

\- Feedback and grading

\- Project approval/rejection

\- Search and filtering

\- Project metadata management

\- Database persistence

\- Responsive UI

\- Light and dark themes



\## Kiro Development Instructions



1\. Understand the existing project structure before making changes.

2\. Preserve the existing Flask backend, database structure, routes, APIs, and Jinja2 connections unless a change is explicitly required.

3\. Do not remove working functionality while modifying the UI.

4\. Reuse existing components, routes, templates, and database operations wherever possible.

5\. Keep frontend and backend functionality properly connected.

6\. Do not use dummy data or placeholder functionality in the final application.

7\. Do not use Lorem Ipsum text.

8\. Do not introduce unnecessary dependencies.

9\. Maintain consistent naming and folder structure.

10\. Ensure all forms, buttons, navigation links, authentication flows, and database operations work correctly.

11\. Handle errors gracefully and provide meaningful user feedback.

12\. Keep the interface responsive for desktop and smaller screens.

13\. Maintain both light and dark theme functionality.

14\. Follow clean, readable, and maintainable coding practices.

15\. Test changes before considering a feature complete.

16\. Do not overwrite existing project files unnecessarily.

17\. When modifying the frontend, preserve all existing backend functionality and Jinja2 variables.

18\. When adding a feature, integrate it with the existing database and application architecture instead of creating disconnected mock functionality.



\## UI Guidelines



\- Use a clean, modern academic/project-archive interface.

\- Maintain consistent spacing, typography, buttons, forms, cards, and navigation.

\- Ensure good contrast and readability in both light and dark modes.

\- Avoid excessive animations or distracting visual effects.

\- Do not use emojis as UI elements.

\- Do not use fake or unrelated images.

\- Keep the interface professional and suitable for an educational institution.



\## Database Guidelines



\- Use the existing MySQL schema wherever possible.

\- Do not delete existing tables or data without explicit instruction.

\- Maintain relationships between students, faculty, projects, submissions, feedback, and approvals.

\- Use parameterized queries to prevent SQL injection.

\- Validate user input before database operations.



\## File Upload Guidelines



\- Validate uploaded files.

\- Use safe filenames and secure upload handling.

\- Store uploaded files in the designated upload directory.

\- Do not expose sensitive server-side paths unnecessarily.

\- Prevent unauthorized users from accessing restricted project files.



\## Final Requirement



The final application should be a functional CampusArchive system rather than a static frontend prototype. All major pages should remain connected to the Flask backend and MySQL database, and existing functionality should not be broken while improving or extending the application.

