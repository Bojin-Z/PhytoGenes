import os
from pathlib import Path

def create_structure():
    # 定义目录结构
    directories = [
        "data/logs",
        "data/raw_html",
        "src/config",
        "src/database",
        "src/mcp_servers",
        "src/infrastructure/crawler/strategies",
        "src/agent",
        "src/utils",
        "tests/unit",
        "tests/integration",
        "scripts",
    ]

    # 定义文件及其初始内容 (可选)
    files = {
        ".env": (
            "# Environment Variables\n"
            "DATABASE_URL=mysql+pymysql://user:password@localhost:3306/phytogenes\n"
            "OPENAI_API_KEY=sk-...\n"
            "SERPAPI_KEY=...\n"
            "LOG_LEVEL=INFO\n"
        ),
        ".gitignore": (
            "__pycache__/\n"
            "*.pyc\n"
            ".env\n"
            ".venv/\n"
            "venv/\n"
            ".idea/\n"
            ".vscode/\n"
            "*.log\n"
            "data/raw_html/*\n"
            "data/logs/*\n"
            "!data/raw_html/.gitkeep\n"
            "!data/logs/.gitkeep\n"
            "*.DS_Store\n"
        ),
        "pyproject.toml": (
            "[project]\n"
            "name = \"phytogenes\"\n"
            "version = \"0.1.0\"\n"
            "description = \"Plant Genes Knowledge Agent based on Pydantic-AI and FastMCP\"\n"
            "authors = [{name = \"Bojin-Z\", email = \"your.email@example.com\"}]\n"
            "requires-python = \">=3.10\"\n\n"
            "[build-system]\n"
            "requires = [\"poetry-core\"]\n"
            "build-backend = \"poetry.core.masonry.api\"\n"
        ),
        "README.md": "# PhytoGenes - 植物基因知识智能检索 Agent\n\n项目负责人：赵博今\n",
        "docker-compose.yml": (
            "version: '3.8'\n"
            "services:\n"
            "  db:\n"
            "    image: mysql:8.0\n"
            "    environment:\n"
            "      MYSQL_ROOT_PASSWORD: root\n"
            "      MYSQL_DATABASE: phytogenes\n"
            "    ports:\n"
            "      - \"3306:3306\"\n"
        ),
        
        # Src - Config
        "src/__init__.py": "",
        "src/config/__init__.py": "",
        "src/config/settings.py": "# Global configuration settings\n",
        "src/config/logging.py": "# Logging configuration\n",

        # Src - Database
        "src/database/__init__.py": "",
        "src/database/connection.py": "# SQLAlchemy Async Engine setup\n",
        "src/database/models.py": "# SQLAlchemy Table Definitions\n",
        "src/database/schemas.py": "# Pydantic Models for Data Validation\n",
        "src/database/crud.py": "# DB Operations\n",

        # Src - MCP Servers
        "src/mcp_servers/__init__.py": "",
        "src/mcp_servers/main_server.py": (
            "from fastmcp import FastMCP\n\n"
            "mcp = FastMCP(\"PhytoGenes Tools\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    mcp.run()\n"
        ),
        "src/mcp_servers/api_fetchers.py": "# Standard API logic (NCBI, etc.)\n",
        "src/mcp_servers/scholar.py": "# SerpApi encapsulation\n",
        "src/mcp_servers/web_scrapers.py": "# Web Scraper MCP Tools\n",

        # Src - Infrastructure
        "src/infrastructure/__init__.py": "",
        "src/infrastructure/crawler/__init__.py": "",
        "src/infrastructure/crawler/browser.py": "# Selenium / Fingerprint Browser Controller\n",
        "src/infrastructure/crawler/proxy.py": "# Proxy Pool Management\n",
        "src/infrastructure/crawler/parser.py": "# HTML Parsing Logic\n",
        "src/infrastructure/crawler/strategies/__init__.py": "",
        "src/infrastructure/crawler/strategies/tair.py": "# TAIR specific strategy\n",
        "src/infrastructure/crawler/strategies/generic.py": "# Generic fallback strategy\n",

        # Src - Agent
        "src/agent/__init__.py": "",
        "src/agent/core.py": "# Pydantic-AI Agent Definition\n",
        "src/agent/prompts.py": "# System Prompts\n",
        "src/agent/router.py": "# Explicit Routing Logic\n",
        "src/agent/workflow.py": "# Main Execution Workflow\n",

        # Src - Utils
        "src/utils/__init__.py": "",
        "src/utils/text_cleaner.py": "",
        "src/utils/validators.py": "",

        # Tests & Scripts
        "tests/__init__.py": "",
        "scripts/init_db.py": "# Script to initialize database tables\n",
        "scripts/run_agent.py": "# CLI Entry point\n",
    }

    base_path = Path(".")

    print(f"🚀 开始在 {base_path.resolve()} 初始化 PhytoGenes 项目结构...")

    # 1. 创建目录
    for dir_path in directories:
        full_path = base_path / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {dir_path}")
        else:
            print(f"⚠️ 目录已存在: {dir_path}")
    
    # 2. 创建 .gitkeep (防止空目录不被git提交)
    Path("data/logs/.gitkeep").touch()
    Path("data/raw_html/.gitkeep").touch()

    # 3. 创建文件
    for file_path, content in files.items():
        full_path = base_path / file_path
        if not full_path.exists():
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"📄 创建文件: {file_path}")
        else:
            print(f"⚠️ 文件已存在 (跳过): {file_path}")

    print("\n🎉 项目结构初始化完成！")
    print("下一步建议：")
    print("1. 运行 `pip install fastmcp pydantic-ai sqlalchemy pymysql python-dotenv`")
    print("2. 配置 .env 文件中的数据库连接和 API Key")

if __name__ == "__main__":
    create_structure()
