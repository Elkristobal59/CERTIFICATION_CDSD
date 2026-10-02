"""
Script de génération de la fiche prompteur PDF (1 page A4) et de l'audio MP3 (Vivienne)
pour l'oral de soutenance du BLOC 2 : TINDER SPEED DATING.
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

VOICE = "fr-FR-VivienneMultilingualNeural"
RATE = "+4%"

DIR_PROJET = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_2_Analyse_Exploratoire\Tinder")
DIR_REVISION = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\02_BLOC2_TINDER_STEAM")
ALL_AUDIOS_DIR = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\TOUS_LES_AUDIOS_MP3")

HTML_PATH = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_2_TINDER.html"
PDF_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_2_TINDER_SLIDE_PAR_SLIDE.pdf"
PDF_REVISION = DIR_REVISION / "ORAL_SOUTENANCE_BLOC_2_TINDER_SLIDE_PAR_SLIDE.pdf"

MP3_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_2_TINDER.mp3"
MP3_ALL = ALL_AUDIOS_DIR / "ORAL_SOUTENANCE_BLOC_2_TINDER.mp3"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Oral Soutenance — Bloc 2 : Tinder Speed Dating (Prompteur 1 Page)</title>
<style>
  :root {
    --accent-color: #e11d48;
    --accent-bg: #fff1f2;
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
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 3px solid var(--accent-color);
    border-radius: 3px;
    padding: 2px 5px;
    margin-bottom: 3.5px;
    font-size: 6.2pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-tips strong { color: #9f1239; }
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
      BLOC 2 : SPEED DATING & TINDER <span class="tag">RNCP 35288</span>
    </div>
    <div class="header-subtitle">
      Guide d'Oral Slide par Slide — Analyse Exploratoire, Inférentielle & Tests Statistiques
    </div>
  </div>
  <div class="header-meta">
    ÉPREUVE ORALE : 10 MIN (5m Pitch + 5m Q&amp;A)<br>
    Candidat : Christopher Gilleron · 8 Slides
  </div>
</div>

<div class="banner-tips">
  <span>🎯 <strong>Objectif :</strong> Répondre à la question : <em>« Est-ce que ce que les gens déclarent chercher correspond à la réalité de leurs choix ? »</em></span>
  <span>⏱️ <strong>Rythme :</strong> ~35 sec / slide · Posé, dynamique, chiffres clés percutants</span>
</div>

<div class="grid-2">

  <!-- SLIDE 1 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S1</span> Titre &amp; Problématique Métier</div>
      <div class="slide-time">00:00 - 00:30 (30s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Bonjour à tous. Aujourd'hui, je vous présente mon projet sur les données de speed dating. L'idée centrale : <strong>qu'est-ce qui déclenche l'attraction mutuelle</strong> ? Et surtout, est-ce que ce que les célibataires disent chercher correspond à leurs choix réels en face-à-face ? Nous verrons que la réponse réserve de vraies surprises et débouche sur des recommandations produit concrètes pour une application comme <strong>Tinder</strong>. »
      </div>
      <ul class="key-points">
        <li><strong>Enjeu Data :</strong> Confrontation préférences déclarées (en amont) vs décisions réelles (in situ).</li>
        <li><strong>Objectif Business :</strong> Optimiser l'algorithme de matching et le profil utilisateur sur Tinder.</li>
      </ul>
      <div class="box-metric">
        <span>Étude de référence</span>
        <strong>Columbia University · 21 vagues</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 2 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S2</span> Données &amp; Nettoyage Rigoureux</div>
      <div class="slide-time">00:30 - 01:10 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « L'étude porte sur <strong>551 participants</strong> (274 femmes, 277 hommes) lors de 21 soirées, totalisant <strong>8 378 dates de 4 minutes</strong>. Mécanique clé : un participant dit "Oui" dans <strong>42 %</strong> des cas, mais le match réciproque s'effondre à <strong>16,5 %</strong>. Pipeline technique : imputation par la <strong>médiane</strong> pour résister aux notes extrêmes, et correction du piège des vagues 6-9 (notées sur 10) réalignées sur une base 100 points. »
      </div>
      <ul class="key-points">
        <li><strong>Dataset :</strong> 195 variables brutes · Dé-doublonnage à 551 individus pour l'analyse des profils.</li>
        <li><strong>Nettoyage :</strong> Normalisation stricte base 100 points · Zéro distorsion d'échelle.</li>
      </ul>
      <div class="box-metric">
        <span>Taux de Oui : <strong>42,0 %</strong></span>
        <span>Taux de Match Réel : <strong>16,5 %</strong> (x2.5 moins !)</span>
      </div>
    </div>
  </div>

  <!-- SLIDE 3 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S3</span> Préférences Déclarées : Le Grand Écart</div>
      <div class="slide-time">01:10 - 01:50 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Sur 100 points déclarés avant les dates, les hommes allouent <strong>27 % au physique</strong> (+50% vs femmes à 18%). Les femmes mettent l'<strong>intelligence en tête (21 %)</strong>, suivie de la sincérité. Accord parfait sur l'humour (17,5 % chacun). Sur l'ambition, les femmes y consacrent 12,8 % contre 8,8 % pour les hommes. Tests t de Student Welch : écarts physique et ambition <strong>hautement significatifs (p &lt; 0.001)</strong>, humour non significatif. »
      </div>
      <ul class="key-points">
        <li><strong>Déclaratif H :</strong> Physique n°1 (27,2%) &gt; Humour (17,5%) &gt; Intelligence (15,3%).</li>
        <li><strong>Déclaratif F :</strong> Intelligence n°1 (21,0%) &gt; Sincérité (18,4%) &gt; Physique n°3 (18,0%).</li>
      </ul>
      <div class="box-metric">
        <span>Test t Welch Physique : <strong>t = 8.87, p &lt; 0.001</strong></span>
        <span>Humour : <strong>t = 0.52, p = 0.60 (égalitaire)</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 4 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S4</span> Préférences Réelles : Le Réveil Brutal</div>
      <div class="slide-time">01:50 - 02:40 (50s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « En face-à-face, tout bascule : le <strong>physique explose comme prédicteur n°1 universel</strong> avec une corrélation de <strong>r = 0,49</strong> sur la décision, suivi de l'humour à <strong>0,41</strong>. L'intelligence (0,22) et la sincérité (0,21), pourtant plébiscitées par les femmes, s'effondrent. En clair : en date court, on ne valide pas un CV intellectuel ; ce qui déclenche le "Oui", c'est l'attirance visuelle immédiate et la légèreté de l'instant. »
      </div>
      <ul class="key-points">
        <li><strong>Corrélation Décision Réelle :</strong> Physique (r = 0.49) &gt; Humour (r = 0.41) &gt;&gt; Intelligence (r = 0.22).</li>
        <li><strong>Fossé déclaratif/réel :</strong> Le filtre physique prime sur toutes les vertus déclarées.</li>
      </ul>
      <div class="box-metric">
        <span>Corrélation Physique réelle</span>
        <strong>r = 0.49 (Facteur dominant n°1)</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 5 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S5</span> Homophilie : Origine vs Passions</div>
      <div class="slide-time">02:40 - 03:20 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Deux autres facteurs testés : l'origine ethnique et les passions communes. Pour l'origine, le taux de match passe de 16,1 % à 17,1 % (+1 pt) : le <strong>test du Chi-deux est non significatif (p = 0.56)</strong>, c'est du pur hasard. En revanche, pour les centres d'intérêt partagés, le taux bondit de 14,7 % à <strong>19,5 % (+4,8 pts)</strong>. Les passions communes renforcent le match, mais interviennent comme un second filtre après le physique. »
      </div>
      <ul class="key-points">
        <li><strong>Même origine :</strong> +1.0 pt de match · Chi-deux non significatif (pas d'effet communautaire).</li>
        <li><strong>Passions partagées :</strong> +4.8 pts de match · Vrai levier de conversion conversationnelle.</li>
      </ul>
      <div class="box-metric">
        <span>Effet Origine : <strong>Non significatif</strong></span>
        <span>Effet Passions : <strong>+4,8 pts de match gagnés</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 6 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S6</span> Biais Cognitif : Lucidité &amp; Surestimation</div>
      <div class="slide-time">03:20 - 04:00 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Sommes-nous lucides sur notre pouvoir de séduction ? En comparant la note auto-évaluée à la note reçue, le constat est sans appel : <strong>presque tout le monde se surestime</strong>. Les hommes se rajoutent en moyenne <strong>+1,0 point sur 10</strong>, les femmes <strong>+0,8 point</strong>. Presque tous les points se situent sous la diagonale de lucidité. C'est la source de la frustration sur les apps : beaucoup visent des profils hors de portée. »
      </div>
      <ul class="key-points">
        <li><strong>Biais d'auto-évaluation :</strong> Hommes (+1.0 pt / 10) · Femmes (+0.8 pt / 10).</li>
        <li><strong>Impact produit :</strong> Asymétrie des swipes et sentiment de rejet chez les utilisateurs.</li>
      </ul>
      <div class="box-metric">
        <span>Surestimation Hommes : <strong>+1,0 pt / 10</strong></span>
        <span>Surestimation Femmes : <strong>+0,8 pt / 10</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 7 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S7</span> Fatigue Décisionnelle : L'Ordre de Passage</div>
      <div class="slide-time">04:00 - 04:30 (30s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « L'ordre des dates influence-t-il la générosité ? Sur les 3 premiers rendez-vous, le taux de "Oui" est de <strong>43,8 %</strong>. Après 15 dates, il tombe à <strong>40,0 % (-3,8 pts)</strong>. Cela démontre une <strong>fatigue cognitive décisionnelle</strong> : face à l'accumulation de profils, le cerveau sature, devient plus critique et rejette plus facilement. En ligne, le swipe infini produit exactement le même épuisement. »
      </div>
      <ul class="key-points">
        <li><strong>Effet d'épuisement :</strong> Décroissance progressive du taux d'acceptation au fil de la soirée.</li>
        <li><strong>Parallèle appli :</strong> Le scrolling infini détruit la valeur perçue des profils rencontrés.</li>
      </ul>
      <div class="box-metric">
        <span>Début (dates 1-3) : <strong>43,8 %</strong></span>
        <span>Fin (&gt; 15 dates) : <strong>40,0 % (-3,8 pts)</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 8 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S8</span> Recommandations Produit pour Tinder</div>
      <div class="slide-time">04:30 - 05:00 (30s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Trois recommandations business pour Tinder : <strong>1. Ignorer les questionnaires déclaratifs</strong> et optimiser l'algorithme sur les actes réels (temps d'arrêt sur photo, swipe). <strong>2. Miser sur la qualité photo par IA</strong> (Smart Photos, cadrage, éclairage) car le visuel pèse 50 % de la décision. <strong>3. Limiter le swipe compulsif</strong> (packs de 10-15 profils) pour contrer la fatigue décisionnelle et valoriser les passions communes. »
      </div>
      <ul class="key-points">
        <li><strong>Axe 1 - Algorithme :</strong> Remplacer les filtres texte par le comportement d'interaction effectif.</li>
        <li><strong>Axe 2 - Qualité visuelle :</strong> Accompagnement IA du choix de la première photo.</li>
        <li><strong>Axe 3 - UX &amp; Rétention :</strong> Casser le swipe infini pour rehausser le taux de match effectif.</li>
      </ul>
      <div class="box-metric">
        <span>Bilan</span>
        <strong>Data-driven matchmaking · Rétention utilisateur accrue</strong>
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

SPEECH_TEXT = """Bonjour à tous. Aujourd'hui, je vous présente mon projet pour le Bloc 2 sur les données de speed dating.

