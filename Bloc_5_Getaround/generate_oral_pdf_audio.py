"""
Script de génération de la fiche prompteur PDF (1 page A4) et de l'audio MP3 (Vivienne)
pour l'oral de soutenance du BLOC 5 : GETAROUND MLOPS.
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

DIR_PROJET = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_5_Getaround")
DIR_REVISION = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\05_BLOC5_GETAROUND")
ALL_AUDIOS_DIR = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\TOUS_LES_AUDIOS_MP3")

HTML_PATH = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_5_GETAROUND.html"
PDF_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_5_GETAROUND_SLIDE_PAR_SLIDE.pdf"
PDF_REVISION = DIR_REVISION / "ORAL_SOUTENANCE_BLOC_5_GETAROUND_SLIDE_PAR_SLIDE.pdf"

MP3_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_5_GETAROUND.mp3"
MP3_ALL = ALL_AUDIOS_DIR / "ORAL_SOUTENANCE_BLOC_5_GETAROUND.mp3"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Oral Soutenance — Bloc 5 : Getaround MLOps (Prompteur 1 Page)</title>
<style>
  :root {
    --accent-color: #0284c7;
    --accent-bg: #f0f9ff;
  }
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
    line-height: 1.15;
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
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-left: 3px solid var(--accent-color);
    border-radius: 3px;
    padding: 2px 5px;
    margin-bottom: 3.5px;
    font-size: 6.2pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-tips strong { color: #0369a1; }
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
    font-size: 6.35pt;
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
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="header-title">
      BLOC 5 : GETAROUND MLOPS &amp; PRICING <span class="tag">RNCP 35288</span>
    </div>
    <div class="header-subtitle">
      Guide d'Oral Slide par Slide — Optimisation de Battement, Random Forest, FastAPI, Streamlit &amp; Docker
    </div>
  </div>
  <div class="header-meta">
    ÉPREUVE ORALE : 10 MIN (5m Pitch + 5m Q&amp;A)<br>
    Candidat : Christopher Gilleron · 7 Slides
  </div>
</div>

<div class="banner-tips">
  <span>🎯 <strong>Objectif :</strong> Résoudre les retards (arbitrage 60 min de battement) et déployer une API de tarification conteneurisée.</span>
  <span>⏱️ <strong>Rythme :</strong> ~40 sec / slide · Vision produit, modélisation &amp; architecture microservices</span>
</div>

<div class="grid-2">

  <!-- SLIDE 1 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S1</span> Contexte Métier &amp; Défis Getaround</div>
      <div class="slide-time">00:00 - 00:35 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Bonjour à tous. Aujourd'hui, je vous présente l'industrialisation et le déploiement du projet <strong>Getaround</strong>, leader européen de l'autopartage entre particuliers. Deux défis business majeurs confiés par l'équipe Produit : <strong>1. Résoudre le problème opérationnel des retards de restitution</strong> grâce à un simulateur de battement. <strong>2. Aider les propriétaires à maximiser leurs revenus locatifs</strong> via un moteur d'estimation tarifaire prédictif déployé sous forme d'API REST conteneurisée. »
      </div>
      <ul class="key-points">
        <li><strong>Client Métier :</strong> Getaround (autopartage P2P).</li>
        <li><strong>Double Enjeu :</strong> Qualité de service (zéro litige retard) + Monétisation propriétaire (pricing juste).</li>
      </ul>
      <div class="box-metric">
        <span>Stack Industrielle</span>
        <strong>Scikit-Learn · FastAPI · Streamlit · Docker · MLflow</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 2 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S2</span> Analyse Exploratoire des Retards</div>
      <div class="slide-time">00:35 - 01:20 (45s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Sur <strong>21 310 locations analysées</strong> : 57,4 % des courses enregistrent un retard, mais la <strong>médiane n'est que de 53 minutes</strong>. Surtout, seules <strong>8,6 %</strong> des locations sont consécutives (enchaînées en moins de 12h) : le risque de litige réel ne concerne que cette fraction. Au total, <strong>218 litiges avérés</strong> identifiés. Fait marquant : la technologie <em>Connect</em> (déverrouillage smartphone) enregistre <strong>18 points de retards en moins</strong> que la remise physique Mobile (43,1 % vs 61,3 %). »
      </div>
      <ul class="key-points">
        <li><strong>Volume :</strong> 21 310 locations · 218 litiges réels (conflit de créneau consécutif).</li>
        <li><strong>Impact Connect :</strong> 43,1% de retards (Connect) vs 61,3% (Mobile avec remise en main propre).</li>
      </ul>
      <div class="box-metric">
        <span>Locations consécutives : <strong>8,6 %</strong></span>
        <span>Litiges avérés : <strong>218 conflits réels</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 3 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S3</span> Simulateur &amp; Seuil Optimal 60 min</div>
      <div class="slide-time">01:20 - 02:05 (45s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pour arbitrer entre litiges évités et créneaux bloqués, j'ai développé un simulateur interactif. Les mathématiques désignent sans ambiguïté le point d'équilibre optimal : <strong>un battement de 60 minutes</strong>. À 60 min, nous neutralisons <strong>67 % des conflits réels (146 litiges évités)</strong> pour seulement <strong>1,88 % de réservations bloquées (401 créneaux)</strong>. Au-delà (120 min), la loi des rendements décroissants frappe : on résout 84 % des litiges mais on double les créneaux perdus à 3,8 % (810 réservations). Arbitrage Getaround : 60 minutes. »
      </div>
      <ul class="key-points">
        <li><strong>Compromis optimal :</strong> 60 minutes de battement obligatoire entre locations.</li>
        <li><strong>Bilan chiffré :</strong> 146 litiges évités (67%) pour seulement 1,88% d'exposition commerciale.</li>
      </ul>
      <div class="box-metric">
        <span>Seuil recommandé : <strong>60 min</strong></span>
        <span>Litiges résolus : <strong>67 % (146 conflits)</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 4 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S4</span> Modélisation Tarifaire : Random Forest</div>
      <div class="slide-time">02:05 - 02:50 (45s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pour prédire le prix journalier optimal sur <strong>4 843 annonces réelles</strong> : notre modèle <strong>Random Forest Regressor (120 arbres)</strong> atteint une erreur moyenne absolue <strong>MAE de 10,78 €/jour</strong> et un <strong>R² de 0,729</strong> sur les 969 véhicules de test. Par rapport à la baseline linéaire Ridge (MAE 12,12 €), le Random Forest gagne 1,34 €/jour de précision en captant les non-linéarités complexes du parc automobile. En production, nous proposons une fourchette de négociation de +/- 11 € autour de l'estimation. »
      </div>
      <ul class="key-points">
        <li><strong>Dataset Prix :</strong> 4 843 véhicules (3 874 train / 969 test indépendant).</li>
        <li><strong>Modèle retenu :</strong> Random Forest Regressor (MAE = 10,78 €/j, R² = 0,729).</li>
      </ul>
      <div class="box-metric">
        <span>Erreur Moyenne MAE : <strong>10,78 € / jour</strong></span>
        <span>Coefficient R² : <strong>0,729 (Ridge = 0.697)</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 5 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S5</span> Explicabilité : Les Variables Clés</div>
      <div class="slide-time">02:50 - 03:30 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « L'analyse d'importance des variables montre que <strong>deux critères écrasent tous les autres : la puissance moteur à 45,5 % et le kilométrage à 28,1 %</strong>. Ensemble, ils pèsent <strong>73,6 %</strong> de la valeur locative journalière d'une voiture ! Les équipements de confort comme le GPS, la climatisation ou le régulateur augmentent le taux de clic et l'attractivité de l'annonce, mais n'ont qu'un impact marginal sur le prix brut journalier. »
      </div>
      <ul class="key-points">
        <li><strong>Facteur n°1 :</strong> Puissance moteur (45,5%) · Segment premium vs citadine.</li>
        <li><strong>Facteur n°2 :</strong> Kilométrage compteur (28,1%) · Usure et décote mécanique.</li>
      </ul>
      <div class="box-metric">
        <span>Puissance + Kilométrage</span>
        <strong>73,6 % de l'explication du prix</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 6 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S6</span> Architecture Microservices &amp; MLOps</div>
      <div class="slide-time">03:30 - 04:20 (50s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pour industrialiser, architecture microservices 100 % conteneurisée : <strong>1. FastAPI (port 8000)</strong> avec validation stricte Pydantic v2, documentation Swagger interactive, prédictions unitaires et batch. <strong>2. Dashboard Streamlit (port 8502)</strong> offrant une interface ergonomique pour simuler les battements et estimer les véhicules. <strong>3. Docker Compose</strong> orchestrant hermétiquement les deux services sans conflit d'environnement. <strong>4. MLflow</strong> centralisant le versioning des modèles et la traçabilité des métriques. »
      </div>
      <ul class="key-points">
        <li><strong>API REST FastAPI :</strong> Port 8000 · Pydantic v2 · Inférence &lt; 15 ms · Swagger.</li>
        <li><strong>Orchestration :</strong> Docker Compose multi-conteneurs · Gouvernance MLflow.</li>
      </ul>
      <div class="box-metric">
        <span>Backend : <strong>FastAPI (Port 8000)</strong></span>
        <span>Frontend : <strong>Streamlit (Port 8502)</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 7 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S7</span> Recommandations Opérationnelles &amp; Bilan</div>
      <div class="slide-time">04:20 - 05:00 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Recommandations pour l'équipe Produit : <strong>1. Déployer le seuil de 60 min via un A/B testing</strong> sur une métropole pilote pour valider la baisse des annulations. <strong>2. Appliquer ce seuil universellement</strong>, car un client bloqué devant un véhicule autonome Connect ne pardonne pas. <strong>3. Intégrer l'API tarifaire dès l'onboarding propriétaire</strong> pour accélérer la mise en location. Bilan : 146 litiges évités, modèle fiable à 10 € près, et socle MLOps prêt pour l'échelle européenne. »
      </div>
      <ul class="key-points">
        <li><strong>Stratégie Déploiement :</strong> A/B Testing progressif avant généralisation universelle.</li>
        <li><strong>Impact Business :</strong> Satisfaction locataire préservée et revenus propriétaires optimisés.</li>
      </ul>
      <div class="box-metric">
        <span>Bilan</span>
        <strong>146 litiges résolus · API déployée · Architecture scalable</strong>
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

SPEECH_TEXT = """Bonjour à tous. Aujourd'hui, je vous présente l'industrialisation et le déploiement du projet Getaround, leader européen de l'autopartage entre particuliers.
Dans le cadre de cette certification Bloc 5, ma mission consistait à apporter une réponse technologique complète à deux défis business majeurs confiés par l'équipe Produit :
D'une part, résoudre le problème opérationnel des retards de restitution de véhicules grâce à un simulateur décisionnel de battement.
D'autre part, aider les propriétaires partenaires à maximiser leurs revenus locatifs grâce à un moteur d'estimation tarifaire prédictive déployé sous forme d'A P I en production.
Pour concrétiser ces solutions, j'ai mis en place une architecture microservices hermétique associant Scikit Learn, Fast A P I, Streamlit, Docker Compose et M L flow.

