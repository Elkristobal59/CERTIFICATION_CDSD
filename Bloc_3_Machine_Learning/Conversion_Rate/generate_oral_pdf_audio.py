"""
Script de génération de la fiche prompteur PDF (1 page A4) et de l'audio MP3 (Vivienne)
pour l'oral de soutenance du BLOC 3 : CONVERSION RATE CHALLENGE.
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

DIR_PROJET = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_3_Machine_Learning\Conversion_Rate")
DIR_REVISION = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\03_BLOC3_CONVERSION_RATE")
ALL_AUDIOS_DIR = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\TOUS_LES_AUDIOS_MP3")

HTML_PATH = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_3_CONVERSION_RATE.html"
PDF_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_3_CONVERSION_RATE_SLIDE_PAR_SLIDE.pdf"
PDF_REVISION = DIR_REVISION / "ORAL_SOUTENANCE_BLOC_3_CONVERSION_RATE_SLIDE_PAR_SLIDE.pdf"

MP3_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_3_CONVERSION_RATE.mp3"
MP3_ALL = ALL_AUDIOS_DIR / "ORAL_SOUTENANCE_BLOC_3_CONVERSION_RATE.mp3"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Oral Soutenance — Bloc 3 : Conversion Rate (Prompteur 1 Page)</title>
<style>
  :root {
    --accent-color: #059669;
    --accent-bg: #ecfdf5;
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
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-left: 3px solid var(--accent-color);
    border-radius: 3px;
    padding: 2px 5px;
    margin-bottom: 3.5px;
    font-size: 6.2pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-tips strong { color: #065f46; }
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
      BLOC 3 : CONVERSION RATE CHALLENGE <span class="tag">RNCP 35288</span>
    </div>
    <div class="header-subtitle">
      Guide d'Oral Slide par Slide — Machine Learning Supervisé, Optimisation de Seuil &amp; Explicabilité
    </div>
  </div>
  <div class="header-meta">
    ÉPREUVE ORALE : 10 MIN (5m Pitch + 5m Q&amp;A)<br>
    Candidat : Christopher Gilleron · 8 Slides
  </div>
</div>

<div class="banner-tips">
  <span>🎯 <strong>Objectif :</strong> Maximiser le F1-Score sur une classe minoritaire (3,23 %) et justifier le choix LogReg vs XGBoost.</span>
  <span>⏱️ <strong>Rythme :</strong> ~35 sec / slide · Rigueur mathématique &amp; recommandations produit</span>
</div>

<div class="grid-2">

  <!-- SLIDE 1 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S1</span> Contexte Métier &amp; Objectifs Business</div>
      <div class="slide-time">00:00 - 00:35 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Bonjour à tous. Aujourd'hui, je vous présente notre travail sur la prédiction du taux de conversion pour le média en ligne <strong>Data Science Weekly</strong>. Leur enjeu : des centaines de milliers de visites, mais ils veulent savoir qui a le plus de chances de s'abonner et sur quels leviers appuyer. Objectif double : bâtir un <strong>modèle prédictif robuste</strong> sur données très déséquilibrées, et fournir des recommandations concrètes à l'équipe produit. »
      </div>
      <ul class="key-points">
        <li><strong>Client Métier :</strong> Data Science Weekly (newsletter IA &amp; Data).</li>
        <li><strong>Double Finalité :</strong> Scoring temps réel des prospects + Optimisation du parcours lecteur.</li>
      </ul>
      <div class="box-metric">
        <span>Volume d'étude</span>
        <strong>284 580 sessions de navigation</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 2 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S2</span> Données &amp; Défi du Déséquilibre</div>
      <div class="slide-time">00:35 - 01:15 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « L'étude porte sur <strong>284 580 sessions</strong> et 5 variables : pays, âge, fidélité (new/returning), source d'acquisition et pages vues. Le fait marquant : un taux de conversion global de seulement <strong>3,23 %</strong>. Piège absolu : l'Accuracy ne veut rien dire, prédire zéro donnerait 96,8 % d'accuracy tout en ratant 100 % des abonnés. Notre boussole est donc le <strong>F1-Score</strong> sur la classe positive, avec un split stratifié 80/20. »
      </div>
      <ul class="key-points">
        <li><strong>Dataset :</strong> 227 664 sessions train / 56 916 validation (stratification stricte).</li>
        <li><strong>Métrique clé :</strong> F1-Score (moyenne harmonique précision-rappel sur les abonnés).</li>
      </ul>
      <div class="box-metric">
        <span>Taux de conversion : <strong>3,23 %</strong></span>
        <span>Accuracy naïve = <strong>96,8 % (trompeur)</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 3 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S3</span> Profils Visiteurs &amp; Analyse Exploratoire</div>
      <div class="slide-time">01:15 - 01:55 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Trois constats majeurs : <strong>1. Gouffre géographique :</strong> Allemagne à <strong>6,2 %</strong>, UK à 5,2 %, USA à 3,8 %, mais la Chine s'effondre à <strong>0,1 %</strong> (x60 d'écart ! bug de tunnel, traduction ou pare-feu). <strong>2. Puissance de la récurrence :</strong> les habitués convertissent 5 fois plus que les nouveaux arrivants (7,2 % vs 1,4 %). <strong>3. Canaux neutres :</strong> Ads, SEO et Direct oscillent tous autour de 3 %. Le canal apporte du volume, pas la décision. »
      </div>
      <ul class="key-points">
        <li><strong>Géographie :</strong> Allemagne (6,2%) &gt; UK (5,2%) &gt; US (3,8%) &gt;&gt;&gt; Chine (0,1%).</li>
        <li><strong>Comportement :</strong> Returning user = facteur multiplicateur x5 de conversion.</li>
      </ul>
      <div class="box-metric">
        <span>Allemagne vs Chine : <strong>Ratio x60</strong></span>
        <span>Returning vs New : <strong>7,2% vs 1,4%</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 4 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S4</span> Comportement en Ligne : La Variable Reine</div>
      <div class="slide-time">01:55 - 02:35 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Une variable écrase tout : le <strong>nombre total de pages vues</strong>. Les non-abonnés consultent 4 pages en moyenne, les convertis en consultent <strong>14</strong> ! Les distributions se séparent nettement : dépasser 8 à 10 pages fait exploser la probabilité d'inscription. L'âge joue aussi : les convertis ont 25 ans en moyenne contre 30 ans. Rigueur data : détection de 2 âges aberrants à 123 ans, sans impact statistique mais remontés à l'équipe web. »
      </div>
      <ul class="key-points">
        <li><strong>Pages vues :</strong> 4 pages (non-convertis) vs 14 pages (convertis) · Séparation nette.</li>
        <li><strong>Âge :</strong> Corrélation inverse · Les jeunes professionnels convertissent davantage.</li>
      </ul>
      <div class="box-metric">
        <span>Pages vues convertis : <strong>14 pages</strong></span>
        <span>Seuil critique engagement : <strong>8 à 10 pages</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 5 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S5</span> Pipeline Scikit-Learn &amp; Baseline</div>
      <div class="slide-time">02:35 - 03:15 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pour modéliser sans fuite de données, pipeline scikit-learn rigoureux : <strong>StandardScaler</strong> sur pages vues et âge, <strong>OneHotEncoder(drop='first')</strong> sur pays et source. Baseline minimale sur une seule variable (pages vues) : F1-Score déjà élevé à <strong>0,7055</strong> (rappel 61 %). La régression logistique complète intégrant toutes les variables monte à <strong>F1 = 0,7675</strong>, avec une précision de 86,5 % et un rappel de 69 %. »
      </div>
      <ul class="key-points">
        <li><strong>Préprocessing :</strong> ColumnTransformer étanche ajusté sur train uniquement.</li>
        <li><strong>Progression :</strong> Baseline 1 variable (0.7055) &rarr; LogReg complète (0.7675).</li>
      </ul>
      <div class="box-metric">
        <span>Baseline LogReg (1 var) : <strong>0,7055</strong></span>
        <span>LogReg Multivariée : <strong>0,7675</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 6 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S6</span> Optimisation du Seuil de Décision</div>
      <div class="slide-time">03:15 - 03:55 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Par défaut, la classification coupe à 0,50. Mais sur un jeu à 3 % de positifs, 0,50 est trop frileux. Nous avons balayé les seuils de 0,05 à 0,95 pour trouver l'optimum F1. Résultat sans appel : <strong>le seuil optimal se situe à 0,45</strong>. Le F1-Score atteint <strong>0,7762</strong> : le rappel grimpe à <strong>71,8 %</strong> (1 318 abonnés captés sur 1 836, 242 faux positifs). Le plateau est très stable entre 0,40 et 0,50, garantissant une forte robustesse en production. »
      </div>
      <ul class="key-points">
        <li><strong>Balayage de seuil :</strong> Optimisation fine sur l'ensemble de validation.</li>
        <li><strong>Impact à 0,45 :</strong> Rappel +2,8 pts · 1 318 abonnés détectés sur 1 836 réels.</li>
      </ul>
      <div class="box-metric">
        <span>Seuil optimal : <strong>0,45</strong></span>
        <span>F1-Score Champion : <strong>0,7762</strong> (Recall 71,8%)</span>
      </div>
    </div>
  </div>

  <!-- SLIDE 7 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S7</span> Benchmark Modèles &amp; Explicabilité</div>
      <div class="slide-time">03:55 - 04:30 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Face aux modèles complexes : Random Forest plafonne à <strong>0,7611</strong>. XGBoost optimisé atteint <strong>0,7763</strong>, soit une stricte égalité avec la LogReg à <strong>0,7762</strong>. Choix final : la <strong>Régression Logistique</strong> ! Moins lourde, instantanée, et surtout 100 % explicable grâce aux Odds Ratios : résider en Allemagne multiplie par <strong>35</strong> la chance de convertir par rapport à la Chine, et chaque écart-type de pages vues apporte un coefficient massif de <strong>+2,52</strong>. »
      </div>
      <ul class="key-points">
        <li><strong>Benchmark :</strong> RF (0.7611) &lt; LogReg (0.7762) &asymp; XGBoost (0.7763).</li>
        <li><strong>Explicabilité :</strong> Odds Ratios immédiats (Allemagne x35, UK x30, P. vues +2.52).</li>
      </ul>
      <div class="box-metric">
        <span>Choix d'ingénieur</span>
        <strong>Régression Logistique (F1=0.7762 · Zéro boîte noire)</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 8 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S8</span> Recommandations Métier &amp; Bilan</div>
      <div class="slide-time">04:30 - 05:00 (30s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Trois actions prioritaires pour Data Science Weekly : <strong>1. Audit d'urgence sur la Chine</strong> pour lever le verrou technique (potentiel de croissance immédiat). <strong>2. Gamification multi-pages</strong> : liens connexes, sommaires pour emmener un maximum de lecteurs au-delà de 8 à 10 pages. <strong>3. Pop-up d'abonnement déclenchée au 9ᵉ clic</strong> pour les visiteurs engagés plutôt qu'à l'arrivée. Bilan : pipeline léger, F1 = 0,7762, modèle prêt pour la production. »
      </div>
      <ul class="key-points">
        <li><strong>Action 1 - Technique :</strong> Résolution du blocage chinois (marché inexploité).</li>
        <li><strong>Action 2 - UX :</strong> Encourager le feuilletage (&gt; 8 pages) pour franchir le seuil d'activation.</li>
        <li><strong>Action 3 - Timing :</strong> Déclenchement contextualisé de la capture d'email.</li>
      </ul>
      <div class="box-metric">
        <span>Bilan</span>
        <strong>Pipeline exporté en production · Leviers ROI immédiats</strong>
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

SPEECH_TEXT = """Bonjour à tous. Aujourd'hui, je vous présente notre travail sur la prédiction du taux de conversion pour le média en ligne Data Science Weekly.
Data Science Weekly, c'est une newsletter spécialisée dans l'intelligence artificielle et la data. Leur enjeu est simple : ils reçoivent des centaines de milliers de visites, mais ils veulent savoir qui a le plus de chances de s'inscrire, et surtout sur quels leviers appuyer pour faire décoller leur nombre d'abonnés.
L'objectif de mon projet est double : d'abord, construire un modèle prédictif robuste capable d'identifier les futurs abonnés sur un jeu de données très déséquilibré. Ensuite, fournir à l'équipe produit des recommandations concrètes et chiffrées pour agir directement sur le site.

