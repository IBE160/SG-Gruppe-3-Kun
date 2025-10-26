# Product Brief: HMSREG Documentation Chatbot

## 1. Executive Summary

The HMSREG Documentation Chatbot is a conversational AI assistant designed to provide quick and accurate answers to users of the HMSREG system. The chatbot will address the significant challenge users face in navigating extensive and complex documentation, which currently leads to user frustration and a high volume of repetitive support tickets. By leveraging the official HMSREG documentation, the chatbot will deliver role-based, context-aware responses, improving user efficiency, reducing support workload, and making critical information more accessible 24/7. The Minimum Viable Product (MVP) will focus on delivering a robust chat interface with a comprehensive knowledge base, targeting subcontractors as the primary user segment.

## 2. Project Name

HMSREG Documentation Chatbot

## 3. Problem Statement

Users of the HMSREG system, across all roles, find it difficult and time-consuming to locate information within the extensive documentation. This leads to users spending several minutes searching before giving up and contacting the support team. This results in a significant and unnecessary workload on support agents, who have to answer repetitive questions. Furthermore, this difficulty in self-serving causes user frustration and a negative perception of the system.

## 4. Proposed Solution

The proposed solution is a chatbot that will make finding information easier and less time-consuming for users. The chatbot will provide direct answers to user questions, addressing the issue of users not knowing the correct terminology to search for, or when the answer is a combination of multiple articles. By providing 24/7 support, the chatbot will empower users to find answers on their own, freeing up the support team to focus on more complex and billable tasks, such as courses and consultant work. This will lead to improved customer satisfaction and a more efficient support operation.

## 5. Target Users

### Primary User Segment

*   **Subcontractors:** This is the most critical user group for the MVP. Their most frequent and urgent questions relate to managing their crew, inviting colleagues and other subcontractors, and uploading documents for audits.

### Secondary User Segments

*   **Suppliers, Construction Workers, Project Managers, Administrators, and Support Personnel:** Each of these groups has unique tasks and questions and uses the system in different ways. The chatbot will be designed to cater to their specific needs by providing role-based personalization.

## 6. Goals and Success Metrics

### Business Objectives

*   Reduce the volume of support tickets related to common HMSREG documentation questions.
*   Increase the support team's capacity for billable hours (e.g., courses, consultant work).
*   Improve overall customer satisfaction with the HMSREG system.
*   Identify documentation gaps and frequently asked topics to improve HMSREG resources.

### User Success Metrics

*   The chatbot provides accurate and helpful answers to at least 80% of HMSREG documentation questions.
*   Achieve a user satisfaction rating of 4/5 or higher.
*   Users can successfully find an answer in the chatbot without needing to contact support.

### Key Performance Indicators (KPIs)

*   Average response time under 5 seconds for standard queries.
*   Percentage of questions successfully answered by the chatbot.
*   User satisfaction ratings (e.g., thumbs up/down, 1-5 scale).
*   Number of support tickets related to documentation questions.
*   Fallback rate (the percentage of questions the chatbot cannot answer).

## 7. MVP Scope

### Core Features (MVP)

1.  **Chat Interface:** A user-friendly interface for asking questions.
2.  **Knowledge Base Integration:** The chatbot must be able to access and retrieve information from the `docs.hmsreg.com` knowledge base.
3.  **Search and Retrieval:** The chatbot must be able to understand user queries and retrieve relevant information from the knowledge base.
4.  **Role-based Personalization:** The chatbot should ask for the user's role to provide tailored answers.
5.  **Fallback Mechanism:** The chatbot must have a mechanism to handle questions it cannot answer, providing users with alternative support channels.

### Out of Scope (for MVP)

*   Proactive Assistance
*   Example scenarios / "What do I do if..." guides
*   Interactive troubleshooting
*   Clarifying questions to understand user's role
*   Log of common questions for analysis and documentation improvement
*   Multi-language support (The MVP will focus on Norwegian, with English as a post-MVP feature)
*   Improved UI with enhanced user experience
*   Mobile-responsive design (While a technical constraint, advanced responsive features will be post-MVP)

### MVP Success Criteria

*   The chatbot provides accurate and helpful answers to at least 80% of HMSREG documentation questions.
*   User satisfaction rating of 4/5 or higher.
*   Average response time under 5 seconds for standard queries.
*   The chatbot successfully identifies and escalates questions it cannot answer with appropriate fallback options.

## 8. Post-MVP Vision

### Phase 2 Features

*   **Multi-language support:** Full support for both Norwegian and English.
*   **Interactive troubleshooting:** Guide users through a series of questions to solve their problems.
*   **Clarifying questions:** The chatbot will ask clarifying questions to better understand the user's role and context.

### Long-Term Vision

The long-term vision is to maintain the chatbot's focus on providing comprehensive and accurate information from the HMSREG documentation, without extending its scope to other parts of the system that may contain sensitive information.

## 9. Technical Considerations

The project will adhere to the technical architecture outlined in the `proposal.md` document. Key considerations include:

*   **Frontend:** Next.js, TypeScript, Tailwind CSS, shadcn/ui
*   **Backend:** Python, FastAPI, LangChain
*   **Vector DB:** ChromaDB
*   **Relational DB:** Supabase (PostgreSQL)
*   **AI:** Google Gemini 2.5 Pro, text-embedding-004
*   **Accessibility:** The application must comply with WCAG 2.2 standards.

## 10. Constraints and Assumptions

### Business Constraints

*   **Budget:** As a student project, the budget is minimal. The project will rely on free or low-cost tiers for all services.
*   **Timeline:** The project has a fixed 6-week timeline.
*   **AI Services:** The project will use low or free-tier AI services.

### Project Assumptions

*   The documentation on `docs.hmsreg.com` is accurate and up-to-date.
*   Users will be willing to use a chatbot to find information.

### Technical Assumptions

*   We will be able to scrape the documentation website without any issues. A fallback plan for manual data collection is in place if this assumption proves false.

## 11. Risks

### Project Risks

*   The 6-week timeline is very tight, and any unexpected technical challenges could cause delays, which is critical for a student project with a fixed deadline.

### Product Risks

*   There is a risk that the chatbot's accuracy will be too low to be useful, which could lead to low user adoption.

## 12. Open Questions

*   None at this time.