Slide 2 : Analyse exploratoire des retards.
En autopartage, le retard d'un locataire provoque un effet domino très destructeur : le client suivant arrive sur place, trouve le parking vide, attend dans l'incertitude et finit par annuler sa location. C'est une perte sèche et une dégradation d'image.
Face à cela, la tentation naturelle de l'équipe Produit est d'imposer un temps de battement obligatoire entre deux réservations.
Mais attention au piège économique : chaque heure de battement imposée bloque un créneau disponible et détruit du chiffre d'affaires potentiel pour nos propriétaires partenaires.
Mon objectif data était donc de quantifier précisément ce compromis : combien de conflits évite-t-on pour chaque créneau bloqué ?
Sur les 21 310 locations analysées, 57,4 pour cent des courses terminées enregistrent un retard au moment de rendre les clés.
Mais attention aux idées reçues : la médiane de ces retards n'est que de 53 minutes. La grande majorité sont de petits retards de moins d'une heure.
Surtout, les données révèlent que seules 8,6 pour cent des locations sont des locations consécutives enchaînées en moins de 12 heures. C'est uniquement sur cette fraction restreinte que le risque de conflit existe réellement.
Au total, nous avons identifié très exactement 218 litiges avérés où le retard du premier conducteur a dépassé le délai disponible avant la prise en main suivante.
Enfin, l'analyse démontre un avantage écrasant pour la technologie Getaround Connect sans remise physique de clé : seulement 43,1 pour cent de retards contre 61,3 pour cent pour le mode Mobile avec remise en main propre, soit 18 points de ponctualité gagnés grâce au déverrouillage autonome par smartphone.

