# Brainstorming Session Results

**Date:** 2025-10-31
**Agent:** Mary, Business Analyst
**User:** BIP
**Techniques Used:** Mind Mapping, User Story Mapping

---

## 1. Mind Map

*   **Central Topic:** Core Features and User Flows
    *   **Primary Goal:** Find information quickly and easily without IT support.
        *   **Information Types:**
            *   Documentation Requirements (for workers, projects)
            *   Certificates (how to upload, what's required)
            *   HMS Cards (validity, renewal process, troubleshooting)
            *   System Procedures (workforce registration, check-in/out)
            *   Project Status (for managers: deviations, documentation overview)
    *   **User: Subcontractor**
        *   **Crew Management:**
            *   Add crew
            *   Edit crew information
        *   **User Management:**
            *   Invite colleagues
            *   Invite their own subcontractors
        *   **Compliance:**
            *   Upload documents for audits
    *   **User: Construction Worker**
        *   **Safety & Compliance:**
            *   Access and complete safety checklists
            *   View work permits
            *   Check HMS card validity
        *   **Site Access:**
            *   Understand check-in/out procedures
    *   **User: Project Manager**
        *   **Project Overview:** Get a high-level view of status, deviations, and documentation.
        *   **(Similar to Subcontractor):** Crew, User, and Compliance management.
    *   **User Flow: Worker Check-in Failure**
        1.  Arrives at site.
        2.  Scans QR code to check in.
        3.  **Check-in Fails** (Error: "Invalid HMS Card").
        4.  Opens Chatbot.
        5.  Asks chatbot for help.
        6.  Chatbot diagnoses the problem.
        7.  Chatbot provides a step-by-step solution (e.g., renewal link).
        8.  Worker resolves the issue.
        9.  Worker successfully checks in later.

---

## 2. User Story Map

*   **Backbone:** `Discover` -> `Learn` -> `Use` -> `Get Help` -> `Resolve`
*   **Stories:**
    *   **Discover:** User sees the chatbot icon on the HMSREG page.
    *   **Learn:** Receives a welcome message, sees quick links for common questions, and views "What do I do if..." scenarios.
    *   **Use:** Asks a specific question and gets a direct answer.
    *   **Get Help:** Receives links to specific documentation or is advised to restart the session if stuck.
    *   **Resolve:** The user's issue is solved, or for complex problems, they are referred to IT support.

---
