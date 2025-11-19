# Technical Research Report: Pydantic AI vs. LangChain for HMSREG Chatbot

**Date:** Saturday, 15 November 2025
**Author:** Mary (Business Analyst Agent)
**Project:** HMSREG Documentation Chatbot
**User Skill Level:** Beginner

## 1. Executive Summary

This report evaluates Pydantic AI as an alternative to LangChain for implementing the Retrieval-Augmented Generation (RAG) pipeline within the HMSREG Documentation Chatbot. While LangChain offers a comprehensive, all-in-one framework for RAG, Pydantic AI excels in ensuring structured and type-safe interactions with Large Language Models (LLMs).

Our analysis concludes that Pydantic AI is not a direct, drop-in replacement for the entire RAG pipeline that LangChain provides. Instead, Pydantic AI is highly complementary, offering significant benefits in the LLM generation phase by enforcing structured output. To fully replace LangChain, a Pydantic AI-based solution would require manual implementation or integration of other libraries for document loading, chunking, embedding, and vector database retrieval.

Given the project's emphasis on structured, citable answers and the desire for granular control, a hybrid approach or a Pydantic AI-centric solution (where RAG components are built using other Python libraries) is feasible. The primary advantage of Pydantic AI in this context is the enhanced reliability and predictability of LLM responses, crucial for a production-grade chatbot.

## 2. Requirements and Constraints (for RAG Pipeline)

Based on the HMSREG Documentation Chatbot proposal and our discussions, the key requirements and constraints for the RAG pipeline component are:

### Functional Requirements

*   Process incoming user questions.
*   Retrieve relevant document chunks from a vector database (ChromaDB).
*   Generate a final, user-facing answer using an LLM (Google Gemini 2.5 Pro).
*   Include source citations in the final answer.
*   Handle both Norwegian and English languages.
*   Be able to handle multi-turn conversations, remembering the user's role.

### Non-Functional Requirements

*   **Performance:** Average response time should be under 5 seconds.
*   **Scalability:** Must handle at least 10 requests per minute and 50 per hour, with potential for more.
*   **Maintainability:** The code should be clear and easy to update, especially the RAG pipeline and prompts.
*   **Developer Experience:** Should integrate well with FastAPI and have good, clear documentation.

### Constraints

*   **Programming Language:** Python 3.11+
*   **Backend Framework:** FastAPI
*   **Vector Database:** ChromaDB
*   **LLM:** Google Gemini 2.5 Pro (or compatible)
*   **Cost:** Keep costs low, leveraging free tiers where possible.
*   **Licensing:** Open-source libraries are preferred.

## 3. Technology Options: LangChain vs. Pydantic AI

### 3.1. LangChain

**Overview:**
LangChain is a comprehensive framework designed to simplify the development of applications powered by large language models. It provides a modular and extensible toolkit for building complex LLM workflows, particularly excelling in Retrieval-Augmented Generation (RAG).

