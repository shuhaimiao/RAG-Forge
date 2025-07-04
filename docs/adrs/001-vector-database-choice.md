# 1. Choice of Vector Database

**Status**: Accepted

**Date**: 2024-07-25

## Context and Problem Statement

For the initial Proof of Concept (PoC) of RAG-Forge, a vector database is required to store and search embeddings for the Retrieval-Augmented Generation (RAG) functionality. The current implementation uses Milvus.

However, the long-term vision for RAG-Forge is to evolve into a multi-tenant SaaS platform. This platform will need to store not only vector embeddings but also a significant amount of relational and transactional data, including:
- User accounts, authentication, and authorization.
- User sessions and chat conversation history.
- User-generated content like prompt libraries, projects, and artifacts.
- Structured document metadata (e.g., categories, sources, ownership).

The choice of database must balance the immediate needs of a PoC with the long-term requirements of scalability, maintainability, and architectural simplicity for a feature-rich application. We need to decide whether to continue with a specialized vector database (Milvus) or consolidate into a general-purpose database with vector capabilities (PostgreSQL + pgvector).

## Decision Drivers

*   **Architectural Simplicity**: Minimize the number of moving parts in the stack to reduce operational overhead.
*   **Developer Experience**: Enable rapid feature development by using a unified and familiar data model.
*   **Data Integrity**: Ensure transactional consistency between vector embeddings and their associated metadata and user data.
*   **Scalability**: The solution should be able_to scale from a PoC to a production SaaS application handling a growing number of users and documents.

## Considered Options

### 1. Milvus (Specialized Vector Database)

A purpose-built, open-source vector database designed for high-performance similarity search on massive datasets.

*   **Pros**:
    *   Potentially superior performance and scalability for billion-vector workloads.
    *   Rich feature set specifically for vector search (e.g., various index types, filtering).
*   **Cons**:
    *   High architectural complexity; requires external dependencies like `etcd` for metadata and `minio` for object storage.
    *   Requires a separate primary database (e.g., PostgreSQL) for relational data, leading to a complex, dual-database architecture.
    *   Queries that mix vector search with relational filtering (e.g., checking user permissions before searching) become complex, two-step operations that are difficult to keep atomic.

### 2. PostgreSQL with `pgvector` extension (General-Purpose Database)

A battle-tested, open-source relational database with a powerful extension (`pgvector`) that adds vector similarity search capabilities.

*   **Pros**:
    *   **Unified Architecture**: A single database stores all data—vectors, relational tables (users, projects), and even JSON documents. This dramatically simplifies deployment, management, backups, and security.
    *   **Rich Querying**: Allows for single, atomic queries that combine vector similarity search with standard SQL `WHERE` clauses. This is a massive advantage for building the intended SaaS features.
    *   **Excellent Ecosystem**: Leverages the mature and extensive tooling, libraries, and community knowledge of PostgreSQL.
    *   **Sufficient Performance**: `pgvector` with HNSW indexing provides excellent performance for millions of vectors, which is more than adequate for the foreseeable future of the platform.
*   **Cons**:
    *   May not achieve the same raw vector search throughput as Milvus at extreme scale (hundreds of millions or billions of vectors).

## Decision

We will adopt **PostgreSQL with the `pgvector` extension** as the primary and sole database for the RAG-Forge platform.

This decision prioritizes architectural simplicity and developer velocity. The ability to manage all application data in a single, transactionally-consistent system is a decisive advantage that directly supports the development of the planned SaaS features.

We will replace the existing Milvus, etcd, and minio services in our `docker-compose.yml` with a single PostgreSQL service configured with the `pgvector` extension.

## Consequences

*   **Positive**:
    *   The application stack will be significantly simplified, reducing operational complexity and cost.
    *   Development of new features will be faster and less error-prone due to the unified data model.
    *   The system will be easier to debug, test, and maintain.
*   **Negative**:
    *   If the platform grows to an extreme scale (billions of vectors), we may eventually need to migrate the vector search component to a specialized service. This is considered a "good problem to have" and a reasonable trade-off for the immediate and significant benefits of a unified architecture. 