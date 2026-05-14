# Lana Notizbuch – Master-Kontext für Lana-KI

Dieses Dokument ist die **einzige Quelle der Wahrheit** für die Lana-KI-Umgebung des Benutzers carpu86 / Carpuncle Cloud.  
Eine KI, die dieses Dokument liest, soll:
- verstehen, wo jede Komponente liegt,
- welche Umgebungsvariablen-Namen (keine Werte!) existieren,
- welche GitHub-Repos aktiv / archiviert sind,
- wie SSH und das Nutzerprofil dauerhaft eingerichtet sind,
- und sofort erkennen, wenn ein Setup-Schritt fehlt oder falsch ist.

---

## 0 · Sicherheitsregel (UNBEDINGT einhalten)

> **Niemals** in dieses Dokument oder das Repo eintragen:
> - API-Keys, Tokens, Passwörter, Client-Secrets
> - Private SSH-Schlüssel (Dateiinhalt)
> - `.env`-Dateiinhalte mit echten Werten
> - ZIP-Inhalte mit Credentials
>
> Erlaubt: Dateinamen, Pfade, Schlüssel-*Namen* (z.B. `OPENAI_API_KEY=`), Endpunkt-URLs ohne Auth-Parameter.

---

## 1 · GitHub-Repositories – Entscheidungsmatrix

| Status | Repository | Zweck |
|--------|-----------|-------|
| ✅ **MASTER** | `carpu86/Lana` | Alle aktuellen Lana-KI-Dokumentationen |
| 📋 **Doku-Brücke** | `carpu86/Lana_Notitzbuch.md` | Dieses Repo – Übergangsdokumentation bis Rename abgeschlossen |
| 🗄️ Archiv | `carpu86/Lana-ki` | Fehlversuch |
| 🗄️ Archiv | `carpu86/lana-ki.app` | Fehlversuch |
| 🗄️ Archiv | `carpu86/Lanaapp` | Fehlversuch |
| 🗄️ Archiv | `carpu86/lana-ki-1` | Fehlversuch |
| 🗄️ Archiv | `carpu86/xxx` | Fehlversuch |
| 🗄️ Archiv | `carpu86/lana-web` | Fehlversuch |
| 🗄️ Archiv | `carpu86/Google-oauth-apps-for-windows` | Fehlversuch |

**Zielzustand (nach Abschluss aller Migrationen):**
```
carpu86/Lana  →  carpuapi/lana
```
Erst nach Archivierung von `carpu86/Lana_Notitzbuch.md` durchführen, damit kein kaputtes Redirect bleibt.

---

## 2 · Lokale Umgebung – Basisstruktur

### 2.1 Persistentes Nutzerprofil

