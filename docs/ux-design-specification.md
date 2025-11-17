# ibe160 UX Design Specification

_Created on Monday, 17 November 2025 by BIP_
_Generated using BMad Method - Create UX Design Workflow v1.0_

---

## Executive Summary

The HMSREG Documentation Chatbot is an AI-powered tool designed to provide quick, accurate, and role-based answers from official documentation. Its core vision is to empower users to self-serve, reduce support workload, improve user efficiency, and ensure information consistency. The primary users are construction workers on-site, needing fast, mobile-friendly help, with secondary users including suppliers, project managers, and admin/support personnel. The core experience is opening the website, typing a problem into the chatbot, and receiving a solution, aiming for an efficient and productive user feeling.

---

## 1. Design System Foundation

### 1.1 Design System Choice

**Chosen Design System:** shadcn/ui with Tailwind CSS

**Rationale:** This choice aligns perfectly with the project's technical stack (Next.js, Tailwind CSS). shadcn/ui provides a collection of highly customizable, accessible, and efficient components built on Radix UI primitives. It offers full control over the component code, allowing for precise adaptation to the HMSREG brand while leveraging pre-built, well-tested foundations. This approach ensures consistency, rapid development, and a high degree of flexibility.

---

## 2. Core User Experience

### 2.1 Defining Experience

**Defining Experience:** "It's like having an expert on HMSREG documentation you can talk to anytime."

This statement encapsulates the chatbot's core value proposition: providing immediate, expert-level assistance for complex documentation through a natural, conversational interface.

### 2.2 Novel UX Patterns

**Novel UX Pattern:** Conversational Simplification

**User Goal:** Get a quick, accurate answer to a complex documentation question without having to search manually.

**Trigger:** Click a chatbot button to open the chat interface.

**Interaction Flow:**
1.  User selects their role to set the context.
2.  User asks a question in natural language.
3.  The system provides a concise, relevant answer with a link to the official source document.

**Visual Feedback:** A clean, simple chat interface that feels responsive and professional.

**States:**
*   **Default:** Ready to receive a question.
*   **Loading:** A subtle indicator that the "expert" is "thinking."
*   **Success:** A clear, well-formatted answer appears quickly.
*   **Error:** A helpful message explaining the issue and providing a path to human support.

**Platform Considerations:** The layout will adapt for mobile, ensuring the input field and chat history are easy to read and use on a smaller screen.

**Accessibility:** The chat will be fully usable with a keyboard and screen reader.

**Inspiration:** General chatbot patterns (like Posten.no), but with a focus on expert-level, documentation-specific answers.

---

## 3. Visual Foundation

### 3.1 Color System

**Proposed Color Palette:**
*   **Primary Color (Main actions, key elements):** A deep, professional blue/teal (e.g., `#004D40` for light mode, a slightly desaturated version for dark mode).
*   **Secondary Color (Supporting actions, accents):** A brighter, but still professional, blue (e.g., `#00796B` for light mode, a complementary shade for dark mode).
*   **Success Color (Positive feedback):** A clear green (e.g., `#388E3C`).
*   **Warning Color (Cautionary messages):** An amber/orange (e.g., `#FFA000`).
*   **Error Color (Negative feedback, alerts):** A distinct red (e.g., `#D32F2F`).
*   **Neutral Grayscale (Background, text, borders):** A range of grays that provide good contrast for both light and dark modes.

**Typography System:**
A professional, clean, and highly readable sans-serif typeface will be used, aligning with the HMSREG brand and ensuring clear visual hierarchy for headings, body text, and other elements.

**Spacing and Layout Foundation:**
Leveraging Tailwind CSS, a consistent spacing system will be implemented, based on a predictable scale (e.g., multiples of 4px or 8px). This ensures harmonious spacing, responsiveness, and efficient application of styles.

**Interactive Visualizations:**

