# Lana-KI / Carpuncle Cloud

## Executive-Projektbeschreibung (ausführlich)
**Lana-KI** ist die lokale KI-Operationsplattform von **Thomas Heckhoff**. Sie steuert ein verteiltes Multi-Node-System, priorisiert lokalen Compute und setzt Cloud-Ressourcen nur gezielt für Burst/Experimente ein.

## 1) Einordnung
Lana-KI soll gleichzeitig auf mehreren Servern agieren, um Aufgaben automatisiert zu erledigen:
- Dateien/Programme erzeugen, aktualisieren, korrigieren
- Endpunkte prüfen, erstellen, reparieren
- Services überwachen (Ports, Prozesse, Logs, Health)
- API-basierte Expertenmodelle als Beratungsschicht einbinden
- Mehrere KI-Bots parallel zur Lösungsfindung nutzen

**Betriebsgrenze:** Kein unkontrollierter „All-Access-Modus“. Schreibzugriffe erfolgen policy-gesteuert, nachvollziehbar und auditpflichtig.

---

## 2) Feste Architekturentscheidung
- **RTX Desktop** = Primary Compute / Primary Inference / Main Orchestrator
- **RunPod** = elastisches Burst-Backend (nicht primär)
- **Hetzner Node A** = Public Edge / API / Gateway / Coordination
- **GCP** = experimentell / isoliert
- **NAS/FritzBox** = Vault / Restore / Backup / VPN-Kontext
- **Laptop** = Admin-/Audit-Hub

### Architekturfluss
```text
Internet
  -> Cloudflare Proxy
    -> gateway.lana-ki.de
      -> Hetzner Node A (Ingress, API, MCP, Routing)
        -> RTX Desktop (LM Studio + ComfyUI + Agent Runtime)
        -> RunPod (Burst GPU Worker)
        -> GCP (Experimental Worker)
      -> NAS/Vault (Backups, Restore, Audit-Archive)
```

---

## 3) Verzeichnis- und Pfadmodell (Windows)
- **Projekt (non-git):** `C:\Carpuncle Cloud\Lana KI`
- **Git-Doku/Audit:** `C:\Carpuncle Cloud\Lana KI\Lana Git`
- **Userordner:** `C:\Carpuncle Cloud\carpuncle.V6`
- **Root-ENV:** `C:\Carpuncle Cloud\.env`
- **Portable Tools:** `C:\Carpuncle Cloud\Tools`

---

## 4) Rollenmodell je Node
### Node A — Hetzner Edge
**Aufgaben:** Cloudflare Tunnel, Reverse Proxy, API Routing, MCP Gateway, OAuth Redirects, Webhook Intake, Queue Coordination, Monitoring/Healthchecks.  
**Nicht Aufgaben:** Primäre LLM-Inferenz, schwere GPU-Jobs, Haupt-Secret-Speicher, Primärdatenhaltung.

### Node B — RTX Desktop (PRIMARY)
Primary Inference, ComfyUI, LM Studio API, Main Orchestration, FastAPI local, Agent Runtime, Development.

### Node C — NAS/Vault
Backup, Restore, Cold Storage, Audit-Archive, Secret-Referenzablage.

### Node D — Laptop
Admin-Steuerung, Emergency Control, Monitoring, Read-only Audit.

### Node E — GCP
Temporary/Experimental Workloads.

### Node F — RunPod
Burst GPU, Batch Jobs, Training, Fallback Rendering.

---

## 5) Betriebsprinzipien
1. Lokal zuerst (RTX ist führend).
2. Edge trennt Ingress von Compute.
3. Secrets niemals im Klartext in Doku/Logs/Chat.
4. Jede Änderung wird automatisch protokolliert.
5. Kein Super-Agent; stattdessen capability-scoped Agenten.
6. Read/Write-Trennung für sichere Automatisierung.

---

## 6) Priorisierte Implementierungsreihenfolge
1. RTX Desktop stabilisieren
2. State/Vault lokal absichern
3. Hetzner Node A härten
4. Cloudflare-Limits/Ingress sauber setzen
5. Secret-Rotation etablieren
6. Audit-Pipeline automatisieren
7. RunPod Burst integrieren
8. GCP später ausbauen

---

## 7) Projektdokumente
- `README.md` — Executive-Projektbeschreibung
- `LANA_SYSTEM_BASELINE.md` — Technische Baseline
- `Lana_Notizbuch.md` — Automatische Protokollierung, Loop, SharePoint/GitHub-Export