Slide 2 : Les données et le défi du déséquilibre.
Pour mener cette étude, nous avons analysé 284 580 sessions de navigation avec cinq variables : le pays d'origine du visiteur, son âge, s'il s'agit d'un nouveau visiteur ou d'un habitué, son canal d'arrivée, et le nombre total de pages qu'il a consultées.
La donnée clé, c'est le taux de conversion global : seulement 3,23 pour cent. Concrètement, sur 100 personnes qui visitent le site, à peine 3 laissent leur email.
Cette disproportion entraîne un piège classique en machine learning : l'Accuracy ne veut rien dire. Si je crée un modèle simpliste qui prédit systématiquement zéro, il aura 96,8 pour cent d'accuracy tout en ratant 100 pour cent des abonnés.
C'est pour cette raison que notre boussole tout au long du projet est le F 1 Score sur la classe minoritaire, c'est-à-dire l'équilibre parfait entre la précision de nos alertes et notre capacité à ne pas rater d'inscriptions.

Slide 3 : Profils visiteurs et analyse exploratoire.
Quand on regarde d'où viennent les visiteurs et comment ils réagissent, trois constats majeurs sautent aux yeux :
Premièrement, la géographie fait des écarts monumentaux. En Allemagne, le taux de conversion grimpe à 6,2 pour cent. Au Royaume-Uni, on est à 5,2 pour cent, et aux États-Unis à 3,8 pour cent. Mais en Chine, le taux s'effondre à 0,1 pour cent. Un visiteur allemand a 60 fois plus de chances de s'abonner qu'un visiteur chinois. Un tel gouffre n'est pas une simple question d'intérêt éditorial : cela indique un problème d'accessibilité technique, de traduction ou de pare-feu sur le site chinois.
Deuxièmement, la fidélité est un levier puissant : les visiteurs récurrents convertissent 5 fois plus que les nouveaux arrivants, avec 7,2 pour cent contre seulement 1,4 pour cent.
Troisièmement, le canal d'acquisition joue très peu : qu'un visiteur vienne de la publicité, du référencement naturel ou en direct, le taux oscille autour des 3 pour cent. Le canal amène du volume, mais ce n'est pas lui qui décide de la signature.

