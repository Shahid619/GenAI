# AI Content Publisher

Automatically generate **unique, professional articles** about AI and Generative AI, and publish them directly to a **GitHub repository**. No templates — every article is dynamically composed with fresh hooks, structures, and analysis.

## Features

- **Unique content every time** — dynamically composed from multiple writing styles, structures, and analytical frameworks. Never repeats identical output.
- **Professional tone** — formal, analytical, industry-appropriate language throughout.
- **15+ AI topics** — RAG, AI Agents, Prompt Engineering, LoRA, SLMs, Multimodal AI, AI Safety, Vector Databases, MLOps, Open Source AI, Synthetic Data, AI Code Generation, AI Regulation, Edge AI, Enterprise AI.
- **3 writing styles** — Educational (concept explainers), Trends (industry analysis), Practical (best practices).
- **One-command publishing** — generates content, commits, and pushes to your GitHub repository.
- **No credentials stored** — prompts interactively or uses optional `.env` file.

## Quick Start

### 1. Install Dependencies

```bash
cd ai-content-publisher
pip install -r requirements.txt
```

### 2. Get a GitHub Personal Access Token

You need a token with **`repo`** scope to push to your repository.

1. Go to: **https://github.com/settings/tokens**
2. Click **Generate new token → Tokens (classic)**
3. Give it a name (e.g., `content-publisher`)
4. ✅ Check the **`repo`** scope (Full control of private repositories)
5. Click **Generate token** and **copy it** (you won't see it again)

### 3. Run

```bash
python main.py publish
```

You will be prompted for:
- Your GitHub token
- Your GitHub username
- Your repository name

The tool will:
1. Generate a unique article
2. Show you a preview
3. Clone your repository
4. Commit and push the article
5. Clean up temporary files

## Configuration (Optional)

If you prefer not to enter credentials every time, create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your_username
GITHUB_REPO=your_repo_name
```

When `.env` is configured, the tool runs without prompts.

## Commands

| Command | Description |
|---------|-------------|
| `python main.py publish` | Generate & publish (random topic) |
| `python main.py publish --style educational` | Specific style (educational / trends / practical) |
| `python main.py publish --topic "RAG"` | Specific topic keyword |
| `python main.py history` | View publishing history |

## Topics Covered

| Category | Topics |
|----------|--------|
| **Educational** | RAG, Fine-Tuning (LoRA), AI Safety, Synthetic Data |
| **Trends** | AI Agents, SLMs, Multimodal AI, Open Source AI, AI Regulation, Edge AI, Enterprise AI |
| **Practical** | Prompt Engineering, Vector Databases, MLOps, AI Code Generation |

Each topic has rich metadata: key points, industry context, statistics, and future outlook — ensuring depth and variety in every article.

## How It Works

```
┌─────────────────────┐
│  Content Generator   │  ← Dynamic composition (no templates)
│  • 4 hook types      │
│  • 5 body structures │
│  • 7 closing styles  │
│  • Rotating hashtags │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Markdown Article    │  ← Formatted with title, body, tags
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  GitHub Publisher    │  ← Clone → Add → Commit → Push
│  • Token-based auth  │
│  • Auto-cleanup      │
└─────────────────────┘
```

## Project Structure

```
ai-content-publisher/
├── main.py                 # CLI entry point
├── generator.py            # Dynamic unique content composer
├── publisher.py            # GitHub repository publisher
├── .env.example            # Credentials template (copy to .env)
├── requirements.txt        # Python dependencies
├── published.json          # Publishing log (auto-created)
├── _repo_work/             # Temporary repo clone (auto-created & deleted)
└── README.md               # This file
```

## Publishing History

Every published article is logged in `published.json`:

```json
{
  "published_at": "2026-04-03T12:00:00",
  "title": "Retrieval-Augmented Generation (RAG)",
  "style": "educational",
  "filename": "retrieval-augmented-generation-rag.md",
  "repo": "username/GenAI",
  "success": true
}
```

## Important Notes

- **No credentials are committed** — `.env` is gitignored
- **Token is used only for git operations** — never stored in commits or logs
- **Local repo is cleaned up** after each publish
- **Articles are unique** — dynamic composition ensures no two outputs are identical
- **Review before publishing** — preview is shown before credentials are requested
