"""
Script de génération des fiches prompteurs PDF et des fichiers audio MP3
pour les oraux de soutenance CDSD (Blocs 2, 3, 4, 5 et 6).
Voix : fr-FR-VivienneMultilingualNeural
"""
import os
import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import pypdf
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_PROJETS = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD")
BASE_REVISIONS = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS")
ALL_AUDIOS_DIR = BASE_REVISIONS / "TOUS_LES_AUDIOS_MP3"
ALL_AUDIOS_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "fr-FR-VivienneMultilingualNeural"
RATE = "+4%"

# ==============================================================================
# 1. TEMPLATES HTML / CSS
# ==============================================================================

CSS_COMMON_1PAGE = """
@page {
  size: A4 portrait;
  margin: 4.5mm 5.5mm 3.5mm 5.5mm;
}
* {
  box-sizing: border-box;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 6.6pt;
  line-height: 1.16;
  color: #0f172a;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
}
.header {
  border-bottom: 2px solid var(--accent-color);
  padding-bottom: 2px;
  margin-bottom: 3px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.header-title {
  font-size: 9.5pt;
  font-weight: 800;
  color: #0a2540;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  display: flex;
  align-items: center;
  gap: 5px;
}
.header-title span.tag {
  background: var(--accent-color);
  color: white;
  font-size: 6.2pt;
  padding: 0.5px 5px;
  border-radius: 2.5px;
  font-weight: 700;
}
.header-subtitle {
  font-size: 6.6pt;
  font-weight: 600;
  color: #475569;
  margin-top: 1px;
}
.header-meta {
  font-size: 6.3pt;
  font-weight: bold;
  color: var(--accent-color);
  text-align: right;
  line-height: 1.2;
}
.banner-tips {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-left: 3px solid var(--accent-color);
  border-radius: 3px;
  padding: 2px 5px;
  margin-bottom: 3.5px;
  font-size: 6.2pt;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
}
.slide-card {
  border: 1px solid #cbd5e1;
  border-radius: 3.5px;
  margin-bottom: 3px;
  background: #ffffff;
  break-inside: avoid;
}
.slide-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: 2px 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.slide-title {
  font-size: 6.9pt;
  font-weight: 700;
  color: #0f172a;
  display: flex;
  align-items: center;
  gap: 3px;
}
.slide-title .num {
  background: var(--accent-color);
  color: #ffffff;
  padding: 0.5px 3.5px;
  border-radius: 2px;
  font-size: 5.9pt;
  font-weight: 800;
}
.slide-time {
  font-size: 5.7pt;
  font-weight: 700;
  color: var(--accent-color);
  background: var(--accent-bg);
  border: 0.5px solid var(--accent-color);
  padding: 0.5px 3.5px;
  border-radius: 2px;
}
.slide-body {
  padding: 2.5px 4.5px 2px 4.5px;
}
.speech-prompt {
  background: #fcfcfd;
  border-left: 2px solid var(--accent-color);
  padding: 2px 4px;
  font-style: italic;
  color: #1e293b;
  margin-bottom: 2.5px;
  font-size: 6.4pt;
  line-height: 1.15;
}
.speech-prompt strong {
  font-style: normal;
  color: #0f172a;
}
ul.key-points {
  margin: 0 0 2px 0;
  padding-left: 10px;
}
ul.key-points li {
  margin-bottom: 1px;
}
.box-metric {
  background: var(--accent-bg);
  border: 0.5px solid var(--accent-color);
  border-radius: 2px;
  padding: 1.5px 3.5px;
  font-size: 5.8pt;
  color: #0f172a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.box-metric strong {
  color: var(--accent-color);
}
"""

CSS_2PAGES = """
@page {
  size: A4 portrait;
  margin: 5mm 6mm 4mm 6mm;
}
* {
  box-sizing: border-box;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 6.8pt;
  line-height: 1.18;
  color: #0f172a;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
}
.page {
  height: 287mm;
  max-height: 287mm;
  overflow: hidden;
  page-break-after: always;
  display: flex;
  flex-direction: column;
}
.page:last-child {
  page-break-after: avoid;
}
.header {
  border-bottom: 2px solid var(--accent-color);
  padding-bottom: 2px;
  margin-bottom: 3.5px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.header-title {
  font-size: 9.8pt;
  font-weight: 800;
  color: #0a2540;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  display: flex;
  align-items: center;
  gap: 5px;
}
.header-title span.tag {
  background: var(--accent-color);
  color: white;
  font-size: 6.2pt;
  padding: 0.5px 5px;
  border-radius: 2.5px;
  font-weight: 700;
}
.header-subtitle {
  font-size: 6.8pt;
  font-weight: 600;
  color: #475569;
  margin-top: 1px;
}
.header-meta {
  font-size: 6.4pt;
  font-weight: bold;
  color: var(--accent-color);
  text-align: right;
  line-height: 1.25;
}
.banner-tips {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-left: 3px solid var(--accent-color);
  border-radius: 3px;
  padding: 2.5px 5.5px;
  margin-bottom: 4px;
  font-size: 6.3pt;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5px;
}
.slide-card {
  border: 1px solid #cbd5e1;
  border-radius: 3.5px;
  margin-bottom: 4px;
  background: #ffffff;
  break-inside: avoid;
}
.slide-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: 2.5px 5.5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.slide-title {
  font-size: 7.2pt;
  font-weight: 700;
  color: #0f172a;
  display: flex;
  align-items: center;
  gap: 3px;
}
.slide-title .num {
  background: var(--accent-color);
  color: #ffffff;
  padding: 0.5px 4px;
  border-radius: 2px;
  font-size: 6.1pt;
  font-weight: 800;
}
.slide-time {
  font-size: 5.9pt;
  font-weight: 700;
  color: var(--accent-color);
  background: var(--accent-bg);
  border: 0.5px solid var(--accent-color);
  padding: 0.5px 4px;
  border-radius: 2px;
}
.slide-body {
  padding: 3px 5px 2.5px 5px;
}
.speech-prompt {
  background: #fcfcfd;
  border-left: 2px solid var(--accent-color);
  padding: 2.5px 4.5px;
  font-style: italic;
  color: #1e293b;
  margin-bottom: 3px;
  font-size: 6.6pt;
  line-height: 1.17;
}
.speech-prompt strong {
  font-style: normal;
  color: #0f172a;
}
ul.key-points {
  margin: 0 0 2.5px 0;
  padding-left: 11px;
}
ul.key-points li {
  margin-bottom: 1px;
}
.box-metric {
  background: var(--accent-bg);
  border: 0.5px solid var(--accent-color);
  border-radius: 2px;
  padding: 2px 4px;
  font-size: 6pt;
  color: #0f172a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.box-metric strong {
  color: var(--accent-color);
}
"""

print("[INIT] Module de génération des oraux et audios initialisé.")