Slide 3 : Simulateur de battement et seuil optimal 60 minutes.
Pour éclairer le choix de l'équipe Produit, j'ai développé un simulateur interactif modélisant la courbe de compromis entre litiges évités et volume de réservations bloquées.
Les résultats mathématiques désignent sans hésitation le point d'équilibre optimal : il se situe à un seuil de 60 minutes de battement.
À 60 minutes, nous neutralisons 67 pour cent des conflits réels, soit 146 litiges évités, pour seulement 1,88 pour cent du volume global de réservations bloquées, c'est-à-dire 401 créneaux.
Au-delà, la loi des rendements décroissants frappe durement : porter le seuil à 120 minutes permet de résoudre 84 pour cent des litiges, mais cela double le nombre de réservations bloquées à 3,8 pour cent, soit plus de 810 créneaux perdus.
Mon arbitrage pour Getaround est donc très clair : déployer un battement de 60 minutes.

Slide 4 : Modélisation tarifaire et Random Forest.
Passons au second volet : le modèle de tarification dynamique.
Pour aider les propriétaires à fixer un prix journalier juste et attractif, j'ai entraîné une chaîne de traitement complète sur 4 843 annonces réelles.
Sur le jeu de test indépendant de 969 véhicules, notre modèle Random Forest Regressor de 120 arbres atteint une erreur moyenne absolue M A E de 10,78 euros par jour et un coefficient de détermination R deux de 0,729.
Par rapport à notre baseline linéaire Ridge qui plafonnait à 12,12 euros d'erreur, le Random Forest fait gagner 1,34 euro de précision par jour en captant les interactions non-linéaires complexes.
En production, notre outil ne dicte pas un prix rigide : il propose une fourchette de négociation de plus ou moins 11 euros autour de l'estimation centrale.