Slide 4 : Le comportement du visiteur, la variable reine.
Si on se penche maintenant sur le comportement en ligne, il y a une variable qui écrase absolument toutes les autres : le nombre de pages vues pendant la session.
Les visiteurs qui ne s'abonnent pas regardent en moyenne 4 pages. Les visiteurs qui s'abonnent en regardent 14. Les deux courbes de distribution ne se chevauchent pratiquement pas : dès qu'un internaute dépasse 8 à 10 pages, sa probabilité d'inscription explose.
L'âge joue aussi un rôle net : les convertis sont plus jeunes, avec une moyenne d'âge autour de 25 ans contre 30 ans pour l'ensemble des visiteurs.
Petite note de rigueur sur la qualité des données : nous avons repéré deux sessions avec un âge aberrant à 123 ans. Sur 284 000 lignes, leur impact est statistiquement nul, mais cela nous a permis de remonter une alerte technique à l'équipe web sur la validation de leurs formulaires.

Slide 5 : Pipeline Scikit-Learn et modèle de référence.
Pour construire nos modèles sans aucune fuite de données, nous avons mis en place un pipeline scikit-learn propre :
D'abord, un découpage stratifié 80 / 20 pour garder exactement 3,23 pour cent d'abonnés dans le train et dans la validation.
Ensuite, un préprocesseur qui applique une standardisation sur les variables numériques comme les pages vues et l'âge, et un encodage ouane hot sans première modalité pour les variables catégorielles comme le pays et la source.
Pour tester notre point de départ, nous avons entraîné une régression logistique minimale sur une seule variable : les pages vues. Elle obtient déjà un F 1 Score de 0,7055 avec un rappel de 61 pour cent.
En intégrant l'ensemble des variables explicatives, notre régression logistique complète monte à 0,7675 de F 1 Score, avec une précision de 86,5 pour cent et un rappel de 69 pour cent.