L'idée centrale de ce travail, c'est de répondre à une vraie question humaine et business : qu'est-ce qui fait qu'on se plaît vraiment ? Et surtout, est-ce que ce que les gens disent chercher correspond à la réalité de leurs choix quand ils rencontrent quelqu'un ? On va voir que la réponse réserve pas mal de surprises, et qu'elle permet de donner des recommandations très concrètes pour une application comme Tinder.

Sur la deuxième slide, on pose le cadre et les données.
Nous travaillons sur une étude menée par l'Université de Columbia avec 551 participants, 274 femmes et 277 hommes, répartis sur 21 soirées de speed dating. Au total, cela représente 8 378 rendez-vous en face-à-face de 4 minutes.
Pour vous donner un ordre d'idée de la mécanique des rencontres : individuellement, un participant dit Oui dans 42 % des cas. Mais pour qu'il y ait un vrai match, il faut que les deux personnes disent Oui en même temps. Et là, le chiffre tombe à 16,5 %. C'est deux fois et demie moins !
Côté technique, j'ai construit un pipeline de nettoyage en Python. Il y avait 195 colonnes et pas mal de données manquantes. Pour les combler proprement, j'ai utilisé la médiane plutôt que la moyenne, pour ne pas être faussé par des notes extrêmes. Et surtout, j'ai corrigé un gros piège dans les données : sur certaines soirées, les organisateurs avaient changé le barème en demandant une note de 1 à 10 au lieu de répartir 100 points. J'ai donc tout recalculé sur une base 100 pour que tous les participants soient parfaitement comparables.