**Key Features:**
*   **Document Loaders:** Integrations with various data sources (web pages, PDFs, databases).
*   **Text Splitters:** Tools to break down large documents into smaller, manageable chunks.
*   **Embeddings:** Integrations with various embedding models (e.g., Google's `text-embedding-004`).
*   **Vector Stores:** Wrappers for popular vector databases (e.g., ChromaDB).
*   **Chains & Agents:** High-level abstractions to orchestrate complex sequences of LLM calls, tool usage, and data processing.
*   **RAG Specific Components:** Dedicated components for building and managing RAG pipelines.

**Pros:**
*   **Rapid Development:** Offers high-level abstractions that allow for quick prototyping and deployment of RAG pipelines with minimal code.
*   **All-in-One Solution:** Provides a complete ecosystem for all stages of RAG (indexing, retrieval, generation).
*   **Extensive Integrations:** Broad support for various LLMs, vector stores, and data sources.

**Cons:**
*   **Abstraction Overhead:** Can sometimes obscure the underlying logic, making deep customization or debugging challenging.
*   **Framework Lock-in:** While flexible, deviating significantly from its patterns can be cumbersome.
*   **Learning Curve:** Can be complex to master for advanced use cases due to its extensive API and concepts.

### 3.2. Pydantic AI

**Overview:**
Pydantic AI is a Python agent framework built on top of Pydantic, designed to bring structure, type safety, and reliability to LLM applications. It focuses on defining and validating the inputs and outputs of LLM interactions, treating them as structured conversations.

**Key Features:**
*   **Structured Output Validation:** Leverages Pydantic models to guarantee that LLM responses conform to predefined, validated data schemas. This is its core strength.
*   **Function/Tool Calling:** Enables LLMs to reliably call Python functions (tools) during conversations, providing access to external data or computations.
*   **Type Safety:** Integrates Python's type hinting for robust and maintainable AI agent development.
*   **LLM Agnostic:** Supports various LLM providers (OpenAI, Anthropic, Gemini, etc.) through `instructor`.

**Pros:**
*   **Predictable LLM Output:** Ensures LLM responses are always in the expected format, critical for downstream processing and API reliability.
*   **Reduced Hallucinations (Structured):** By forcing a structure, it can indirectly reduce certain types of hallucinations related to formatting or missing required fields.
*   **Pythonic & Transparent:** Feels more like writing standard Python code, offering greater control and clarity over LLM interactions.
*   **Excellent for API Integration:** Naturally fits into FastAPI-based backends due to its Pydantic foundation.

**Cons:**
*   **Not a Full RAG Framework:** Pydantic AI does not natively provide components for document loading, text splitting, or direct vector store management. These "R" and "A" parts of RAG must be implemented using other libraries (e.g., `requests`, `BeautifulSoup`, `langchain_text_splitters`, `chromadb` client).
*   **More Manual Orchestration:** Requires more manual coding to set up the entire RAG pipeline compared to LangChain's higher-level abstractions.

## 4. Comparative Analysis

| Feature/Aspect           | LangChain                                                              | Pydantic AI (with supporting libraries)                               |
| :----------------------- | :--------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| **Primary Focus**        | End-to-end LLM application development, especially RAG                 | Structured, type-safe LLM interactions and agent orchestration        |
| **RAG Pipeline Support** | Comprehensive (loaders, splitters, embeddings, vector stores, chains)  | Requires external libraries for data loading, chunking, embedding, retrieval |
| **Structured Output**    | Achievable, but often requires more manual parsing/validation          | Core strength; enforces output schema via Pydantic models             |
| **Control & Flexibility**| High-level abstractions, can be less flexible for deep customization   | More granular control over each step, highly flexible                 |
| **Developer Experience** | Rapid prototyping, but can have a steeper learning curve for advanced use | Pythonic, familiar for Pydantic/FastAPI users, clear data flow        |
| **Integration with FastAPI** | Good, but might require adapting LangChain's patterns to FastAPI's API design | Excellent, native fit due to shared Pydantic foundation               |
| **Suitability for HMSREG Chatbot** | Quick to set up initial RAG, but might need custom validation for specific output formats | Requires more initial setup for RAG, but ensures highly reliable and structured answers, ideal for factual chatbots |

## 5. Trade-offs and Decision Factors

**Trade-offs:**

*   **Development Speed vs. Control/Reliability:** LangChain offers faster initial RAG setup but with less granular control. Pydantic AI requires more manual RAG component assembly but provides superior control and reliability for LLM output.
*   **Framework Abstraction vs. Pythonic Code:** LangChain's abstractions can hide complexity but also limit transparency. Pydantic AI promotes more explicit, Pythonic code, which can be easier to debug and maintain for specific, critical data flows.

**Decision Factors (Weighted by Project Needs):**

1.  **Structured, Citable Answers (High Priority):** The HMSREG chatbot requires accurate, citable, and consistently formatted answers. Pydantic AI's core strength in structured output validation directly addresses this.
2.  **Maintainability & Transparency (High Priority):** Given the need for clear, auditable responses in a critical domain, explicit control over the RAG pipeline and LLM output is valuable.
3.  **Integration with FastAPI (High Priority):** Pydantic AI's native compatibility with Pydantic makes it a seamless fit for the chosen backend framework.
4.  **Development Effort (Medium Priority):** While Pydantic AI requires more manual setup for RAG components, the clarity and reliability gained might offset the initial effort.

## 6. Real-World Evidence

*   **LangChain:** Widely adopted as a standard for RAG, with a large community and numerous production examples. Its strength lies in its comprehensive ecosystem.
*   **Pydantic AI:** Gaining traction for applications requiring high reliability and structured data extraction from LLMs. Often used in scenarios where LLM output needs to be consumed by other systems or APIs, similar to the HMSREG chatbot's need for structured, citable responses.

## 7. Recommendations

Given your project's emphasis on **structured, citable, and reliable answers** for a production-grade documentation chatbot, and your existing FastAPI backend, I recommend the following:

**Option A: Pydantic AI-Centric RAG (Recommended)**

*   **Approach:** Implement the RAG pipeline by combining Pydantic AI for LLM interaction and structured output, with other Python libraries for data loading, chunking, embedding, and ChromaDB retrieval.
*   **Rationale:** This approach directly addresses the critical need for predictable and validated LLM responses, which is a core requirement for your chatbot. It leverages Pydantic AI's strengths in type safety and structured output, which aligns perfectly with your FastAPI backend. While it requires more manual orchestration for the "R" and "A" parts of RAG, the increased control and transparency will lead to a more robust and maintainable system for a factual chatbot.
*   **Benefits:**
    *   Guaranteed structured output for answers and citations.
    *   High reliability and reduced parsing errors.
    *   Excellent integration with FastAPI.
    *   More explicit control over the RAG process.
*   **Considerations:** Requires more custom code for document processing and retrieval compared to LangChain.

**Option B: Hybrid Approach (LangChain + Pydantic AI)**

*   **Approach:** Use LangChain for the initial RAG pipeline (document loading, chunking, embedding, retrieval) and then integrate Pydantic AI (via `instructor`) specifically for the final LLM generation step to enforce structured output.
*   **Rationale:** This leverages LangChain's rapid RAG setup while still gaining the benefits of Pydantic AI's structured output.
*   **Benefits:** Faster initial RAG setup. Structured output for the final answer.
*   **Considerations:** Might introduce some complexity in integrating two frameworks, potentially leading to a larger dependency footprint.

**Decision:** For the HMSREG Chatbot, where the accuracy and structured nature of the output are paramount, **Option A (Pydantic AI-Centric RAG)** is the stronger recommendation. It provides a cleaner, more Pythonic solution that aligns well with your existing FastAPI/Pydantic stack, even if it means slightly more initial development for the retrieval components.

## 8. Architecture Decision Record (ADR) Template

```markdown
# ADR-XXX: [Decision Title]

## Status

[Proposed | Accepted | Superseded]

## Context

The HMSREG Documentation Chatbot requires a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, citable answers based on official documentation. The initial proposal suggested LangChain. This ADR evaluates replacing LangChain with a Pydantic AI-centric approach.

## Decision Drivers

*   **Criticality of Structured Output:** The chatbot must provide consistently formatted answers with clear citations.
*   **Maintainability and Transparency:** Desire for explicit control over the RAG process and LLM interactions.
*   **Integration with Existing Stack:** Strong preference for solutions that integrate natively with Python 3.11+, FastAPI, and Pydantic.
*   **Cost-Effectiveness:** Leverage free tiers and open-source solutions where possible.

## Considered Options

1.  **LangChain (Original Proposal):** Comprehensive RAG framework.
2.  **Pydantic AI-Centric RAG:** Build RAG components with standard Python libraries and use Pydantic AI for structured LLM interaction.
3.  **Hybrid (LangChain + Pydantic AI):** Use LangChain for retrieval, Pydantic AI for structured generation.

## Decision

[Chosen option and rationale]

## Consequences

**Positive:**

*   Highly reliable and predictable LLM output due to Pydantic validation.
*   Clean, Pythonic codebase that integrates seamlessly with FastAPI.
*   Greater control and transparency over each stage of the RAG pipeline.

**Negative:**

*   Requires more manual implementation for document loading, chunking, embedding, and vector retrieval compared to LangChain's abstractions.
*   Potentially longer initial development time for the RAG pipeline setup.

**Neutral:**

*   Continued use of ChromaDB and Google Gemini 2.5 Pro.

## Implementation Notes

*   Utilize `requests` and `BeautifulSoup` for web scraping.
*   Employ `langchain_text_splitters` for document chunking.
*   Use `chromadb` client with `GoogleGenerativeAiEmbeddingFunction` for embeddings and vector storage.
*   Leverage `instructor` to patch the OpenAI client for structured Pydantic AI responses.

## References

*   HMSREG Documentation Chatbot Proposal (`proposal.md`)
*   Pydantic AI Documentation
*   LangChain Documentation
*   ChromaDB Documentation
*   Google AI Documentation (Gemini, Embedding models)
```

## 9. Next Steps

1.  **Review the `rag_with_pydantic.py` script:** This script provides a working example of the Pydantic AI-centric RAG pipeline.
2.  **Decision on Approach:** Confirm whether to proceed with the Pydantic AI-centric RAG (Option A) or the Hybrid Approach (Option B).
3.  **Refine Data Ingestion:** Develop a more robust data ingestion strategy to scrape all relevant documentation pages from `docs.hmsreg.com`, as outlined in your proposal.
4.  **Integrate into FastAPI:** Begin integrating the Pydantic AI-centric RAG logic into your FastAPI backend.

---
**Report End**