Slide 6 : Optimisation du seuil de décision.
Par défaut, un algorithme de classification binaire coupe sa décision à 0,50 de probabilité. Mais sur un jeu de données où la classe positive ne pèse que 3 pour cent, ce seuil de 0,50 est trop frileux.
Nous avons donc balayé l'ensemble des seuils de décision entre 0,05 et 0,95 sur notre jeu de validation pour trouver l'optimum qui maximise le F 1 Score.
Le résultat est sans appel : le meilleur compromis se situe à un seuil de 0,45.
En passant le seuil à 0,45, le F 1 Score monte à 0,7762. Concrètement, nous passons le rappel à 71,8 pour cent : sur les 1 836 abonnés réels du jeu de validation, le modèle en attrape 1 318, tout en limitant les fausses alertes à seulement 242.
La courbe est très plate entre 0,40 et 0,50, ce qui démontre que notre réglage est parfaitement robuste et stable.

Slide 7 : Benchmark des modèles et explicabilité.
Nous avons challengé cette approche face à des algorithmes plus complexes :
Un random forest optimisé plafonne à 0,7611 de F 1 Score, avec une tendance à générer plus de faux positifs.
Un X G Boost avec régularisation atteint 0,7763, soit exactement le même score que notre régression logistique à 0,7762.
Face à cette égalité de score, notre choix final se porte sur la régression logistique. Pourquoi ? Parce qu'avec 5 variables bien nettoyées, la frontière de séparation est quasi-linéaire. Mais surtout, la logistique n'est pas une boîte noire : elle nous donne des coefficients directs et des odds ratios immédiatement compréhensibles pour l'équipe métier.
Concrètement, résider en Allemagne multiplie par 35 la chance de convertir par rapport à la Chine. Résider au Royaume-Uni la multiplie par 30. Et chaque augmentation d'un écart-type sur les pages vues apporte un coefficient massif de plus 2,52.