- Color Theme Explorer: [ux-color-themes.html](./ux-color-themes.html) (Conceptual)

---

## 4. Design Direction

### 4.1 Chosen Design Approach

**Chosen Design Direction:** Structured & Informative

**Description:** This approach balances direct answers with helpful context and navigation. The chat interface might have a subtle, collapsible sidebar or an expandable panel for "related topics," "session context" (like the selected role), or suggested follow-up questions. Answers are prominent, but supporting information is also clearly organized and accessible. Interaction includes standard text input, but also "quick-reply" buttons for common follow-up questions or to explore related topics. The visual weight is slightly denser than a purely minimalist approach, but still very clean and professional, with information organized into digestible blocks.

**Interactive Mockups:**

- Design Direction Showcase: [ux-design-directions.html](./ux-design-directions.html) (Conceptual)

---

## 5. User Journey Flows

### 5.1 Critical User Paths

**User Journey: Primary Information Retrieval**
**User Goal:** Get accurate information from HMSREG documentation.
**Approach:** Guided & Reassuring, with an emphasis on efficiency.

**Flow Steps:**

1.  **Entry Screen (Chatbot Closed)**
    *   **User sees:** A clear button on the website, perhaps labeled "Chat with HMSREG Expert" or a simple chat icon.
    *   **User does:** Clicks the button.
    *   **System responds:** The chatbot interface opens, typically as an overlay or a fixed panel.

2.  **Initial Chatbot Greeting & Role Selection**
    *   **User sees:**
        *   Chatbot: "Welcome to the HMSREG Assistant! To provide the most relevant information, please select your role:"
        *   Interactive buttons: `[Construction Worker]`, `[Supplier / Subcontractor]`, `[Project Manager / Admin]`
    *   **User does:** Clicks on their specific role (e.g., `[Construction Worker]`).
    *   **System responds:** The chatbot processes the selection and prepares the next message.

3.  **Role Confirmation & Prompt for Question**
    *   **User sees:**
        *   Chatbot: "Great! I'm ready to help from a [user's role] perspective. Just so you know, all my answers are based *only* on the official documentation found at `docs.hmsreg.com` to ensure accuracy. What can I help you with today?"
        *   Input field: Clearly visible, perhaps with a placeholder like "Type your question..."
    *   **User does:** Types their question (e.g., "Hvorfor feiler innsjekkingen min?") and presses Enter or clicks a "Send" button.
    *   **System responds:** A subtle "typing" or "thinking" indicator appears, reinforcing the "human-like" feedback.

4.  **Processing & Answer Display**
    *   **User sees:**
        *   Chatbot: Displays the concise and accurate answer to the question, tailored to the selected role.
        *   Links: Includes clear, clickable links to the specific source documentation on `docs.hmsreg.com`.
        *   Feedback: Simple `[👍 Helpful]` and `[👎 Not Helpful]` buttons below the answer.
    *   **User does:** Reads the answer, potentially clicks a source link for more detail, or provides feedback.
    *   **System responds:** (If feedback given) Records the feedback for analytics.

**Decision Points:**

*   **User clicks source link:** The relevant documentation page opens (either in a new tab or within the chatbot interface, depending on implementation).
*   **User provides feedback:** The feedback is recorded.

**Error States (Fallback Mechanism):**

*   **Chatbot cannot confidently answer:** If the chatbot's confidence score is low, it triggers the fallback.
    *   **User sees:**
        *   Chatbot: "Jeg fant ikke et klart svar i dokumentasjonen for dette spørsmålet. Kan du utdype spørsmålet? [Suggestions for rephrasing or common topics] 📚 Dokumentasjon: docs.hmsreg.com 💬 Support: support@hmsreg.no | Tlf: [nummer]"
    *   **User does:** Can rephrase their question, select a suggested topic, or choose to contact support.

**Success State:**

