# Design Choices and Time Spent

## Website Selection  [2h]

After careful consideration, I decided to focus on web scraping [We Work Remotely](https://weworkremotely.com/) for this project. This decision was influenced by my ongoing interest in job hunting technologies, as demonstrated in my previous projects: [Husky Job Application Tracker](https://github.com/cathyfu1215/huksyApplicationTracker) and [Husky Interview Prep](https://github.com/cathyfu1215/huskyinterviewprep).

### Research Process [3+ h]

I researched best practices for ethical web scraping and analyzed the robots.txt files of potential target websites:

- **Indeed**: Their robots.txt prohibits most forms of automated scraping, making it unsuitable for this project.
- **We Work Remotely**: Their policy is more permissive toward responsible scraping activities.

As a beginner with Selenium, I determined that We Work Remotely would provide a more accessible and ethically sound environment for developing my web scraping skills.

## Database Choices: Google Firebase [1h]

### SQL vs NoSQL 

After analyzing the content structure on We Work Remotely, I found the data model to be straightforward yet variable. I quickly developed a schema focusing on the primary entity: Jobs. During this analysis, I observed that job listings contain numerous optional fields, which would result in many null values if implemented in a traditional SQL database.

While SQL databases excel at maintaining data integrity and preventing duplicates, my research revealed that We Work Remotely job listings include unique identifiers in their URLs. This feature enables duplicate prevention during the scraping process, making a NoSQL solution equally viable for this requirement.

Furthermore, I considered future expansion opportunities for this project. Beyond job listings, the system could eventually incorporate additional entities such as companies and users. Each job could store application history and associated interview questions; companies could maintain listings of their open positions; and users could track their interview experiences across multiple companies. A NoSQL database offers greater flexibility for these potential relationship models (though GraphQL could also be considered for future implementations). For convenience and familiarity, I selected Firebase as my NoSQL solution.

## Technology Stack Decisions

### Backend: FastAPI [2h]

For the backend implementation of this project, I selected FastAPI for several strategic reasons:

1. **Learning Opportunity**: While I have no prior experience with FastAPI, this project presented an ideal opportunity to expand my technical skillset. FastAPI's intuitive design and comprehensive documentation make it approachable for newcomers.

2. **Performance Considerations**: FastAPI's high-performance capabilities are particularly well-suited for a web scraping application. Its asynchronous request handling aligns perfectly with the potentially time-intensive nature of scraping operations.

3. **API Documentation**: The automatic interactive API documentation generation simplifies both development and potential future collaboration. This feature is especially valuable for a project that will expose job data through API endpoints.

4. **Python Ecosystem**: Leveraging Python for both the scraping logic and API layer creates a cohesive development experience, eliminating the need to context-switch between different programming languages.

### Frontend: React [1h]

For the frontend implementation, I opted to use React based on the following considerations:

1. **Familiarity and Productivity**: My previous experience with React allows for faster development cycles and implementation of complex UI features.

2. **Component Architecture**: React's component-based design is ideal for displaying job listings with consistent styling and behavior, while allowing for modular development.

3. **State Management**: Managing the state of filtered job searches, pagination, and user preferences is streamlined through React's ecosystem of state management solutions.

4. **Data Visualization**: The potential to implement interactive visualizations of job market trends (by location, salary ranges, or skills) is well-supported by React's integration with visualization libraries.

### Project Analysis and Justification

This web scraping project has several characteristics that make these technology choices particularly appropriate:

- **Data Processing Pipeline**: The flow from web scraping to data storage to API endpoints to frontend display benefits from FastAPI's streamlined request handling and React's efficient rendering.

- **Scalability Concerns**: As the dataset grows with continuous scraping, both FastAPI's performance and React's virtual DOM approach help maintain responsiveness even with larger data volumes.

- **Feature Expansion**: The potential future features (user accounts, saved searches, email notifications) would be well-supported by FastAPI's authentication capabilities and React's component reusability.

- **Development Timeline**: The combination of a familiar frontend technology with a new but approachable backend framework strikes an effective balance between learning and delivery speed.

This technology stack provides a solid foundation for not only the current requirements but also for future enhancements to this job market analysis tool.