Da `C:\Windows` regelmäßig neu installiert wird und `C:\Users\` dann leer ist, gilt:

> **Alle Nutzer-Profile und zukünftige Einstellungen zeigen auf `C:\Carpuncle Cloud\carpuncle.V6`**

```
C:\Carpuncle Cloud\
├── carpuncle.V6\            ← Persistentes Profil (ALLE User)
│   └── .ssh\                ← SSH-Schlüssel (Übersicht → Abschnitt 2.2)
├── .env                     ← Globale Umgebungsvariablen (Werte NICHT committen!)
├── Lana KI\                 ← Hauptarbeitsverzeichnis (→ Abschnitt 3)
└── Tools\                   ← Portable Tools (→ Abschnitt 5)
```

**Setup-Prüfschritt für KI:**  
Wenn ein Skript `$HOME` oder `%USERPROFILE%` verwendet und damit **nicht** auf `C:\Carpuncle Cloud\carpuncle.V6` zeigt, ist die Umgebung falsch konfiguriert → Skript stoppen, Profil-Redirect reparieren.

### 2.2 SSH-Schlüssel-Inventar

Alle Schlüssel liegen unter `C:\Carpuncle Cloud\carpuncle.V6\.ssh\`.  
**Nur Dateinamen – kein Inhalt wird hier gespeichert.**

| Datei | Typ | Verwendung |
|-------|-----|-----------|
| `id_ed25519` + `.pub` | Ed25519 | Haupt-Identität GitHub / SSH |
| `id_rsa` + `.pub` | RSA (legacy) | Ältere Dienste |
| `carpuncle_laptop_key` + `.pub` | Ed25519 | Laptop-spezifisch |
| `id_cloud_vm` + `.pub` | Ed25519 | Cloud-VM Zugriff |
| `id_direct_cloud` | Ed25519 | Direktverbindung Cloud |
| `id_emergency` + `.pub` | Ed25519 | Notfallzugang |
| `lana_ki_deploy_ed25519` + `.pub` | Ed25519 | Lana-KI Deploy-Key |
| `google_compute_engine` + `.pub` + `.ppk` | Ed25519/RSA | GCP Compute Engine |
| `Carpuncle.ppk` | PuTTY-Format | PuTTY / WinSCP |
| `config` | SSH-Config | Host-Aliase und Defaults |
| `config.backup-*` | Backups | Verschiedene Backup-Stände |
| `authorized_keys` | Auth-Liste | Zugelassene Schlüssel für eingehende Verbindungen |
| `known_hosts` | Hostkeys | Bekannte SSH-Hosts |

**Wichtig für KI:** Wenn SSH-Verbindung schlägt fehl → zuerst prüfen ob `config` auf `C:\Carpuncle Cloud\carpuncle.V6\.ssh\config` zeigt, nicht auf `C:\Users\<user>\.ssh\`.

### 2.3 Globale `.env` – Schlüsselnamen-Übersicht

Datei: `C:\Carpuncle Cloud\.env`  
**Werte sind NICHT hier eingetragen.** Nur die Schlüsselnamen, damit eine KI weiß, welche Variablen vorhanden sind.

Erwartete Schlüsselnamen (auf Vollständigkeit prüfen):
```
OPENAI_API_KEY=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT=
GOOGLE_API_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
FIREWORKS_API_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=
GITHUB_TOKEN=
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ZONE_ID=
CLOUDFLARE_ACCOUNT_ID=
NODE_ENV=
LANA_ENV=
```

**KI-Prüfregel:** Wenn ein Dienst startet und einen fehlenden Key meldet → prüfen, ob der Key-Name in dieser Liste steht. Falls nicht vorhanden, als neuen Eintrag dokumentieren, **bevor** weiterer Code deployed wird.

---

## 3 · Lana KI – Hauptverzeichnis

```
C:\Carpuncle Cloud\Lana KI\
├── .vscode\                    ← VS-Code-Workspace-Einstellungen
├── _backups\                   ← Lokale Backup-Schnappschüsse
├── audit\                      ← Sicherheits- und Konfigurations-Audits
├── config\                     ← Konfigurationsdateien (keine Secrets committen)
├── docs\
│   └── zip\                    ← ZIP-Archive (→ Abschnitt 4)
├── Lana Git\                   ← Lokale Git-Repositories / Mirror-Klone
├── logs\                       ← Laufzeit-Logs
├── runtime\                    ← Laufzeitdaten, temporäre Dateien
├── scripts\                    ← PowerShell / Bash Skripte
├── security\                   ← Sicherheitszertifikate, Policy-Dateien
├── Sync\                       ← Sync-Status für Cloud-Dienste
├── Tools\                      ← (Symlink / Verweis auf C:\Carpuncle Cloud\Tools)
├── EXECUTIVE_SUMMARY.md        ← Managementübersicht Lana-KI
├── LANA_CORE_MEMORY.md         ← Kern-Gedächtnis / persistenter Kontext
├── LANA_PATH_POLICY.md         ← Pfad-Richtlinie (USER=carpuncle.V6)
├── LANA_SYSTEM_BASELINE.md     ← System-Baseline, erwartete Dienste
├── lana_logo_192x192.png       ← App-Icon
├── Lana_Notitzbuch.md          ← Lokale Kopie dieses Notizbuchs
├── package-lock.json           ← Node.js Abhängigkeiten (Lana-Web / App)
└── README.md                   ← Einstiegspunkt für neue Installationen
```

**KI-Prüfregel:** Wenn nach Windows-Neuinstallation `C:\Carpuncle Cloud\Lana KI\` nicht vorhanden ist, sofort aus dem letzten Backup oder Git-Spiegel wiederherstellen, bevor irgendwelche Dienste gestartet werden.

---

## 4 · ZIP-Archiv-Inventar

Pfad: `C:\Carpuncle Cloud\Lana KI\docs\zip\`

Diese Archive enthalten **historische oder übertragene Daten**. Alle darin enthaltenen Keys/Secrets sind als **ungültig zu behandeln** – sie wurden bei der Übertragung kompromittiert oder sind veraltet.

| Dateiname | Inhalt / Hinweis |
|-----------|-----------------|
| `lana-ki-main.zip` | Lana-KI Haupt-Repo (Snapshot) – vor Verwendung auf riskante Dateien scannen |
| `lana-ki.zip` | Frühere Iteration des Repos |
| `lana.zip` | Basis-Lana-Archiv |
| `lana1.zip` – `lana4.zip` | Aufeinander folgende Entwicklungs-Snapshots |
| `lana-ki-unified-gateway.zip` | Gateway-Komponente (Logik, keine aktiven Keys) |
| `Lana-Master-Setup-Secret-Download-88x9.zip` | ⚠️ Name deutet auf Secrets hin – **vor Entpacken scannen, Keys als ungültig betrachten** |
| `LANA_KI_MASTER_BLUEPRINT_bundle.zip` | Master-Blueprint-Bündel |
| `gateway.zip` | Gateway-Quellcode-Snapshot |
| `logic.zip` | Logik-Komponenten |
| `logs.zip` | Log-Dateien-Archiv |
| `skill.zip` | Skill-Komponenten |
| `botContent.zip` | Bot-Inhalte / Prompts |
| `Carpuncle.zip` | Allgemeine Carpuncle-Konfigurationen |
| `Erstellt.zip` | Erstellte Artefakte |
| `icon.zip` | App-Icons |
| `Textdokument.zip` | Textdokumente |
| `Vault.zip` | ⚠️ Vault-Konfiguration – **Keys als ungültig betrachten** |
| `WindowsPowerShell.zip` | PowerShell-Profile / Skripte |
| `msgraph-training-python.zip` | Microsoft Graph Python-Training-Repo (Fork/Snapshot) |
| `authenticate-users-vercel-ai-next-js-sample.zip` | Vercel AI Auth-Sample |
| `commandlinetools-win-14742923_latest.zip` | Android SDK Command-Line-Tools |
| `op_windows_amd64_v2.33.0.zip` | 1Password CLI v2.33.0 (Windows AMD64) |
| `Bereitstellung – OpenAICreate-20260415115958.zip` | Azure-Bereitstellungs-Export (20260415) |
| `KI namens Lana.zip` | Frühe Lana-Konzeptdokumente |
| `Lana (carpu@lana-ki.de).zip` | E-Mail-Export oder Kontoarchiv |
| `lana-&-lia-–-thomas.zip` | Kommunikations-/Planungsarchiv |

**KI-Scan-Regel vor Merge:**
```powershell
# Vor jedem Entpacken ausführen:
git ls-files | Select-String -Pattern '\.env$|secret|token|password|credential|private|\.pem$|\.pfx$|\.ovpn$|\.zip$'
# Bei Treffern: STOP – erst manuell prüfen.
```

---

## 5 · Tools-Inventar

Pfad: `C:\Carpuncle Cloud\Tools\`  
Alle Tools sind portable (keine systemweite Installation nötig). Nach Windows-Neuinstallation diesen Ordner in den PATH aufnehmen.

| Tool / Ordner | Version / Hinweis |
|---------------|------------------|
| `git\` | Portable Git |
| `nodejs\` | Node.js (portable) |
| `Python3.12\` + `Python314\` + `python-full\` | Python-Versionen (portable) |
| `pwsh\` | PowerShell Core (portable) |
| `vscode\` | VS Code (portable) |
| `gcloud\` | Google Cloud SDK |
| `op_windows_amd64_v2.33.0\` | 1Password CLI |
| `rclone\` | rclone (Cloud-Sync) |
| `mongosh\` | MongoDB Shell |
| `jdk-25.0.2.10-hotspot\` | Java 25 (Adoptium) |
| `cmdline-tools\` + `sdk\` | Android SDK |
| `PuTTY\` | SSH-Client (PuTTY) |
| `WinSCP\` | SFTP/SCP-Client |
| `7zip\` | Archiv-Tool |
| `winrar\` | Archiv-Tool |
| `SSH\` | Portable SSH-Tooling |
| `PSTools\` | Sysinternals PsTools |
| `AnyDesk\` | Remote-Desktop |
| `Telegram\` | Messaging |
| `UniGetUI\` | Paketmanager-GUI |
| `NirSoft-Tools` (diverse `.exe`) | System-Diagnose / Analyse |

**PATH-Empfehlung (nach Windows-Neuinstallation):**
```powershell
$Env:PATH = "C:\Carpuncle Cloud\Tools\git\bin;" +
            "C:\Carpuncle Cloud\Tools\nodejs;" +
            "C:\Carpuncle Cloud\Tools\Python3.12;" +
            "C:\Carpuncle Cloud\Tools\pwsh;" +
            "C:\Carpuncle Cloud\Tools\gcloud\bin;" +
            "C:\Carpuncle Cloud\Tools\rclone;" +
            $Env:PATH
