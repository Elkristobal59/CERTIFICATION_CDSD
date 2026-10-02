"""
Script de génération de la fiche prompteur PDF (2 pages A4 Recto-Verso) et de l'audio MP3 (Vivienne)
pour l'oral de soutenance du BLOC 6 : PROJET FINAL CLINIER (10 MIN CHRONO).
"""
import os
import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import pypdf
import edge_tts
import shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VOICE = "fr-FR-VivienneMultilingualNeural"
RATE = "+4%"

DIR_PROJET = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_6_CliNER")
DIR_REVISION = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\06_BLOC6_CLINER_PROJET_FINAL")
ALL_AUDIOS_DIR = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\TOUS_LES_AUDIOS_MP3")

HTML_PATH = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_6_CLINER.html"
PDF_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_6_CLINER_SLIDE_PAR_SLIDE.pdf"
PDF_REVISION = DIR_REVISION / "ORAL_SOUTENANCE_BLOC_6_CLINER_SLIDE_PAR_SLIDE.pdf"

MP3_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_6_CLINER.mp3"
MP3_ALL = ALL_AUDIOS_DIR / "ORAL_SOUTENANCE_BLOC_6_CLINER.mp3"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Oral Soutenance — Bloc 6 : Projet Final CliNER (Prompteur 2 Pages)</title>
<style>
  :root {
    --accent-color: #0e7490;
    --accent-bg: #ecfeff;
  }
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
    justify-content: space-between;
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
    background: #ecfeff;
    border: 1px solid #a5f3fc;
    border-left: 3px solid var(--accent-color);
    border-radius: 3px;
    padding: 2.5px 5.5px;
    margin-bottom: 4px;
    font-size: 6.3pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-tips strong { color: #155e75; }
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    flex: 1;
  }
  .slide-card {
    border: 1px solid #cbd5e1;
    border-radius: 3.5px;
    margin-bottom: 4px;
    background: #ffffff;
    break-inside: avoid;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
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
    font-size: 6.55pt;
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
</style>
</head>
<body>

<!-- PAGE 1 : SLIDES 1 A 4 -->
<div class="page">
  <div>
    <div class="header">
      <div>
        <div class="header-title">
          BLOC 6 : PROJET FINAL CLINIER <span class="tag">RNCP 35288</span>
        </div>
        <div class="header-subtitle">
          Guide d'Oral Slide par Slide — Direction de Projet IA, Fine-Tuning LLM Souverain &amp; NLP Clinique (Page 1/2)
        </div>
      </div>
      <div class="header-meta">
        ÉPREUVE ORALE : 20 MIN (10m Pitch + 10m Q&amp;A)<br>
        Candidat : Christopher Gilleron · 8 Slides
      </div>
    </div>

    <div class="banner-tips">
      <span>🎯 <strong>Objectif :</strong> Automatiser l'extraction des critères d'éligibilité clinique avec Qwen-2.5-7B LoRA et BioBERT RAG.</span>
      <span>⏱️ <strong>Chrono :</strong> 10 min au total (~1m15 / slide) · Rigueur médicale, FinOps &amp; souveraineté</span>
    </div>
  </div>

  <div class="grid-2">

    <!-- SLIDE 1 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S1</span> Contexte Médical &amp; Enjeu d'Accès aux Essais</div>
        <div class="slide-time">00:00 - 01:15 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Bonjour à tous. Aujourd'hui, j'ai le plaisir de vous présenter <strong>CliNER</strong>, notre solution d'intelligence artificielle appliquée à la standardisation des protocoles cliniques et au recrutement de patients. En oncologie, le recrutement est un goulot d'étranglement critique : les médecins perdent des heures à lire des protocoles de 50 à 100 pages. ClinicalTrials.gov compte 500 000 études, mais l'information est enfouie dans des blocs de texte libre ou des PDF scannés. Mission de CliNER : un <strong>pipeline ETL augmenté par l'IA</strong> qui extrait chirurgicalement les critères d'éligibilité en données structurées. »
        </div>
        <ul class="key-points">
          <li><strong>Problème Médical :</strong> 80 % des essais accusent des retards de recrutement de patients.</li>
          <li><strong>Gisement Data :</strong> 500 000 protocoles ClinicalTrials.gov inexploitables à grande échelle.</li>
          <li><strong>Proposition de valeur :</strong> Diviser par 5 le temps de qualification d'un patient pour un essai.</li>
        </ul>
        <div class="box-metric">
          <span>Corpus mondial</span>
          <strong>500 000 protocoles · Textes non structurés</strong>
        </div>
      </div>
    </div>

    <!-- SLIDE 2 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S2</span> Démonstration Applicative &amp; UX Praticien</div>
        <div class="slide-time">01:15 - 02:30 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Notre solution se matérialise par une application web intuitive pour les oncologues. Depuis Streamlit, le praticien saisit une pathologie (ex. cancer du poumon). En moins d'une seconde, l'API officielle retourne les essais correspondants. Dès qu'il clique sur "Extraire", l'IA s'active : en <strong>2 à 4 secondes</strong>, le GPU génère un <strong>JSON médical structuré</strong> isolant pathologies ciblées, molécules prescrites, tranches d'âge et critères d'exclusion. Pour les études déjà analysées, notre <strong>cache vectoriel Supabase répond en 0,1 seconde</strong> sans GPU. Un chatbot RAG interactif permet de dialoguer directement avec le texte du protocole. »
        </div>
        <ul class="key-points">
          <li><strong>Recherche API :</strong> Instantanée (&lt; 1s) · Filtres d'état de recrutement et localisation.</li>
          <li><strong>Extraction IA :</strong> 2 à 4s sur GPU · JSON standardisé validé par Pydantic.</li>
          <li><strong>Cache persistant :</strong> 0,1s pour les études déjà traitées · Chatbot interactif RAG.</li>
        </ul>
        <div class="box-metric">
          <span>Temps d'extraction GPU : <strong>2 à 4 secondes</strong></span>
          <span>Réponse Cache Supabase : <strong>0,1 seconde</strong></span>
        </div>
      </div>
    </div>

    <!-- SLIDE 3 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S3</span> Architecture Cloud Hybride &amp; FinOps</div>
        <div class="slide-time">02:30 - 03:45 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Pour concilier haute performance et maîtrise des coûts, nous avons conçu une <strong>architecture FinOps à double détente</strong>. <strong>Branche A (Recherche &amp; UI) :</strong> 100 % serverless sur Render et API publique, coût 0 € en GPU. <strong>Branche B (Moteur IA) :</strong> allumée uniquement sur demande d'extraction profonde. Elle mobilise une instance <strong>AWS EC2 g4dn.xlarge (GPU NVIDIA T4 16 Go)</strong> propulsée par <strong>vLLM à 75 tokens/seconde</strong>, une base PostgreSQL Supabase avec pgvector, et un stockage S3 pour archiver les PDF. Le tracking est centralisé sur MLflow. »
        </div>
        <ul class="key-points">
          <li><strong>Branche A (Serverless) :</strong> Render (Streamlit) + API ClinicalTrials.gov (0 € GPU).</li>
          <li><strong>Branche B (Inférence GPU) :</strong> AWS EC2 g4dn.xlarge (NVIDIA T4) · Moteur vLLM (75 tok/s).</li>
          <li><strong>FinOps :</strong> Auto-Kill EC2 par script Boto3 dès inactivité · Réduction de 85 % de la facture AWS.</li>
        </ul>
        <div class="box-metric">
          <span>Inférence vLLM : <strong>75 tokens / sec</strong></span>
          <span>GPU : <strong>NVIDIA T4 16 Go (AWS EC2)</strong></span>
        </div>
      </div>
    </div>

    <!-- SLIDE 4 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S4</span> Pipeline ETL Augmenté par l'IA</div>
        <div class="slide-time">03:45 - 05:00 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Sous le capot, CliNER est un véritable pipeline ETL médical : <strong>1. Extraction robuste :</strong> Plan A direct si le JSON officiel fournit le texte (> 100 car) ; Plan B scraper PDF vers S3 avec zone de rejet pour isoler les fichiers corrompus sans bloquer le batch. <strong>2. Transformation hybride :</strong> BioBERT projette les paragraphes dans un espace biomédical 768D pour extraire le Top-5 des chunks pertinents et éliminer le bruit ; puis Qwen-2.5-7B Fine-Tuné génère le JSON final. <strong>3. Chargement :</strong> persistance dans Supabase et mise en cache vectoriel. »
        </div>
        <ul class="key-points">
          <li><strong>Extract (Plan A/B) :</strong> Parsing JSON direct ou téléchargement PDF avec zone de quarantaine.</li>
          <li><strong>Transform Hybride :</strong> BioBERT (filtrage sémantique 768D) + Qwen-7B LoRA (génération structurée).</li>
          <li><strong>Load :</strong> Cache vectoriel PostgreSQL Supabase (pgvector) pour réutilisation immédiate.</li>
        </ul>
        <div class="box-metric">
          <span>Embeddings BioBERT : <strong>768 dimensions</strong></span>
          <span>Prétraitement : <strong>Top-5 Chunks filtrés</strong></span>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- PAGE 2 : SLIDES 5 A 8 -->
<div class="page">
  <div>
    <div class="header">
      <div>
        <div class="header-title">
          BLOC 6 : PROJET FINAL CLINIER <span class="tag">RNCP 35288</span>
        </div>
        <div class="header-subtitle">
          Guide d'Oral Slide par Slide — Benchmark Médical, LLMOps, CI/CD &amp; Déploiement HDS (Page 2/2)
        </div>
      </div>
      <div class="header-meta">
        ÉPREUVE ORALE : 20 MIN (10m Pitch + 10m Q&amp;A)<br>
        Candidat : Christopher Gilleron · Slides 5 à 8
      </div>
    </div>

    <div class="banner-tips">
      <span>🎯 <strong>Excellence Métier :</strong> Souveraineté Qwen LoRA (0 € API propriétaire), priorité à la Précision clinique et gouvernance MLOps.</span>
      <span>⏱️ <strong>Chrono :</strong> Slides 5 à 8 (05:00 à 10:00) · Bilan stratégique et passage à l'échelle industrielle</span>
    </div>
  </div>

  <div class="grid-2">

    <!-- SLIDE 5 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S5</span> Fine-Tuning Souverain : Qwen-2.5-7B LoRA</div>
        <div class="slide-time">05:00 - 06:15 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Pour garantir la <strong>souveraineté des données médicales (RGPD)</strong> et éliminer les coûts prohibitifs des API fermées, nous avons fine-tuné le modèle open-source <strong>Qwen-2.5-7B via QLoRA 4-bit</strong> sur le corpus de référence <strong>CHIA</strong> (1 000 études annotées par des experts). Rigueur scientifique absolue : découpage strict par identifiant d'essai (800 train / 200 test) éliminant tout risque de data leakage. Pour le Demo Day, nous avons annoté 5 études réelles inédites hors CHIA. Pendant le training, la perte a fondu de <strong>1,66 à 0,84</strong> et l'accuracy token a atteint <strong>85,7 %</strong>. »
        </div>
        <ul class="key-points">
          <li><strong>Méthode QLoRA 4-bit :</strong> Adaptation de rang faible sur r=16, alpha=32 · 20M paramètres entraînés.</li>
          <li><strong>Corpus CHIA :</strong> 1 000 essais cliniques segmentés strictement sans fuite d'information.</li>
          <li><strong>Validation externe :</strong> 5 études réelles du Demo Day testées en aveugle complet.</li>
        </ul>
        <div class="box-metric">
          <span>Perte d'entraînement : <strong>1,66 &rarr; 0,84</strong></span>
          <span>Précision token : <strong>85,7 %</strong></span>
        </div>
      </div>
    </div>

    <!-- SLIDE 6 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S6</span> Benchmark &amp; Priorité à la Précision</div>
        <div class="slide-time">06:15 - 07:30 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Le verdict du benchmark : sur la tâche d'extraction d'entités nommées, notre fine-tuning fait bondir le <strong>F1-Score de 37 % (Gemini Flash) à 58,3 %</strong> pour Qwen LoRA (+21 points !). Mais en santé, la métrique reine n'est pas le F1 : <strong>c'est la Précision</strong>. Notre modèle atteint <strong>63 % de précision globale et 100 % sur l'extraction des molécules et médicaments</strong> guidée par BioBERT. Pourquoi ce choix ? En cancérologie, rater une mention est un désagrément, mais inventer un traitement qu'un patient ne doit pas recevoir serait une faute médicale grave. Fiabilité absolue. »
        </div>
        <ul class="key-points">
          <li><strong>Gain F1-Score :</strong> +21 pts face aux modèles généralistes non spécialisés (Gemini Flash).</li>
          <li><strong>Précision Médicaments :</strong> 100 % d'exactitude clinique grâce au double guidage BioBERT.</li>
          <li><strong>Éthique médicale :</strong> Zéro hallucination thérapeutique tolérée pour la sécurité du patient.</li>
        </ul>
        <div class="box-metric">
          <span>Précision Molécules : <strong>100 %</strong></span>
          <span>Gain F1 vs Gemini Flash : <strong>+21 points (58,3%)</strong></span>
        </div>
      </div>
    </div>

    <!-- SLIDE 7 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S7</span> Trajectoire MLOps &amp; LLMOps Industrielle</div>
        <div class="slide-time">07:30 - 08:45 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « Pour le passage à l'échelle industrielle, CliNER applique les standards Lead MLOps : <strong>1. CI/CD :</strong> pipelines GitHub Actions, tests unitaires PyTest, évaluation RAG automatisée via le framework Ragas, et conteneurs Docker multi-stage durcis et légers. <strong>2. Continuous Training (CT) :</strong> surveillance continue de la dérive des concepts (Data Drift) par <strong>distance de Wasserstein</strong> sur les embeddings BioBERT et réentraînement LoRA incrémental. <strong>3. FinOps &amp; Infra as Code :</strong> Terraform pour déployer le cluster et script Auto-Kill Boto3 sur AWS EC2. »
        </div>
        <ul class="key-points">
          <li><strong>CI/CD :</strong> GitHub Actions + PyTest + Framework Ragas (évaluation continue de la fidélité RAG).</li>
          <li><strong>Monitoring Drift :</strong> Distance de Wasserstein sur vecteurs BioBERT &rarr; Alerte réentraînement.</li>
          <li><strong>Infrastructure as Code :</strong> Terraform + Docker Multi-stage + Auto-Kill AWS EC2.</li>
        </ul>
        <div class="box-metric">
          <span>Détection Drift : <strong>Distance de Wasserstein</strong></span>
          <span>Évaluation RAG : <strong>Ragas Framework</strong></span>
        </div>
      </div>
    </div>

    <!-- SLIDE 8 -->
    <div class="slide-card">
      <div class="slide-header">
        <div class="slide-title"><span class="num">S8</span> Bilan d'Impact &amp; Déploiement HDS</div>
        <div class="slide-time">08:45 - 10:00 (75s)</div>
      </div>
      <div class="slide-body">
        <div class="speech-prompt">
          « En conclusion, CliNER apporte un impact concret et mesurable : <strong>réduction de 80 % du temps de revue des protocoles</strong> pour les oncologues, fiabilisation du pré-recrutement et accélération de la recherche médicale. Grâce à son architecture open-source souveraine, la solution est immédiatement déployable sur des serveurs hospitaliers certifiés <strong>HDS (Hébergeur de Données de Santé)</strong>, garantissant une conformité totale au secret médical et au RGPD. CliNER prouve qu'un modèle spécialisé de 7 milliards de paramètres surpasse les géants généralistes tout en restant frugal et souverain. Merci pour votre attention. »
        </div>
        <ul class="key-points">
          <li><strong>Impact Clinique :</strong> Revue de protocole accélérée de 80 % · Matching patient optimisé.</li>
          <li><strong>Souveraineté Hospitalière :</strong> Compatible Hébergeur Données de Santé (HDS) &amp; RGPD strict.</li>
          <li><strong>Frugalité :</strong> LLM 7B spécialisé &gt; API propriétaire fermée · Coûts prédictibles et maîtrisés.</li>
        </ul>
        <div class="box-metric">
          <span>Bilan</span>
          <strong>Gain de temps : 80 % · Déployable sur cluster hospitalier HDS</strong>
        </div>
      </div>
    </div>

  </div>
</div>

</body>
</html>
"""

SPEECH_TEXT = """Bonjour à tous. Aujourd'hui, j'ai le plaisir de vous présenter Cli N E R, notre solution d'intelligence artificielle appliquée à la standardisation des protocoles cliniques et au recrutement de patients.
Dans le monde médical, et particulièrement en oncologie, le recrutement des patients dans les essais cliniques est un goulot d'étranglement majeur.
Chaque semaine, les médecins et chercheurs perdent des heures précieuses à lire des protocoles indigestes de 50 à 100 pages pour savoir si l'un de leurs patients est éligible à un traitement novateur.
La base mondiale officielle, Clinical Trials point gov, compte près de 500 000 études. Mais ces données sont enfouies soit dans des blocs de texte libre au sein de fichiers J S O N massifs, soit dans des documents P D F annexés.
Notre mission avec Cli N E R : construire un pipeline E T L intelligent capable d'aspirer ces protocoles, d'en extraire chirurgicalement les critères d'éligibilité et de les restituer sous forme de données médicales parfaitement structurées.

Slide 2 : Démonstration applicative et expérience praticien.
Notre solution se matérialise sous la forme d'une application web interactive conçue pour les médecins.
Depuis l'interface Streamlit, le praticien tape simplement le nom d'une pathologie, par exemple le cancer du poumon.
En moins d'une seconde, l'application interroge l'A P I officielle et affiche un tableau synthétique des essais correspondants.
Lorsque le médecin sélectionne une étude pour en extraire les critères d'éligibilité, l'inférence G P U s'active : en 2 à 4 secondes, l'intelligence artificielle analyse le document et génère un J S O N structuré qui isole les pathologies ciblées, les médicaments prescrits, les tranches d'âge et les critères d'exclusion.
Et si ce protocole a déjà été analysé auparavant, notre cache vectoriel renvoie le résultat complet en un dixième de seconde sans solliciter le G P U.
L'application propose également un chatbot interactif qui permet au médecin de dialoguer en langage naturel directement avec le texte du protocole.

Slide 3 : Architecture cloud hybride et approche FinOps.
Pour concilier haute performance et maîtrise des coûts cloud, nous avons imaginé une architecture dite FinOps à double détente :
La Branche A gère la recherche et le filtrage. Elle tourne sur Streamlit hébergé sur Render et interroge directement l'A P I publique en requêtes gratuites, sans consommer la moindre ressource G P U.
La Branche B est le moteur d'intelligence, allumé uniquement lorsque l'extraction approfondie est demandée. Elle s'appuie sur une infrastructure distribuée :
Pour l'inférence G P U, nous utilisons une instance A W S E C 2 g 4 d n point x large avec carte N V I D I A T 4 et conteneurisation Docker, propulsée par le moteur v L L M pour un débit de 75 tokens par seconde.
Pour la persistance et la recherche sémantique, nous nous appuyons sur une base Postgre S Q L Supabase dotée de l'extension vectorielle p g vector, et un stockage S 3 pour archiver les P D F.
Le tracking des runs et la télémétrie sont centralisés sur un serveur M L flow dédié.

Slide 4 : Pipeline ETL augmenté par l'intelligence artificielle.
Sous le capot, Cli N E R fonctionne comme un véritable pipeline E T L augmenté par l'intelligence artificielle :
À l'étape d'extraction, nous gérons l'hétérogénéité des données grâce à un système à deux plans :
Le Plan A est un mode rapide : si le J S O N officiel contient déjà les critères textuels sur plus de 100 caractères, nous les extrayons directement.
Le Plan B est notre filet de sécurité : si le texte est absent, notre scraper télécharge le P D F original via le C D N officiel vers Supabase, avec une zone de rejet pour isoler les fichiers corrompus sans jamais interrompre le traitement global.
À l'étape de transformation, nous appliquons un pipeline hybride :
D'abord, Bio B E R T segmente le document et projette les paragraphes dans un espace vectoriel biomédical de 768 dimensions pour isoler les passages pertinents et éliminer le bruit.
Ensuite, notre modèle Kouène 2.5 7B Fine-Tuné reçoit ce contexte épuré et génère le J S O N finalisé.
Enfin, à l'étape de chargement, les résultats alimentent le tableau de bord et enrichissent la base vectorielle persistante.

Slide 5 : Fine-Tuning souverain : Qwen-2.5-7B LoRA.
Pour obtenir une précision clinique sans dépendre d'A P I propriétaires payantes comme Open A I, nous avons fait le choix de la souveraineté en fine-tunant le modèle Open-Source Kouène 2.5 7B via la méthode Q LoRA en 4 bits.
Nous avons entraîné le modèle sur le jeu de données de référence C H I A, qui comporte 1 000 études cliniques annotées par des experts.
Pour garantir une rigueur scientifique absolue et éliminer tout risque de fuite de données, la séparation entre les 800 études d'entraînement et les 200 études de test a été faite strictement par identifiant d'essai.
Mieux encore : pour le Demo Day, nous avons annoté manuellement 5 études réelles inédites et prouvé par script qu'elles n'appartenaient pas à la base C H I A.
Durant l'entraînement, la perte a fondu de 1,66 à 0,84 et la précision token a atteint 85,7 pour cent, confirmant que le modèle a parfaitement intégré la grammaire clinique.

Slide 6 : Benchmark et rigueur clinique : priorité à la précision.
Sur le plan des performances, le verdict du benchmark est sans appel :
Sur une métrique très exigeante de reconnaissance d'entités nommées, notre fine-tuning fait bondir le F 1 Score de 37 pour cent pour un modèle standard comme Gemini Flash à 58,3 pour cent pour notre modèle spécialisé, soit un gain spectaculaire de plus de 20 points.
Mais en milieu médical, la métrique reine n'est pas le F 1 Score : c'est la Précision.
Notre modèle atteint 63 pour cent de précision globale et monte jusqu'à 100 pour cent sur l'extraction des molécules et médicaments grâce au guidage de Bio B E R T.
Pourquoi ce choix ? Parce qu'en cancérologie, rater une mention dans un document est un désagrément, mais inventer un traitement qu'un patient ne doit pas recevoir serait une faute médicale grave. Notre modèle privilégie donc systématiquement la fiabilité à l'extrapolation.

Slide 7 : Trajectoire MLOps et LLMOps industrielle.
Pour terminer, nous avons pensé Cli N E R pour son passage à l'échelle industrielle selon les standards Lead M L Ops :
Premier axe : l'Intégration Continue C I C D avec des pipelines Git Hub Actions, des tests unitaires Py Test, la validation automatique des réponses R A G via Ragas, et des builds Docker multi-stage légers et durcis.
Deuxième axe : le Continuous Training C T avec la détection automatique de la dérive des concepts sur les embeddings via distance de Wasserstein et réentraînement LoRA incrémental.
Troisième axe : le FinOps et la Souveraineté, avec l'Infrastructure as Code Terraform pour automatiser l'infrastructure, un script d'Auto-Kill Boto 3 sur l'instance A W S E C 2 pour couper le G P U dès inactivité, et la capacité de déployer localement en milieu hospitalier certifié Hébergeur de Données de Santé.

Slide 8 : Bilan d'impact et perspectives de déploiement.
En conclusion, Cli N E R apporte un impact concret et mesurable : réduction de 80 pour cent du temps de revue des protocoles pour les oncologues, fiabilisation du pré-recrutement et accélération de la recherche médicale.
Grâce à son architecture open-source souveraine, la solution est immédiatement déployable sur des serveurs hospitaliers certifiés H D S, garantissant une conformité totale au secret médical et au R G P D.
Cli N E R prouve qu'un modèle spécialisé de 7 milliards de paramètres surpasse les géants généralistes tout en restant frugal et souverain.
Merci pour votre attention, et je suis ravi d'échanger avec vous.
"""

def clean_for_tts(text):
    t = text
    t = t.replace("%", " pour cent")
    t = t.replace("CliNER", "Cli N E R")
    t = t.replace("Qwen-2.5-7B", "Kouène 2.5 7B")
    t = t.replace("Qwen", "Kouène")
    t = t.replace("BioBERT", "Bio B E R T")
    t = t.replace("vLLM", "v L L M")
    t = t.replace("QLoRA", "Q LoRA")
    t = t.replace("HDS", "H D S")
    t = t.replace("CHIA", "C H I A")
    t = t.replace("JSON", "J S O N")
    t = t.replace("PDF", "P D F")
    t = t.replace("GPU", "G P U")
    t = t.replace("F1", "F 1")
    t = t.replace('"', '')
    t = t.replace('«', '')
    t = t.replace('»', '')
    return t

async def main():
    print("=== GÉNÉRATION BLOC 6 : PROJET FINAL CLINIER ===")
    
    # 1. Écriture HTML
    HTML_PATH.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"[OK] HTML écrit : {HTML_PATH}")
    
    # 2. Rendu PDF via Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{HTML_PATH.resolve().as_posix()}")
        await page.emulate_media(media="print")
        await page.pdf(
            path=str(PDF_PROJET),
            format="A4",
            print_background=True,
            margin={"top": "5mm", "bottom": "4mm", "left": "6mm", "right": "6mm"}
        )
        await browser.close()
    
    reader = pypdf.PdfReader(str(PDF_PROJET))
    page_count = len(reader.pages)
    print(f"[PDF] Pages générées : {page_count} (Cible : 2 pages Recto/Verso)")
    if page_count == 2:
        print("[SUCCÈS] Le PDF tient parfaitement sur 2 pages A4 Recto/Verso !")
    else:
        print(f"[ATTENTION] Le PDF fait {page_count} pages au lieu de 2 !")
        
    DIR_REVISION.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PDF_PROJET, PDF_REVISION)
    print(f"[COPIE] PDF copié vers {PDF_REVISION}")

    # 3. Audio MP3 via edge-tts (Vivienne)
    print("\n[AUDIO] Synthèse vocale avec Vivienne (fr-FR-VivienneMultilingualNeural)...")
    cleaned_speech = clean_for_tts(SPEECH_TEXT)
    communicate = edge_tts.Communicate(cleaned_speech, VOICE, rate=RATE)
    await communicate.save(str(MP3_PROJET))
    print(f"[OK] MP3 généré : {MP3_PROJET} ({MP3_PROJET.stat().st_size / 1024:.1f} Ko)")
    
    shutil.copy2(MP3_PROJET, MP3_ALL)
    print(f"[COPIE] MP3 copié vers {MP3_ALL}")
    print("=== FIN BLOC 6 ===")

if __name__ == "__main__":
    asyncio.run(main())
