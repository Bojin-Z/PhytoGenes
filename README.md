# PhytoGenes - Plant Gene Knowledge Intelligent Retrieval Agent

[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Agent-Pydantic--AI-green)](https://github.com/pydantic/pydantic-ai)
[![Protocol](https://img.shields.io/badge/Protocol-FastMCP-orange)](https://github.com/punkpeye/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-grey)](LICENSE)
 
> **Yang Lab**: [https://yanglab.hzau.edu.cn/](https://yanglab.hzau.edu.cn/)

---

## 1. Project Background & Goals

### 1.1 Background
With the rapid growth of plant genomics data, information is not only scattered across heterogeneous sources but also faces complex legacy issues due to long research spans. The evolution of gene naming standards and the continuous iteration of functional understanding have resulted in datasets full of synonyms, old designations, and obsolete descriptions. This heterogeneity and fragmentation make it difficult for researchers to efficiently identify and unify data when facing massive amounts of unstructured information.

### 1.2 Goals
To build a vertical AI agent based on the **Pydantic-AI** framework and **FastMCP** protocol. The agent aims to achieve:

* **Automated Multi-Source Retrieval**:
    * **Standard API Integration**: Direct connections for open databases (NCBI, Uniprot) via dedicated MCP modules.
    * **Lightweight Static Scraping**: HTML parsing for unprotected webpages.
    * **High-Resistance Simulation Crawling**: Integrated fingerprint browsers, ISP proxies, and Selenium to mimic human behavior for commercial data sources with strict anti-scraping mechanisms (e.g., TAIR).
    * **Deep Academic Retrieval**: Integration of SerpApi to bypass Google Scholar restrictions, automating literature list acquisition and metadata extraction.
* **Intelligent Routing**: Dynamic selection of retrieval strategies based on user input (Species-specific vs. Broad search).
* **Structured Archiving**: Utilizing LLMs to clean dispersed unstructured information and map it to a standard relational database schema.

---

## 2. Technical Architecture

### 2.1 Core Tech Stack

* **Agent Framework**: **Pydantic-AI**
    * *Selection Logic*: After evaluating CrewAI, Mastra, Agno (too abstracted/black-box), and AutoGen/SmolAgents (too autonomous/hard to control), we chose **Pydantic-AI**. It provides a "transparent" architecture that relies on explicit routing logic rather than implicit automation magic. This significantly reduces debugging difficulty and ensures deterministic outputs suitable for rigorous scientific data.
* **Tool Protocol**: **FastMCP**
    * Used to decouple tool services from Agent logic, allowing for modular development of fetchers and scrapers.
* **LLM Base**: **GPT-5.1 / Claude 4.5 Opus / Gemini 3 Pro** (Targeting late 2025 SOTA models).
* **Data Storage**: **MySQL** (Relational Database).
    * *Key Tables*: `genes`, `gene_aliases`, `map_locations`, `gene_features`, `proteins`, `go_annotations`, `polymorphisms`, `germplasms`, `publications`.

### 2.2 System Modules

### 2.2 System Modules

```mermaid
graph TD
    User[User Input] --> Preprocess[Preprocess: Entity Extraction]
    Preprocess --> Router{Intelligent Router}
    
    subgraph Retrieval_Layer [FastMCP Servers]
        Router -- Specific Species --> SpecificDB[Species DB MCP]
        Router -- Generic Search --> BroadDB[Broad DB Search MCP]
        SpecificDB --> Scholar[Scholar MCP - Literature]
        BroadDB --> Scholar
        
        BroadDB -- No Results/Circuit Breaker --> Error[Return Error Hint]
    end
    
    subgraph Infrastructure [Infra Layer]
        SpecificDB -.-> Crawler[High-Resistance Crawler]
        Scholar -.-> SerpApi[SerpApi]
    end
    
    Retrieval_Layer --> Cleaner[Data Cleaning]
    Cleaner --> LLM[LLM Structured Mapping]
    LLM --> DB[(MySQL Database)]
    Cleaner --> LLM[LLM Structured Mapping]
    LLM --> DB[(MySQL Database)]