Sur la troisième slide, on regarde ce que les hommes et les femmes déclarent chercher avant même de commencer les rendez-vous.
On leur a demandé de répartir 100 points sur six critères : le physique, l'intelligence, la sincérité, l'humour, l'ambition, et le fait d'avoir des centres d'intérêt communs.
Le premier gros écart, c'est le physique : les hommes y consacrent plus de 27 % de leur budget, alors que les femmes n'y mettent que 18 %. C'est 50 % de plus chez les hommes !
Les femmes, de leur côté, mettent l'intelligence en tête à 21 %, suivie de près par la sincérité.
En revanche, les deux sont parfaitement d'accord sur l'humour : autour de 17,5 % chacun. Enfin, sur l'ambition, les femmes y consacrent près de 13 %, alors que les hommes la relèguent au dernier rang à moins de 9 %. Les tests té de Student confirment que les écarts sur le physique et l'ambition sont hautement significatifs, avec une p-value minuscule inférieure à 0,001, alors que sur l'humour, la différence est purement due au hasard.

Sur la quatrième slide, on arrive au cœur de l'analyse : est-ce que les gens font vraiment ce qu'ils disent ?
Et là, c'est le grand écart. Quand on regarde les décisions réelles à la fin des 4 minutes de date, la hiérarchie change du tout au tout.
Le physique, que les femmes ne plaçaient qu'en troisième position derrière l'intelligence et la sincérité, explose complètement dans la réalité : il a une corrélation de 0,49 avec la décision de revoir l'autre, suivi par l'humour à 0,41.
À l'inverse, l'intelligence et la sincérité, que les femmes mettaient en avant dans les questionnaires, s'effondrent avec des corrélations de seulement 0,22 et 0,21.
En clair : dans un échange court, ce n'est pas le CV intellectuel qui déclenche le coup de cœur. Ce qui fait dire Oui, c'est d'abord l'attirance visuelle et le fait de passer un moment léger et marrant.

