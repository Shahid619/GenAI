# 🤖 Claude Code + Google Gemini (Free) — Windows Setup Guide

Run Claude Code for **free** using Google Gemini as the backend model via `claude-code-router`.
 
---

## 📋 Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher)
- A Google account
- PowerShell (comes with Windows)

---

## Step 1 — Get a Free Gemini API Key

1. Go to [aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)
2. Sign in with your Google account
3. Click **Create API Key**, select a project
4. Copy the generated key — you'll need it in Step 4

> ⚠️ Google's free tier has daily request limits. If you hit them, wait 24 hours or switch to a higher-limit model like `gemini-2.0-flash`.

---

## Step 2 — Install Claude Code + Router

Open PowerShell and run:

```powershell
npm install -g @anthropic-ai/claude-code @musistudio/claude-code-router
```

---

## Step 3 — Create Config Folders & File

Run each block in PowerShell one at a time:

**Create the folders:**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude-code-router"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"
```

**Create the config file:**
```powershell
$config = @'
{
  "LOG": true,
  "LOG_LEVEL": "info",
  "HOST": "127.0.0.1",
  "PORT": 3456,
  "API_TIMEOUT_MS": 600000,
  "Providers": [
    {
      "name": "gemini",
      "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/",
      "api_key": "$GOOGLE_API_KEY",
      "models": [
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash"
      ],
      "transformer": { "use": ["gemini"] }
    }
  ],
  "Router": {
    "default": "gemini,gemini-2.5-flash-lite",
    "background": "gemini,gemini-2.5-flash-lite",
    "think": "gemini,gemini-2.5-flash-lite",
    "longContext": "gemini,gemini-2.5-flash-lite",
    "longContextThreshold": 60000
  }
}
'@
$config | Out-File -FilePath "$env:USERPROFILE\.claude-code-router\config.json" -Encoding utf8
```

---

## Step 4 — Set Your Gemini API Key (Permanently)

Replace `your_actual_key_here` with the key you copied in Step 1:

```powershell
[System.Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", "your_actual_key_here", "User")
```

This saves the key permanently for your Windows user — no need to set it again after restart.

**Verify it's saved:**
```powershell
[System.Environment]::GetEnvironmentVariable("GOOGLE_API_KEY", "User")
```

---

## Step 5 — Run Claude Code

You need **two PowerShell windows** open at the same time.

**Terminal 1 — Start the router:**
```powershell
ccr start
```
Wait for: ✅ `Service started successfully`

**Terminal 2 — Start Claude Code:**
```powershell
ccr code
```

> 💡 **Tip:** Navigate to your project folder before running `ccr code`:
> ```powershell
> cd C:\Users\YourName\MyProject
> ccr code
> ```

---

## Step 6 — Test It

Inside Claude Code, type:
```
what files are in this directory?
```
If it reads your files and responds — **you're all set!** 🎉

---

## 🔁 Daily Usage

Every time you want to use Claude Code:

| Terminal | Command |
|----------|---------|
| Terminal 1 | `ccr start` |
| Terminal 2 | `ccr code` |

Keep Terminal 1 running in the background while you work.

---

## 🧠 Which Gemini Model to Use?

| Model | Best For |
|-------|----------|
| `gemini-2.0-flash` | Speed, higher free limits |
| `gemini-2.5-flash-lite` | Balanced quality + speed |
| `gemini-2.5-pro` | Complex tasks (lower free limits) |

To switch models, update the `"default"` field in your config file:
```
%USERPROFILE%\.claude-code-router\config.json
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ccr` not recognized | Re-run `npm install -g @musistudio/claude-code-router` |
| Port 3456 already in use | Change `"PORT": 3457` in `config.json` |
| API key not found | Run `echo $env:GOOGLE_API_KEY` to verify |
| Rate limit errors | Switch to `gemini-2.0-flash` in `config.json` |
| `mkdir -p` error in PowerShell | Use `New-Item` commands from Step 3 instead |

---

## 📁 Config File Location

```
C:\Users\YourName\.claude-code-router\config.json
```

---

## 🔗 Resources

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/overview)
- [claude-code-router on npm](https://www.npmjs.com/package/@musistudio/claude-code-router)
- [Google AI Studio (API Keys)](https://aistudio.google.com/api-keys)
- [Gemini Models Overview](https://ai.google.dev/gemini-api/docs/models)

---

*Guide based on Windows PowerShell setup. For macOS/Linux, use `export` for env variables and `mkdir -p` for folders.*
