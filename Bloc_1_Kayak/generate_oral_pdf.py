"""
Script de génération du PDF pour l'oral de soutenance du Bloc 1 - Kayak.
Génère une fiche de prompteur minutée slide par slide SUR UNE SEULE PAGE A4 (5 minutes chrono).
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import pypdf

OUTPUT_DIR_PROJET = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_1_Kayak")
OUTPUT_DIR_REVISION = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\01_BLOC1_KAYAK")

HTML_PATH = OUTPUT_DIR_PROJET / "ORAL_SOUTENANCE_BLOC_1_KAYAK.html"
PDF_PATH_PROJET = OUTPUT_DIR_PROJET / "ORAL_SOUTENANCE_BLOC_1_KAYAK_SLIDE_PAR_SLIDE.pdf"
PDF_PATH_REVISION = OUTPUT_DIR_REVISION / "ORAL_SOUTENANCE_BLOC_1_KAYAK_SLIDE_PAR_SLIDE.pdf"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Oral Soutenance — Bloc 1 : Kayak (Prompteur 1 Page)</title>
<style>
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
    font-size: 6.7pt;
    line-height: 1.18;
    color: #0f172a;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  /* Header Compact */
  .header {
    border-bottom: 2px solid #ff690f;
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
    background: #ff690f;
    color: white;
    font-size: 6.2pt;
    padding: 0.5px 5px;
    border-radius: 2.5px;
    font-weight: 700;
  }
  .header-subtitle {
    font-size: 6.7pt;
    font-weight: 600;
    color: #475569;
    margin-top: 1px;
  }
  .header-meta {
    font-size: 6.4pt;
    font-weight: bold;
    color: #ea580c;
    text-align: right;
    line-height: 1.25;
  }

  /* Guide Banner */
  .banner-tips {
    background: #fff7ed;
    border: 1px solid #fdba74;
    border-left: 3px solid #ea580c;
    border-radius: 3px;
    padding: 2.5px 5.5px;
    margin-bottom: 4px;
    font-size: 6.3pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-tips strong { color: #9a3412; }

  /* 2-Columns Grid */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
  }

  /* Slide Cards */
  .slide-card {
    border: 1px solid #cbd5e1;
    border-radius: 3.5px;
    margin-bottom: 3.5px;
    background: #ffffff;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    overflow: hidden;
  }
  .slide-header {
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 2px 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .slide-num-title {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .badge-slide {
    background: #0a2540;
    color: #ffffff;
    font-size: 5.8pt;
    font-weight: 800;
    padding: 0.5px 4px;
    border-radius: 2px;
    text-transform: uppercase;
  }
  .slide-title-text {
    font-size: 7.2pt;
    font-weight: 800;
    color: #0f172a;
  }
  .badge-chrono {
    background: #ffedd5;
    color: #9a3412;
    border: 1px solid #fdba74;
    font-size: 5.8pt;
    font-weight: 700;
    padding: 0.5px 3.5px;
    border-radius: 2px;
  }

  .slide-body {
    padding: 3px 5px 3.5px 5px;
  }

  /* Stage cues */
  .cue-box {
    background: #f1f5f9;
    border-left: 2px solid #64748b;
    padding: 1.5px 4px;
    margin-bottom: 2.5px;
    font-size: 5.9pt;
    color: #334155;
    font-style: italic;
  }
  .cue-box strong {
    color: #0f172a;
    font-style: normal;
  }

  /* Prompt Speech Text */
  .prompt-speech {
    font-size: 6.6pt;
    line-height: 1.18;
    color: #0f172a;
    text-align: justify;
    margin: 0 0 2.5px 0;
  }
  .prompt-speech strong {
    color: #0a2540;
    font-weight: 800;
  }
  .prompt-speech mark {
    background-color: #fef08a;
    color: #854d0e;
    font-weight: 700;
    padding: 0 1.5px;
    border-radius: 1.5px;
  }
  .prompt-speech em {
    color: #ea580c;
    font-style: normal;
    font-weight: 700;
  }

  /* Transition */
  .transition-box {
    background: #ecfdf5;
    border-left: 2px solid #10b981;
    padding: 1.5px 4px;
    font-size: 6pt;
    color: #065f46;
  }
  .transition-box strong { color: #047857; }

  /* Q&A Section */
  .qa-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 3px solid #d97706;
    border-radius: 3.5px;
    padding: 3px 5px;
    margin-top: 1px;
  }
  .qa-title {
    font-size: 6.8pt;
    font-weight: 800;
    color: #92400e;
    margin-bottom: 2px;
    display: flex;
    justify-content: space-between;
  }
  .qa-item {
    font-size: 6.1pt;
    line-height: 1.16;
    margin-bottom: 1.5px;
    color: #1e293b;
    text-align: justify;
  }
  .qa-item strong { color: #9a3412; }

  /* Footer */
  .footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 1.5px;
    display: flex;
    justify-content: space-between;
    font-size: 5.8pt;
    color: #64748b;
    margin-top: 2px;
  }
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="header">
    <div>
      <div class="header-title">
        <span>Oral Soutenance — Bloc 1 : Kayak</span>
        <span class="tag">PROMPTEUR 1 PAGE (5 MIN CHRONO)</span>
      </div>
      <div class="header-subtitle">Script oral intégral mot à mot — Présentation : Kayak_presentation.pptx — RNCP 35288</div>
    </div>
    <div class="header-meta">
      Candidat : Christopher GILLERON<br>
      Épreuve : 5 min Pitch + 15 min Q&A
    </div>
  </div>

  <!-- BANNER CONSEILS -->
  <div class="banner-tips">
    <div><strong>🎯 RÈGLE DU JEU :</strong> 5 minutes = 300 secondes (~140 mots/min). Ne récitez pas, racontez une démarche d'ingénieur. Marquez les pauses <em>(...)</em> et appuyez sur les mots en gras.</div>
    <div>⏱️ <strong>Chrono cible :</strong> 35-45s par slide</div>
  </div>

  <!-- GRID 2 COLONNES -->
  <div class="grid-2">

    <!-- COLONNE GAUCHE (SLIDES 1, 2, 3, 4) -->
    <div>

      <!-- SLIDE 1 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 1</span>
            <span class="slide-title-text">Titre & Cadrage Métier</span>
          </div>
          <span class="badge-chrono">⏱️ 00:00 - 00:35 (35s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Regard franc vers le jury. Voix posée. Posez le problème client avec conviction.</div>
          <p class="prompt-speech">
            « Bonjour messieurs-dames les membres du jury. Je suis <strong>Christopher Gilleron</strong>, et je vous présente aujourd'hui mon projet d'ingénierie des données pour le <strong>Bloc 1</strong> : <em>Plan your trip with Kayak</em>.
            Le point de départ est un besoin métier très concret : <strong>comment aider un voyageur indécis</strong> à planifier son séjour idéal en France en éliminant la météo défavorable et en lui recommandant instantanément les meilleurs hébergements ?
            Pour y répondre, j'ai conçu et déployé de bout en bout un <strong>pipeline ETL automatisé</strong> : il géocode <mark>35 grandes villes françaises</mark>, agrège les prévisions météo sur 5 jours, sélectionne les 5 destinations les plus ensoleillées, extrait <mark>100 offres hôtelières qualifiées</mark> sur Booking.com, et stocke l'ensemble dans une architecture Cloud sécurisée pour restituer des cartes interactives d'aide à la décision. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Voyons sur la slide suivante l'architecture globale qui soutient ce pipeline. »</div>
        </div>
      </div>

      <!-- SLIDE 2 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 2</span>
            <span class="slide-title-text">Architecture & Stack Technique</span>
          </div>
          <span class="badge-chrono">⏱️ 00:35 - 01:10 (35s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Balayez de gauche à droite sur le schéma : Sources ➔ ETL ➔ Cloud ➔ Restitution.</div>
          <p class="prompt-speech">
            « Voici la cartographie de notre infrastructure, articulée autour de <strong>quatre briques clés</strong> :
            D'abord, <strong>les Sources</strong> : l'API <em>OpenWeatherMap</em> pour la météo temps réel, et le site <em>Booking.com</em> pour l'offre hôtelière.
            Ensuite, <strong>la Collecte et l'ETL</strong> : j'ai choisi de piloter Chromium avec <strong>Playwright</strong> plutôt que Selenium. Playwright est nettement plus moderne, plus rapide, et gère nativement le rendu asynchrone JavaScript sans plantage.
            Pour <strong>le Stockage Cloud</strong>, j'ai mis en place une architecture à deux étages : <strong>Amazon S3</strong> comme Data Lake pour les fichiers bruts, et <strong>Neon DB</strong>, une base relationnelle <strong>PostgreSQL 16 serverless</strong> taillée pour le FinOps.
            Enfin, <strong>la Restitution</strong> : des cartes interactives créées avec <strong>Plotly Express</strong>, compilées en fichiers HTML autonomes visualisables sans aucun serveur applicatif lourd. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Détaillons maintenant la première étape : l'acquisition et le tri météo. »</div>
        </div>
      </div>

      <!-- SLIDE 3 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 3</span>
            <span class="slide-title-text">Collecte Météo & Heuristique Top-5</span>
          </div>
          <span class="badge-chrono">⏱️ 01:10 - 01:50 (40s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Citez bien les chiffres clés. Insistez sur le respect du rate-limiting Nominatim (rigueur d'ingénieur).</div>
          <p class="prompt-speech">
            « Pour interroger l'API météo, il fallait d'abord localiser précisément nos 35 villes. Les modèles météo raisonnant par coordonnées géodésiques, j'ai utilisé l'API de géocodage <strong>Nominatim d'OpenStreetMap</strong> pour convertir chaque commune en latitude et longitude exactes, en appliquant un délai strict de <mark>1,5 seconde</mark> pour respecter le rate-limiting.
            À partir de ces coordonnées, j'ai collecté les prévisions sur 5 jours d'OpenWeatherMap, soit <mark>40 relevés par ville</mark> consolidés sous Pandas.
            Pour isoler les meilleures destinations, j'ai défini une <strong>heuristique de tri stricte</strong> : maximiser la température moyenne et imposer un risque médian de pluie strictement nul.
            Le résultat est un <strong>Top-5 incontestable dans le Sud</strong> : <em>Nîmes</em> arrive en tête avec <mark>32,7 °C</mark>, suivie d'<em>Uzès</em> (31,5 °C), <em>Avignon</em>, <em>Carcassonne</em> et <em>Aix-en-Provence</em>, toutes avec <mark>0 % de risque de pluie</mark>. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Une fois nos 5 destinations sélectionnées, le pipeline déclenche le scraping des hôtels. »</div>
        </div>
      </div>

      <!-- SLIDE 4 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 4</span>
            <span class="slide-title-text">Scraping Hôtelier avec Playwright</span>
          </div>
          <span class="badge-chrono">⏱️ 01:50 - 02:40 (50s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Slide technique maîtresse ! Montrez la robustesse face aux anti-bots et la qualité des données.</div>
          <p class="prompt-speech">
            « Scraper un site comme Booking.com est un vrai défi face aux contre-mesures anti-robots et au chargement dynamique. Pour garantir une extraction 100 % fiable, j'ai conçu <strong>trois mécanismes avancés</strong> :
            1. Le <strong>contournement anti-bot</strong> : le script injecte un <em>User-Agent</em> réaliste de navigateur de bureau, simule un préchauffage de session sur la page d'accueil et clique automatiquement pour accepter la bannière de consentement <strong>OneTrust</strong>.
            2. La <strong>navigation en double-onglet</strong> : un onglet principal reste ancré sur la page de résultats pour préserver la recherche, tandis qu'un second onglet fait la navette en arrière-plan pour charger chaque hôtel en profondeur et en extraire le nom, le tarif en euros, la note client sur 10, la description et les coordonnées GPS.
            3. La <strong>stratégie du vivier tampon</strong> : plutôt que de prendre les 20 premiers résultats parfois incomplets, le script charge un vivier de <mark>50 candidats par ville</mark> et élimine immédiatement toute fiche sans prix ou sans note. Dès que <mark>20 hôtels parfaits</mark> sont validés, il passe à la ville suivante. Cela garantit un dataset final de <mark>100 hôtels d'une propreté absolue</mark>. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Voyons comment ces données sont pérennisées dans le Cloud. »</div>
        </div>
      </div>

    </div>

    <!-- COLONNE DROITE (SLIDES 5, 6, 7, 8 + Q&A) -->
    <div>

      <!-- SLIDE 5 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 5</span>
            <span class="slide-title-text">Architecture Cloud : S3 vs Neon DB</span>
          </div>
          <span class="badge-chrono">⏱️ 02:40 - 03:25 (45s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Insistez bien sur la distinction Data Lake (brut) vs Data Warehouse (analytique), puis l'argument FinOps.</div>
          <p class="prompt-speech">
            « Notre stockage Cloud applique la séparation canonique entre <strong>Data Lake</strong> et <strong>Data Warehouse</strong> :
            Au premier niveau, le <strong>Data Lake sur Amazon S3</strong> héberge le fichier brut <code>hotels_data.csv</code>. C'est notre <em>Raw Zone</em> : elle stocke la donnée source non modifiée. Son rôle est capital pour la résilience et la traçabilité : si la structure de Booking évolue ou si nous voulons recalculer une colonne demain, nous pouvons rejouer l'ETL sans jamais avoir besoin de re-scraper le web.
            Au second niveau, le <strong>Data Warehouse sur PostgreSQL</strong> stocke la table relationnelle nettoyée et typée, enrichie par les métriques météo via des identifiants UUID. C'est la table métier dédiée aux requêtes décisionnelles des analystes.
            Côté infrastructure, j'ai fait un choix <strong>FinOps fort avec Neon DB</strong> : cette base PostgreSQL managée est <em>serverless</em> et s'éteint automatiquement lorsqu'elle n'est pas sollicitée (<em>scale-to-zero</em>). Contrairement à une instance AWS RDS classique qui coûterait 20 € par mois en continu, Neon DB garantit un <strong>coût d'hébergement réel de 0,00 € par mois</strong>. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Ces données enrichies permettent de restituer des cartes interactives. »</div>
        </div>
      </div>

      <!-- SLIDE 6 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 6</span>
            <span class="slide-title-text">Restitution Cartographique (Plotly)</span>
          </div>
          <span class="badge-chrono">⏱️ 03:25 - 04:05 (40s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Décrivez les deux cartes. Mettez en avant le format "standalone / sans serveur".</div>
          <p class="prompt-speech">
            « Pour rendre ces résultats exploitables par l'équipe produit et les voyageurs, j'ai généré deux visualisations avec <strong>Plotly Express</strong> :
            La première carte, <code>top_5_destinations_map.html</code>, présente la météo globale avec un dégradé de chaleur et des marqueurs dont la taille est proportionnelle à la température observée sur nos cinq villes lauréates.
            La seconde carte, <code>top_20_hotels_map.html</code>, zoome directement sur les meilleurs établissements avec des infobulles riches : au survol ou au clic, l'utilisateur découvre instantanément le nom de l'hôtel, sa note sur 10, son prix pour deux nuits et un extrait de description.
            L'atout technique majeur réside dans le format : ces cartes sont exportées en <strong>fichiers HTML autonomes</strong> embarquant la librairie <em>Plotly.js</em>. Elles s'ouvrent dans n'importe quel navigateur sans nécessiter de serveur web ni d'API active, simplifiant leur intégration dans l'application Kayak. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Regardons le classement obtenu et le passage à l'échelle. »</div>
        </div>
      </div>

      <!-- SLIDE 7 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 7</span>
            <span class="slide-title-text">Classement & Axes d'Amélioration</span>
          </div>
          <span class="badge-chrono">⏱️ 04:05 - 04:45 (40s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Prenez de la hauteur. Apportez une vision d'architecte pour la mise en production industrielle.</div>
          <p class="prompt-speech">
            « Le classement met en avant des pépites, notamment l'hôtel <em>O Mas de Meze</em> à Uzès avec une note exceptionnelle de <mark>9,8/10</mark>, ou <em>Sur le quai</em> à Carcassonne, très compétitif à 304 € pour deux nuits.
            Si Kayak nous demandait de passer à des millions d'offres à l'échelle européenne, j'ai identifié <strong>trois axes d'amélioration industrielle</strong> :
            1. <strong>Normalisation de base de données</strong> : passer en <em>Troisième Forme Normale (3NF)</em> en séparant la table <code>cities</code> de la table <code>hotels</code> via une clé étrangère, pour éliminer toute redondance des attributs météo.
            2. <strong>Orchestration automatisée</strong> : déployer un DAG <strong>Apache Airflow</strong> planifié chaque matin pour actualiser la météo et les disponibilités en arrière-plan sans intervention humaine.
            3. <strong>Optimisation Big Data & Coûts</strong> : convertir les données en format colonnaire compressé <strong>Parquet</strong> sur S3 et utiliser le moteur serverless <strong>AWS Athena</strong>, permettant d'interroger des téraoctets de données pour quelques centimes. »
          </p>
          <div class="transition-box"><strong>➡️ TRANSITION :</strong> « Ce qui m'amène à ma conclusion. »</div>
        </div>
      </div>

      <!-- SLIDE 8 -->
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-num-title">
            <span class="badge-slide">Slide 8</span>
            <span class="slide-title-text">Conclusion & Ouverture aux Questions</span>
          </div>
          <span class="badge-chrono">⏱️ 04:45 - 05:00 (15s)</span>
        </div>
        <div class="slide-body">
          <div class="cue-box"><strong>👁️ POSTURE :</strong> Marquez un arrêt de 2 secondes. Souriez. Mains ouvertes. Vous terminez pile à 05:00.</div>
          <p class="prompt-speech">
            « En conclusion, ce projet valide l'intégralité des compétences du <strong>Bloc 1</strong> : la collecte multi-sources hétérogènes, le web scraping dynamique résilient, l'architecture Cloud hybride sécurisée et la restitution cartographique décisionnelle.
            Je vous remercie pour votre attention et je suis désormais ravi de répondre à l'ensemble de vos questions. »
          </p>
        </div>
      </div>

      <!-- BOX Q&A DU JURY -->
      <div class="qa-box">
        <div class="qa-title">
          <span>🎯 TOP 4 QUESTIONS PIÈGES DU JURY (RÉPONSES FLASH)</span>
          <span>15 MIN Q&A</span>
        </div>
        <div class="qa-item"><strong>Q1 : S3 ET PostgreSQL, pas redondant ?</strong> ➔ Non : S3 = Data Lake brut (résilience, rejouabilité de l'ETL sans re-scraper) ; PostgreSQL = Data Warehouse propre, typé et indexé pour requêtes analytiques rapides.</div>
        <div class="qa-item"><strong>Q2 : Pourquoi Nominatim avant OpenWeather ?</strong> ➔ L'API météo exige latitude/longitude géodésiques. Nominatim élimine aussi les homonymes (Paris France vs Texas) et les accents (Uzès).</div>
        <div class="qa-item"><strong>Q3 : Pourquoi Playwright vs Selenium/Scrapy ?</strong> ➔ Scrapy n'exécute pas le JavaScript dynamique de Booking. Playwright est plus moderne, plus rapide que Selenium et gère nativement le double-onglet.</div>
        <div class="qa-item"><strong>Q4 : FinOps Neon DB vs RDS ?</strong> ➔ RDS facture ~20 €/mois 24h/24 même sans trafic. Neon DB s'éteint automatiquement (scale-to-zero) hors requête : PostgreSQL 16 complet pour 0,00 €/mois.</div>
      </div>

    </div>

  </div>

  <!-- FOOTER -->
  <div class="footer">
    <span>Certification CDSD (RNCP 35288) — Bloc 1 (Ingénierie des données)</span>
    <span>Document d'épreuve : Fiche Prompteur Recto Unique (5 min chrono)</span>
    <span>Candidat : Christopher Gilleron</span>
  </div>

</body>
</html>
"""

async def generate_pdf():
    print("=" * 70)
    print("GÉNÉRATION DU PROMPTEUR 1 PAGE POUR LE BLOC 1 - KAYAK")
    print("=" * 70)

    HTML_PATH.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"HTML écrit : {HTML_PATH}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{HTML_PATH.as_posix()}", wait_until="networkidle")

        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        await browser.close()

    PDF_PATH_PROJET.write_bytes(pdf_bytes)
    PDF_PATH_REVISION.write_bytes(pdf_bytes)

    reader = pypdf.PdfReader(str(PDF_PATH_PROJET))
    print(f"Nombre total de pages du document : {len(reader.pages)}")
    print(f"Taille du fichier : {PDF_PATH_PROJET.stat().st_size // 1024} Ko")
    if len(reader.pages) == 1:
        print("[SUCCÈS PARFAIT] Le PDF tient STRICTEMENT sur UNE SEULE PAGE !")
    else:
        print(f"[ATTENTION] Le PDF fait {len(reader.pages)} pages. Réajustement nécessaire.")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(generate_pdf())
