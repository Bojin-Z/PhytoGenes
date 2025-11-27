# PhytoGenes - Plant Gene Knowledge Intelligent Retrieval Agent

[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
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
```mermaid
graph TD
    %% Global Styles
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef terminator fill:#eeeeee,stroke:#616161,stroke-width:2px;
    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px,stroke-dasharray: 5 5;
    classDef db fill:#e0e0e0,stroke:#333,stroke-width:2px,shape:cylinder;

    Start((Start)):::terminator
    End(((End Process))):::terminator

    %% Module 1
    subgraph M1 [3.1 Module 1: Input Preprocessing & Intent Recognition]
        direction TB
        Input[Receive User Natural Language Input]:::process
        CheckGene{LLM Validation:<br/>Contains Valid Gene Name?}:::decision
        ErrorInput[Return Error Hint:<br/>Invalid Input]:::error
        Extract[Entity Extraction:<br/>Gene Name + Species Name]:::process
    end

    %% Module 2
    subgraph M2 [3.2 Module 2: Intelligent Retrieval Routing]
        direction TB
        CheckSpecies{Is Species Name<br/>Extracted?}:::decision
        
        %% Right Branch: Specific Species
        MatchTool[LLM Match FastMCP Tool<br/>e.g., Arabidopsis_TAIR_MCP]:::process
        CallSpecific[Call Specific DB API<br/>+ Scholar_MCP with Species Keywords]:::process
        
        %% Left Branch: Broad Search
        CallAll[Parallel Call to All<br/>Registered DB MCPs]:::process
        CheckDBResult{Database Results<br/>Found?}:::decision
        
        %% Sub-branch: No DB Results
        ScholarFull[Google Scholar<br/>Full-Text Search]:::process
        CheckCount{Result Count > 100?}:::decision
        CircuitBreaker[Circuit Breaker:<br/>Too many results & no match<br/>Stop & Return Error]:::error
        
        %% Sub-branch: DB Results Found
        ScholarVerify[Google Scholar Secondary Verification<br/>Keywords: Result Species + User Gene Name]:::process
    end

    %% Module 3
    subgraph M3 [3.3 Module 3: Data Cleaning & Archiving]
        direction TB
        Aggregation[Data Aggregation:<br/>JSON / HTML / Text]:::process
        Schema[(Target DB Schema)]:::db
        LLMClean[LLM Cleaning & Mapping<br/>Based on Pydantic-AI Structured Output]:::process
        
        Classify{Data Classification<br/>Mapping}:::decision
        
        TabExp[Table_Expression]:::process
        TabFunc[Table_Function]:::process
        TabSeq[Table_Sequence]:::process
        
        Persist[Generate SQL/ORM Object<br/>Persist to Database]:::process
    end

    %% Connections
    Start --> Input
    Input --> CheckGene
    
    CheckGene -- No --> ErrorInput
    ErrorInput --> End
    
    CheckGene -- Yes --> Extract
    Extract --> CheckSpecies
    
    %% M2 Logic
    CheckSpecies -- Yes --> MatchTool
    MatchTool --> CallSpecific
    CallSpecific --> Aggregation
    
    CheckSpecies -- No --> CallAll
    CallAll --> CheckDBResult
    
    CheckDBResult -- Yes --> ScholarVerify
    ScholarVerify --> Aggregation
    
    CheckDBResult -- No --> ScholarFull
    ScholarFull --> CheckCount
    
    CheckCount -- Yes --> CircuitBreaker
    CircuitBreaker --> End
    CheckCount -- No --> Aggregation

    %% M3 Logic
    Aggregation --> LLMClean
    Schema --> LLMClean
    LLMClean --> Classify
    
    Classify --> TabExp
    Classify --> TabFunc
    Classify --> TabSeq
    
    TabExp --> Persist
    TabFunc --> Persist
    TabSeq --> Persist
    
    Persist --> End

    %% Styling for Subgraphs
    style M1 fill:#fffde7,stroke:#fbc02d,stroke-width:1px
    style M2 fill:#fffde7,stroke:#fbc02d,stroke-width:1px
    style M3 fill:#e8eaf6,stroke:#3f51b5,stroke-width:1px
```
### 2.3 Setup & Requirements
* OS: Linux recommended.

* Language: Python 3.10+.

* Database: MySQL 8.0+.

* API Keys Required:
    * LLM Provider (OpenAI / Anthropic / Google)
    * SerpApi (for Google Scholar)
    * ISP Proxy Service (for crawling)