Sur la cinquième slide, on s'est posé deux autres questions : est-ce qu'on matche plus avec quelqu'un de la même origine ethnique, ou avec quelqu'un qui partage nos passions ?
Pour l'origine ethnique, le résultat est très net : être de la même origine ne fait passer le taux de match que de 16,1 % à 17,1 %. C'est un tout petit point d'écart, et mon test statistique du Chi-deux montre que ce n'est pas significatif, c'est juste du hasard.
Pour les passions communes en revanche, ça joue vraiment : passer de goûts très opposés à des passions très proches fait monter le taux de match de 14,7 % à 19,5 %, soit un gain de 4,8 points. C'est un vrai coup de pouce, même s'il arrive après le filtre physique.

Sur la sixième slide, on a regardé si les participants sont lucides sur leur propre pouvoir de séduction.
On a comparé la note physique que chacun s'est attribuée avec la note moyenne que ses partenaires lui ont réellement donnée pendant la soirée.
Le constat est sans appel : presque tout le monde se surestime. Les hommes se rajoutent en moyenne 1 point complet sur 10, et les femmes se rajoutent 0,8 point. Sur notre graphique, presque tous les points sont en dessous de la diagonale de lucidité. Personne ou presque ne se sous-estime. Et c'est un point clé pour comprendre la frustration sur les applis : beaucoup d'utilisateurs visent des profils hors de portée parce qu'ils se voient plus séduisants qu'ils ne le sont perçus par les autres.

