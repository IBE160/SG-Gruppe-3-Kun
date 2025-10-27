# Technical Research Report: LangChain vs. Pydantic AI for RAG Chatbot

**Date:** 2025-10-27
**Prepared by:** Gemini
**Project Context:** Student project (IBE160) building a RAG chatbot with a 6-week timeline. Tech stack includes Python, FastAPI, ChromaDB, and Google Gemini models.

---

## Executive Summary

This report evaluates two primary Python frameworks, LangChain and Pydantic AI, for building a Retrieval-Augmented Generation (RAG) chatbot.

### Key Recommendation

**Primary Choice:** **LangChain**

**Rationale:** For this project, LangChain is the recommended framework. Its mature, extensive ecosystem and vast community resources present the lowest risk for a student project with a tight 6-week deadline. The availability of pre-built integrations for nearly all components of the RAG stack (document loaders, vector stores, LLMs) will significantly accelerate MVP development.

**Key Benefits:**

- **Reduced Development Time:** Comprehensive tooling and a massive library of integrations minimize the need for boilerplate code.
- **Abundant Learning Resources:** A large community provides extensive tutorials, documentation, and solutions to common problems.
- **Proven Track Record:** LangChain is the de facto industry standard for building LLM applications, making it a reliable and valuable tool to use.

---

## 1. Research Objectives

### Technical Question

To determine the most suitable Python framework (LangChain vs. Pydantic AI) for developing the backend of a RAG-based chatbot for the IBE160 project.

### Project Context

The project is a student-led initiative to build a documentation chatbot over a fixed 6-week period. The goal is to produce a functional MVP.

### Requirements and Constraints

#### Functional Requirements

- Ingest documentation from a web source.
- Implement a RAG pipeline (split, embed, store, retrieve).
- Integrate with FastAPI, ChromaDB, and Google Gemini models.

#### Non-Functional Requirements

- Rapid development is a priority.
- The framework should be well-documented and have strong community support.

#### Technical Constraints

- **Timeline:** 6 weeks.
- **Team Expertise:** Students, assumed to be learning these frameworks for the first time.
- **Tech Stack:** Python, FastAPI, ChromaDB.

---

## 2. Technology Options Evaluated

1.  **LangChain:** A comprehensive framework for developing applications powered by language models.
2.  **Pydantic AI:** A framework from the creators of Pydantic for building type-safe, testable, and production-ready AI agents.

---

## 3. Detailed Technology Profiles

### Option 1: LangChain

**Overview:**
LangChain is a mature and widely adopted framework designed to simplify the creation of applications using LLMs. It provides a modular architecture based on "chains" and a vast ecosystem of integrations.

**Pros:**
- **Massive Ecosystem:** Unmatched number of pre-built integrations for LLMs, vector databases (including ChromaDB), document loaders, and more.
- **Large Community:** Extensive tutorials, articles, and community support make it easy to find help and examples.
- **Comprehensive Tooling:** Covers the entire RAG lifecycle, from data ingestion to final output generation.
- **Flexible Composition:** The LangChain Expression Language (LCEL) offers a powerful way to compose and customize chains.

**Cons:**
- **High Abstraction & Complexity:** The framework's concepts (Chains, Agents, LCEL) can have a steep learning curve and add cognitive overhead.
- **API Instability:** The API evolves rapidly, which can lead to breaking changes between versions.
- **Verbosity:** Can sometimes require more code for simple tasks compared to more direct approaches.

### Option 2: Pydantic AI

**Overview:**
Pydantic AI is a newer framework focused on bringing modern software engineering best practices (type safety, validation, testing) to LLM application development. It is built by the team behind Pydantic and has ergonomics inspired by FastAPI.

**Pros:**
- **Type-Safe and Validated:** Enforces structured, validated data for LLM inputs and outputs, leading to more robust and predictable code.
- **Intuitive Ergonomics:** Uses FastAPI-style dependency injection, making it feel natural for Python web developers.
- **Excellent for Structured Output:** Its core strength is ensuring LLM outputs conform to a specific Pydantic model, eliminating messy parsing.
- **Good Observability:** Built with tracing and debugging in mind.

**Cons:**
- **Smaller Ecosystem:** Does not have the sheer breadth of integrations that LangChain offers. More custom code may be required.
- **Less Mature:** As a younger project, it has a smaller community and fewer learning resources compared to LangChain.
- **Agent-Focused:** While capable of RAG, its primary focus is on agentic workflows, and its RAG-specific tooling is less extensive than LangChain's.

---

## 4. Comparative Analysis

| Dimension | LangChain | Pydantic AI |
| :--- | :--- | :--- |
| **Ecosystem & Integrations** | 🟢 **Excellent** | 🟡 **Good** |
| **Community & Resources** | 🟢 **Excellent** | 🟡 **Good** |
| **Ease of Use (Beginner)** | 🟡 **Good** (many examples) | 🟡 **Good** (if familiar with FastAPI) |
| **Code Robustness** | 🟡 **Good** | 🟢 **Excellent** (due to Pydantic) |
| **Development Speed** | 🟢 **Excellent** (due to integrations) | 🟡 **Good** (may need more custom code) |
| **Maturity & Stability** | 🟡 **Good** (Mature but API changes) | 🟡 **Good** (Newer but more stable philosophy) |

---

## 5. Recommendations

**Top Recommendation: LangChain**

LangChain is the most pragmatic choice for this project's constraints. The 6-week timeline demands a framework that minimizes friction and provides the quickest path to a functional MVP. LangChain's vast library of integrations and extensive community support directly address this need. While it has a steeper learning curve in its abstractions, the abundance of tutorials mitigates this risk for a student team.

**Alternative Option: Pydantic AI**

Pydantic AI is a strong contender and represents a more modern approach to building LLM applications. If the development team had prior experience with it or a longer timeline, it could lead to a cleaner, more maintainable, and more robust codebase. It remains an excellent framework to watch and consider for future projects.

---

## 6. Architecture Decision Record (ADR)

# ADR-001: Choice of AI Application Framework

## Status

Accepted

## Context

The IBE160 chatbot project requires a backend Python framework to orchestrate a Retrieval-Augmented Generation (RAG) pipeline. This involves loading documents, managing a vector store (ChromaDB), and interacting with an LLM (Google Gemini). The project has a fixed 6-week timeline.

## Decision Drivers

- **Speed of Development:** The primary driver is the ability to deliver an MVP within the 6-week timeframe.
- **Availability of Learning Resources:** The framework must be accessible to students who may be learning it for the first time.
- **Integration with Existing Stack:** Must seamlessly integrate with FastAPI, ChromaDB, and Gemini.

## Considered Options

1.  **LangChain:** A mature, feature-rich framework with a large ecosystem.
2.  **Pydantic AI:** A modern, type-safe framework with FastAPI-style ergonomics.

## Decision

We will use **LangChain** for the initial development and MVP of the project.

**Rationale:** LangChain's comprehensive set of pre-built integrations and extensive community support directly translate to faster development velocity. For a time-constrained student project, this advantage outweighs the benefits of Pydantic AI's cleaner abstractions and type safety, which can be explored in post-MVP phases or future projects.

## Consequences

**Positive:**

- Reduced time to build the core RAG pipeline.
- Easy access to community support and tutorials for troubleshooting.
- The team will gain experience with the current industry-standard tool.

**Negative:**

- The codebase may become coupled to LangChain's abstractions, which can be complex.
- The project may be subject to breaking changes if LangChain's API evolves.
- May miss the benefits of Pydantic AI's compile-time validation and structured data enforcement.