```

---

## 6 · Dienste und Endpunkte

| Dienst | URL / Endpunkt | Status |
|--------|---------------|--------|
| Lana KI Web-App | `https://lana-ki.de` | Ziel-Produktions-Domain |
| Carpuncle Cloud | `https://carpuncle.cloud` | Haupt-Domain |
| GitHub (carpu86) | `https://github.com/carpu86` | Aktives Profil |
| GitHub (carpuapi) | `https://github.com/carpuapi` | Organisation (zukünftig Master) |
| Azure OpenAI | Wert aus `AZURE_OPENAI_ENDPOINT` in `.env` | Inferenz-Endpunkt |
| Langfuse | Wert aus `LANGFUSE_HOST` in `.env` | Tracing / Observability |
| Cloudflare DNS | API via `CLOUDFLARE_API_TOKEN` | DNS-Verwaltung `lana-ki.de` |
| Google Cloud (GCP) | Projekt aus `gcloud config` | VM / Compute |

**KI-Prüfregel:** Endpunkt-URLs aus `.env` lesen, niemals hardcoden. Wenn ein Dienst nicht erreichbar → zuerst Cloudflare DNS prüfen (Script: `C:\Carpuncle Cloud\Tools\lana-cloudflare-dns-fix-v2.ps1`).