Sur la septième slide, on a étudié l'effet de l'ordre de passage au cours de la soirée.
Est-ce qu'on dit plus facilement Oui au début ou à la fin quand on commence à être fatigué ?
La réponse, c'est qu'on devient plus difficile. Sur les 3 premiers rendez-vous, le taux de Oui est de 43,8 %. Mais après 15 rendez-vous, il descend à 40,0 %, soit une baisse de 3,8 points. Ce n'est pas un effondrement, mais ça montre bien une fatigue de décision : après avoir parlé à 15 inconnus, on est saturé, plus blasé, et on dit Non plus facilement.

Enfin, sur la huitième slide, voici ce que Tinder doit retenir de tout ça :
Premièrement : ne basez pas votre algorithme sur ce que les gens cochent dans leur profil. Fiez-vous uniquement à leurs actes : sur quelles photos ils s'arrêtent, combien de secondes ils regardent un profil, et qui ils swipent en vrai.
Deuxièmement : puisque le visuel représente la moitié de la décision, investissez sur la qualité des photos. Utilisez de l'intelligence artificielle pour aider les utilisateurs à choisir leur meilleur cliché, avec un bon éclairage et sans lunettes de soleil.
Et troisièmement : aidez les utilisateurs à calibrer leurs attentes et limitez le nombre de profils qu'on peut swiper d'un coup pour éviter la fatigue cognitive.

Merci pour votre attention, je suis maintenant à votre disposition pour vos questions.
"""

def clean_for_tts(text):
    t = text
    t = t.replace("%", " pour cent")
    t = t.replace("Chi-deux", "Chi deux")
    t = t.replace("test té", "test t")
    t = t.replace("test t de Student", "test té de Student")
    t = t.replace("p-value", "p value")
    t = t.replace("r =", "r égale")
    t = t.replace("t =", "t égale")
    t = t.replace("< 0.001", "inférieure à zéro virgule zéro zéro un")
    t = t.replace("=", "égale")
    t = t.replace('"', '')
    t = t.replace('«', '')
    t = t.replace('»', '')
    return t

async def main():
    print("=== GÉNÉRATION BLOC 2 : TINDER SPEED DATING ===")
    
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
        
    # Copie révision
    DIR_REVISION.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(PDF_PROJET, PDF_REVISION)
    print(f"[COPIE] PDF copié vers {PDF_REVISION}")

    # 3. Génération Audio MP3 via edge-tts (Vivienne)
    print("\n[AUDIO] Synthèse vocale avec Vivienne (fr-FR-VivienneMultilingualNeural)...")
    cleaned_speech = clean_for_tts(SPEECH_TEXT)
    communicate = edge_tts.Communicate(cleaned_speech, VOICE, rate=RATE)
    await communicate.save(str(MP3_PROJET))
    print(f"[OK] MP3 généré : {MP3_PROJET} ({MP3_PROJET.stat().st_size / 1024:.1f} Ko)")
    
    shutil.copy2(MP3_PROJET, MP3_ALL)
    print(f"[COPIE] MP3 copié vers {MP3_ALL}")
    print("=== FIN BLOC 2 ===")

if __name__ == "__main__":
    asyncio.run(main())
