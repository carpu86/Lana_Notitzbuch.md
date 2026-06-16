# LANA_SYSTEM_BASELINE

## Scope
Technische Baseline für:
- Arbeitsordner (non-git): `C:\Carpuncle Cloud\Lana KI`
- Git-Auditordner: `C:\Carpuncle Cloud\Lana KI\Lana Git`

## A) Systemrollen
- Primary Compute / Orchestrator: RTX Desktop
- Public Edge / Gateway: Hetzner Node A
- Burst Compute: RunPod
- Experimental: GCP
- Vault/Restore: NAS/FritzBox
- Admin/Audit: Laptop

## B) Pflichtendpunkte
- LM Studio API: `http://127.0.0.1:1234`
- ComfyUI API/UI: `http://127.0.0.1:8188`

## C) Multi-Agent-Regeln
- Mehrere spezialisierte Agenten statt Super-Agent
- Capability-Scopes je Agent (diagnose/build/patch/deploy/audit)
- Write-Operationen nur mit Policy + Logging
- Neue API-Modelle/Agenten onboarding-fähig, aber nur über kontrollierte Registrierung

## D) ENV- und Secret-Regeln
- Root `.env`: `C:\Carpuncle Cloud\.env`
- `.env` nie löschen, nie leeren, nie blind überschreiben
- Vor jeder Konfigänderung: Backup mit Timestamp
- Keine Secret-Ausgabe in Markdown, Logs, PRs, Chat
- Secret-Referenzen bevorzugen (z. B. `op://...`)

## E) Operations-Checks (PowerShell 7)
Vor Serviceeingriffen:
1. `Test-Path`
2. `Get-ChildItem`
3. `Get-NetTCPConnection`
4. `Get-CimInstance Win32_Process`
5. `Get-Content -Tail`
6. `Invoke-RestMethod`
7. `curl.exe`
8. `git status --short` (nur im Git-Ordner)

## F) Node-Constraints
### Hetzner Node A darf
- Ingress, Routing, OAuth, Webhooks, Healthchecks, Queue-Koordination

### Hetzner Node A darf nicht
- Primäre Inferenz
- Schwere GPU-Jobs
- Primärer Secretspeicher
- Langfristige Primärdatenhaltung

### RunPod darf
- Temporäre Worker, Burst GPU, Batch/Training

### RunPod darf nicht
- Zentrale Wahrheit, zentraler Secret-Store, permanenter MCP-Core

## G) Logging/Audit
- Primärjournal: `Lana_Notizbuch.md`
- Felder: UTC, Node, Scope, Root Cause, Fix, Commands, Result, Next Step, Secret-Check
- Weekly `LOOP_REPORT` mit Incidents, MTTR, Top Root Causes, Maßnahmen

## H) Git-Doku-Strategie (empfohlen)
```gitignore
# Secrets
.env
*.key
*.pem
*.pfx
*.ovpn
*.secret
Vault/secrets/**
Vault/private/**

# Runtime
node_modules/
venv/
__pycache__/
dist/
build/

# Cache
*.log
*.tmp

# Doku erlauben
!*.md
!docs/**
!runbooks/**
!audit/**
```