*   **Completion feedback:** The user receives the accurate information they were looking for, feeling efficient and productive.
*   **Next action:** The user can ask another question, explore the source documentation, or close the chatbot.

---

## 6. Component Library

### 6.1 Component Strategy

**Core Components (likely from shadcn/ui, customized with Tailwind):**
*   **Button:** For role selection, sending messages, feedback (thumbs up/down), and quick-reply suggestions.
*   **Input:** The text field where users type their questions.
*   **Dialog/Sheet:** To house the main chatbot interface (whether it's a pop-up or a fixed panel).
*   **Loading Indicator:** A subtle animation to show the chatbot is "thinking."
*   **Link:** For citing source documentation.
*   **Icon:** For visual cues (e.g., send icon, feedback icons).

**Custom Compositions (built using shadcn/ui primitives and Tailwind):**
*   **Chat Bubble/Message Display:** A unique composition that includes the message content, role-based styling, source links, and feedback buttons.
*   **Role Selection Component:** A specific layout of buttons for the initial role selection.

---

## 7. UX Pattern Decisions

### 7.1 Consistency Rules

**1. Button Hierarchy:**
*   **Primary Actions (like "Send"):** Solid background using our primary blue/teal color for high visibility.
*   **Secondary Actions (like suggested questions):** More subtle style, perhaps an outline or a lighter background.
*   **Destructive Actions (e.g., "End Chat"):** Distinct red color to signal caution.

**2. Feedback Patterns:**
*   **Success:** Subtle checkmark icon or a brief, polite message.
*   **Error:** Clear, inline message right below the input field.
*   **Loading:** Subtle "typing" or "thinking" indicator.

**3. Form Patterns:**
*   **Validation:** Input checked on "Send."
*   **Help Text:** Placeholder text in the input field.

**4. Modal Patterns:**
*   **Dismissal:** Users can close the chatbot by clicking outside of it or pressing the 'Escape' key.
*   **Focus:** When the chatbot opens, the cursor will automatically be in the text input field.

**5. Empty State Patterns:**
*   **First Use:** Initial greeting and role selection prompt.
*   **No Results:** The helpful fallback message.

**6. Search Patterns:**
*   **Trigger:** Manual (user clicks "Send" or presses 'Enter').
*   **Results Display:** Answer appears directly in the chat conversation.
*   **No Results:** The fallback message is shown.

---

## 8. Responsive Design & Accessibility

### 8.1 Responsive Strategy

**1. Desktop (Large Screens):**
*   **Layout:** Three-column layout:
    *   **Left Column:** Dedicated to navigation links (e.g., documentation table of contents).
    *   **Middle Column:** Displays the main article content.
    *   **Right Column:** Houses the chatbot interface.
*   **Usage of Space:** Efficiently uses extra screen real estate to provide context alongside the interactive chatbot.
*   **Navigation:** The left-hand navigation will be persistent and easily accessible.

**2. Mobile (Small Screens):**
*   **Layout:** Single-column layout, showing only one primary content area at a time.
*   **Switching Mechanism:** A **tabbed interface** at the bottom of the screen or a **segmented control** at the top will provide quick, direct access to switch between "Links," "Article," and "Chatbot."
*   **Content Adaptation:**
    *   When the "Chatbot" tab is active, the chatbot interface will take up the full screen.
    *   When the "Article" tab is active, the documentation content will be full screen.
    *   When the "Links" tab is active, the navigation links will be full screen.
*   **Touch Targets:** All interactive elements will have adequate touch target sizes.

### Accessibility Strategy:

**Compliance Target:** WCAG 2.1 AA standards.

**Key Requirements:**
*   **Color Contrast:** High contrast between text and background colors for both light and dark modes.
*   **Keyboard Navigation:** All interactive elements fully navigable and operable using only a keyboard.
*   **Focus Indicators:** Clear visual indicators for keyboard focus.
*   **ARIA Labels:** Meaningful ARIA labels for screen readers, especially for the chat interface.
*   **Form Labels:** Properly associated labels for any form elements.
*   **Error Identification:** Clear, descriptive error messages.

---

## 9. Implementation Guidance

### 9.1 Completion Summary

Excellent work, BIP! Your UX Design Specification for the HMSREG Documentation Chatbot is complete.

**What we created together:**

*   **Design System:** We've chosen **shadcn/ui with Tailwind CSS**, providing a highly customizable, accessible, and efficient foundation for development.
*   **Visual Foundation:** We've established a professional blue/teal color palette, a clear sans-serif typography system, and a consistent spacing strategy, all aligned with the HMSREG brand.
*   **Design Direction:** We're moving forward with a **Structured & Informative** approach, balancing direct answers with helpful context and navigation.
*   **User Journeys:** We've detailed the **Primary Information Retrieval** flow, ensuring an efficient, guided, and reassuring experience for users.
*   **UX Patterns:** We've defined consistent patterns for buttons, feedback, forms, modals, empty states, and search, ensuring a predictable and intuitive user experience.
*   **Responsive Strategy:** We've planned for a three-column desktop layout and a single-column mobile layout with an efficient tabbed switching mechanism, ensuring optimal usability across devices.
*   **Accessibility:** We've committed to **WCAG 2.1 AA compliance**, making the chatbot accessible to all users.

**Your Deliverables:**

*   **UX Design Document:** `docs/ux-design-specification.md`
*   **Interactive Color Themes:** (Conceptual) `ux-color-themes.html` - _This would be an interactive HTML file showing all color theme options explored, with live UI component examples._
*   **Design Direction Mockups:** (Conceptual) `ux-design-directions.html` - _This would be an interactive HTML file with 6-8 complete design approaches for key screens._

**What happens next:**
This comprehensive specification provides a clear roadmap for designers to create high-fidelity mockups and for developers to implement the chatbot with clear UX guidance and rationale. All your design decisions are documented with reasoning for future reference.

You've made thoughtful choices through visual collaboration that will create a great user experience. Ready for design refinement and implementation!

---

## Appendix

### Related Documents

- Product Requirements: `docs/PRD.md`
- Product Brief: `docs/product-brief-HMSREG-Documentation-Chatbot-15-11-2025.md`
- Brainstorming: `docs/brainstorming-session-results-Wednesday, 12 November 2025.md`

### Core Interactive Deliverables

This UX Design Specification was created through visual collaboration:

- **Color Theme Visualizer**: (Conceptual) `ux-color-themes.html`
  - Interactive HTML showing all color theme options explored
  - Live UI component examples in each theme
  - Side-by-side comparison and semantic color usage

- **Design Direction Mockups**: (Conceptual) `ux-design-directions.html`
  - Interactive HTML with 6-8 complete design approaches
  - Full-screen mockups of key screens
  - Design philosophy and rationale for each direction

### Optional Enhancement Deliverables

_This section will be populated if additional UX artifacts are generated through follow-up workflows._

<!-- Additional deliverables added here by other workflows -->

### Next Steps & Follow-up Workflows

This UX Design Specification can serve as input to:

- **Wireframe Generation Workflow** - Create detailed wireframes from user flows
- **Figma Design Workflow** - Generate Figma files via MCP integration
- **Interactive Prototype Workflow** - Build clickable HTML prototypes
- **Component Showcase Workflow** - Create interactive component library
- **AI Frontend Prompt Workflow** - Generate prompts for v0, Lovable, Bolt, etc.
- **Solution Architecture Workflow** - Define technical architecture with UX context

### Version History

| Date     | Version | Changes                         | Author        |
| -------- | ------- | ------------------------------- | ------------- |
| Monday, 17 November 2025 | 1.0     | Initial UX Design Specification | BIP |

---

_This UX Design Specification was created through collaborative design facilitation, not template generation. All decisions were made with user input and are documented with rationale._