---

## 7 · Skripte und Automatisierung

Pfad: `C:\Carpuncle Cloud\Tools\`

| Skript | Zweck |
|--------|-------|
| `codex-safe-setup.ps1` | Sicheres Basis-Setup nach Windows-Neuinstallation |
| `codex-safe-cleanup.ps1` | Bereinigung temporärer / veralteter Dateien |
| `lana-cloudflare-dns-fix.ps1` | Cloudflare-DNS-Reparatur (v1) |
| `lana-cloudflare-dns-fix-v2.ps1` | Cloudflare-DNS-Reparatur (v2, bevorzugen) |
| `lana-p0-safe-audit.ps1` | P0-Sicherheitsaudit (kritische Konfigurationsprüfung) |

Pfad: `C:\Carpuncle Cloud\Lana KI\scripts\`  
Enthält weitere Lana-spezifische Automatisierungs-Skripte.

---

## 8 · Backup-Strategie

**Lokale Backups:** `C:\Carpuncle Cloud\Lana KI\_backups\`  
**GitHub-Mirror-Backups:** `C:\Carpuncle Cloud\Tools\repo-mirror-backup\`  
**ZIP-Archive:** `C:\Carpuncle Cloud\Lana KI\docs\zip\`

Backup-Rotation (PowerShell-Schema):
```powershell
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupDir = "C:\Carpuncle Cloud\github-repo-backups\$Stamp"
```

---

## 9 · Fehlerbehebungs-Muster für KI

### 9.1 Nach Windows-Neuinstallation
1. `C:\Carpuncle Cloud\` prüfen – muss vorhanden sein (liegt auf separater Partition / Laufwerk)
2. `C:\Carpuncle Cloud\carpuncle.V6` als `$HOME` / `%USERPROFILE%` setzen
3. `C:\Carpuncle Cloud\Tools\` in `PATH` aufnehmen (→ Abschnitt 5)
4. `C:\Carpuncle Cloud\.env` laden
5. SSH-Config prüfen: `C:\Carpuncle Cloud\carpuncle.V6\.ssh\config`

### 9.2 Git-Authentifizierung schlägt fehl
1. SSH-Key auf GitHub hochgeladen? `id_ed25519.pub` → GitHub → SSH Keys
2. SSH-Config zeigt auf richtigen Key? (`IdentityFile C:/Carpuncle Cloud/carpuncle.V6/.ssh/id_ed25519`)
3. SSH-Agent läuft? `ssh-add "C:\Carpuncle Cloud\carpuncle.V6\.ssh\id_ed25519"`

### 9.3 Dienst startet nicht (fehlende Env-Variable)
1. Schlüsselname in Abschnitt 2.3 nachschlagen
2. `C:\Carpuncle Cloud\.env` öffnen und Wert prüfen (nicht committen!)
3. Ggf. in Azure Portal / 1Password nachschlagen

### 9.4 DNS / Domain erreichbar nicht
1. `lana-cloudflare-dns-fix-v2.ps1` ausführen
2. Cloudflare Dashboard prüfen: Zone aus `CLOUDFLARE_ZONE_ID`
3. TTL abwarten (max. 300 Sekunden bei Cloudflare Proxy)

### 9.5 ZIP-Archiv soll verwendet werden
1. **Niemals blind entpacken und committen**
2. Erst riskante Dateien scannen (→ KI-Scan-Regel in Abschnitt 4)
3. Enthaltene Keys/Secrets als **ungültig** betrachten und neu generieren
4. Nur Logik und Dokumentation übernehmen

---

## 10 · Repository-Entscheidung (Zusammenfassung)

```
MASTER (aktiv):     carpu86/Lana
DOKU-BRÜCKE:        carpu86/Lana_Notitzbuch.md  (dieses Repo)
ARCHIVIEREN:        carpu86/Lana-ki
                    carpu86/lana-ki.app
                    carpu86/Lanaapp
                    carpu86/lana-ki-1
                    carpu86/xxx
                    carpu86/lana-web
                    carpu86/Google-oauth-apps-for-windows
SPÄTER:             carpu86/Lana → carpuapi/lana  (nach Archivierung fertig)
```

---

*Letzte Aktualisierung: 2026-05-14 · Version: 2.0*