Slide 8 : Recommandations métier et plan d'action.
De ces analyses, nous tirons trois actions prioritaires pour la newsletter :
Action numéro un : lancer un audit d'urgence sur l'accès depuis la Chine. Avec 0,1 pour cent de conversion, il y a un bug technique, un problème de passerelle ou de chargement. Le débloquer offrirait un réservoir de croissance immédiat.
Action numéro deux : repenser le parcours de lecture pour favoriser la navigation multi-pages. Mettre des liens d'articles recommandés en bas de page, des résumés en fin d'article et des sommaires pour emmener un maximum de lecteurs au-delà de 8 à 10 pages.
Action numéro trois : afficher un bandeau d'inscription personnalisé à partir de la neuvième page consultée, au moment exact où le lecteur est conquis.
Merci pour votre écoute, et je suis ravi de répondre à vos questions.
"""

def clean_for_tts(text):
    t = text
    t = t.replace("%", " pour cent")
    t = t.replace("XGBoost", "X G Boost")
    t = t.replace("LogReg", "Régression Logistique")
    t = t.replace("F1", "F 1")
    t = t.replace("OneHotEncoder", "Ouane Hot Encoder")
    t = t.replace("StandardScaler", "Standard Scaler")
    t = t.replace("ColumnTransformer", "Column Transformer")
    t = t.replace('"', '')
    t = t.replace('«', '')
    t = t.replace('»', '')
    return t

async def main():
    print("=== GÉNÉRATION BLOC 3 : CONVERSION RATE ===")
    
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
    print("=== FIN BLOC 3 ===")

if __name__ == "__main__":
    asyncio.run(main())