Slide 5 : Explicabilité des prix et variables clés.
L'analyse d'explicabilité montre que deux variables écrasent toutes les autres : la puissance moteur à 45,5 pour cent et le kilométrage à 28,1 pour cent. Ensemble, elles pèsent 73,6 pour cent du prix d'une voiture.
Les options comme le G P S ou la climatisation favorisent le taux de clic plutôt que le prix brut journalier.

Slide 6 : Architecture microservices et industrialisation MLOps.
Pour l'industrialisation, cœur de ce Bloc 5, j'ai conçu une architecture microservices 100 pour cent conteneurisée :
Premièrement, notre A P I REST Fast A P I tourne sur le port 8000. Elle intègre une validation stricte des données entrantes grâce aux schémas Pydantic version 2, expose nativement une documentation Swagger interactive et prend en charge les prédictions unitaires ainsi que les calculs par lots pour les flottes professionnelles.
Deuxièmement, notre Dashboard décisionnel Streamlit tourne sur le port 8502. Il offre une interface visuelle épurée où les Product Managers simulent les seuils et où les propriétaires estiment leur véhicule en temps réel.
Troisièmement, les deux services sont orchestrés hermétiquement par Docker Compose, garantissant une reproductibilité absolue entre l'environnement de développement et la production.
Quatrièmement, l'ensemble de la chaîne est gouverné par M L flow : versioning du pipeline Scikit Learn, traçabilité des métriques et possibilité de rollback immédiat en cas de régression.

Slide 7 : Recommandations opérationnelles et bilan.
En conclusion, voici nos recommandations opérationnelles :
D'abord, déployer le seuil de battement de 60 minutes via un A B testing sur une métropole pilote pour mesurer sur le terrain la chute des annulations sans perturber l'ensemble du réseau.
Ensuite, appliquer ce seuil de façon universelle, car même si Connect a moins de retards, la déception d'un client bloqué devant un véhicule autonome est fatale pour sa fidélité.
Enfin, intégrer l'A P I de tarification dès la création de l'annonce pour accélérer la mise en location des véhicules.
Le bilan : 146 litiges évités pour moins de 2 pour cent de créneaux exposés, un modèle fiable à 10 euros près, et une infrastructure prête pour la montée en charge.
Merci pour votre écoute, et je suis prêt pour la démonstration en direct et vos questions.
"""

def clean_for_tts(text):
    t = text
    t = t.replace("%", " pour cent")
    t = t.replace("FastAPI", "Fast A P I")
    t = t.replace("MLflow", "M L flow")
    t = t.replace("MAE", "M A E")
    t = t.replace("R²", "R deux")
    t = t.replace("P2P", "peer to peer")
    t = t.replace("A/B testing", "A B testing")
    t = t.replace('"', '')
    t = t.replace('«', '')
    t = t.replace('»', '')
    return t

async def main():
    print("=== GÉNÉRATION BLOC 5 : GETAROUND MLOPS ===")
    
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
            margin={"top": "4.5mm", "bottom": "3.5mm", "left": "5.5mm", "right": "5.5mm"}
        )
        await browser.close()
    
    reader = pypdf.PdfReader(str(PDF_PROJET))
    page_count = len(reader.pages)
    print(f"[PDF] Pages générées : {page_count} (Cible : 1 page)")
    if page_count == 1:
        print("[SUCCÈS] Le PDF tient parfaitement sur 1 seule page A4 !")
    else:
        print(f"[ATTENTION] Le PDF fait {page_count} pages au lieu de 1 !")
        
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
    print("=== FIN BLOC 5 ===")

if __name__ == "__main__":
    asyncio.run(main())
