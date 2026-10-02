"""
Script de génération de la fiche prompteur PDF (1 page A4) et de l'audio MP3 (Vivienne)
pour l'oral de soutenance du BLOC 4 : AT&T SMS SPAM DETECTOR.
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

DIR_PROJET = Path(r"D:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_4_ATT_Spam_Detector")
DIR_REVISION = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\04_BLOC4_ATT_SPAM")
ALL_AUDIOS_DIR = Path(r"D:\CODE JEDHA\PROJETS\REVISIONS\TOUS_LES_AUDIOS_MP3")

HTML_PATH = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_4_ATT_SPAM.html"
PDF_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_4_ATT_SPAM_SLIDE_PAR_SLIDE.pdf"
PDF_REVISION = DIR_REVISION / "ORAL_SOUTENANCE_BLOC_4_ATT_SPAM_SLIDE_PAR_SLIDE.pdf"

MP3_PROJET = DIR_PROJET / "ORAL_SOUTENANCE_BLOC_4_ATT_SPAM.mp3"
MP3_ALL = ALL_AUDIOS_DIR / "ORAL_SOUTENANCE_BLOC_4_ATT_SPAM.mp3"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Oral Soutenance — Bloc 4 : AT&T SMS Spam Detector (Prompteur 1 Page)</title>
<style>
  :root {
    --accent-color: #0284c7;
    --accent-bg: #eff6ff;
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
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 3px solid var(--accent-color);
    border-radius: 3px;
    padding: 2px 5px;
    margin-bottom: 3.5px;
    font-size: 6.2pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-tips strong { color: #1e40af; }
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
      BLOC 4 : AT&amp;T SMS SPAM DETECTOR <span class="tag">RNCP 35288</span>
    </div>
    <div class="header-subtitle">
      Guide d'Oral Slide par Slide — Deep Learning &amp; NLP Séquentiel (Bi-LSTM, Keras, Embedding)
    </div>
  </div>
  <div class="header-meta">
    ÉPREUVE ORALE : 10 MIN (5m Pitch + 5m Q&amp;A)<br>
    Candidat : Christopher Gilleron · 8 Slides
  </div>
</div>

<div class="banner-tips">
  <span>🎯 <strong>Objectif :</strong> Détecter le smishing/spam avec asymétrie des coûts : zéro faux positif garanti sur les SMS légitimes.</span>
  <span>⏱️ <strong>Rythme :</strong> ~35 sec / slide · Rigueur réseau de neurones &amp; impact télécom</span>
</div>

<div class="grid-2">

  <!-- SLIDE 1 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S1</span> Contexte Métier &amp; Enjeux Télécom AT&amp;T</div>
      <div class="slide-time">00:00 - 00:35 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Bonjour à tous. Aujourd'hui, je vous présente notre projet de Deep Learning NLP pour l'opérateur télécom <strong>AT&amp;T</strong>. Le sujet : le <strong>smishing</strong> (phishing par SMS). Chez un opérateur, les coûts d'erreurs sont <strong>totalement asymétriques</strong> : rater un spam est un désagrément mineur ; bloquer par erreur un SMS légitime (code bancaire, RDV médical) est une rupture de service critique. Mission : un filtre séquentiel chirurgical à zéro faux positif. »
      </div>
      <ul class="key-points">
        <li><strong>Client Métier :</strong> AT&amp;T (filtrage de flux SMS temps réel).</li>
        <li><strong>Contrainte Industrielle :</strong> Asymétrie des coûts (tolérance zéro pour les faux positifs).</li>
      </ul>
      <div class="box-metric">
        <span>Faux Positif (Code bancaire bloqué)</span>
        <strong>Impact critique / Inacceptable</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 2 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S2</span> Exploration du Corpus &amp; Asymétrie</div>
      <div class="slide-time">00:35 - 01:15 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Notre étude repose sur <strong>5 572 SMS réels en anglais</strong>. Deux traits majeurs : <strong>1. Déséquilibre de classe :</strong> 86,6 % de messages légitimes (hams) contre 13,4 % de spams (1 spam pour 6,5 hams). <strong>2. Typologie contrastée :</strong> hams courts et familiers vs spams longs, alarmistes (win, claim, urgent), liens suspects et numéros surtaxés. Split stratifié 80/20 : 4 457 SMS train / 1 115 test conservant le ratio 13,4 %. »
      </div>
      <ul class="key-points">
        <li><strong>Dataset :</strong> 5 572 SMS annotés (86,6% légitimes / 13,4% spams).</li>
        <li><strong>Split :</strong> Stratification stricte 80/20 (1 115 SMS de test indépendant).</li>
      </ul>
      <div class="box-metric">
        <span>Hams (Légitimes) : <strong>86,6 %</strong></span>
        <span>Spams (Menaces) : <strong>13,4 %</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 3 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S3</span> Baseline Machine Learning (TF-IDF)</div>
      <div class="slide-time">01:15 - 01:50 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pour étalonner nos gains, baseline solide en ML classique : vectorisation <strong>TF-IDF</strong> et Régression Logistique. Elle donne 97,2 % d'accuracy et F1 = 0,885 sur les spams. Mais elle a une <strong>limite structurelle majeure : le sac de mots</strong>. Le TF-IDF ignore l'ordre syntaxique et le contexte. Or, <em>« Je ne suis pas une arnaque »</em> et <em>« Arnaque, je ne suis pas »</em> ont les mêmes mots mais pas la même intention. D'où le passage au Deep Learning séquentiel. »
      </div>
      <ul class="key-points">
        <li><strong>Baseline ML :</strong> TF-IDF + LogisticRegression (F1 = 0.885).</li>
        <li><strong>Limite sac de mots :</strong> Insensible à la syntaxe, la négation et la proximité temporelle.</li>
      </ul>
      <div class="box-metric">
        <span>F1 Spam Baseline : <strong>0,885</strong></span>
        <span>Limite : <strong>Perte de la structure séquentielle</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 4 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S4</span> Préparation Textuelle : Tokenisation &amp; Padding</div>
      <div class="slide-time">01:50 - 02:25 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pipeline de prétraitement Keras en deux étapes : <strong>1. Tokenisation :</strong> vocabulaire des 10 000 mots les plus fréquents, chaque mot reçoit un index entier, token spécial <code>&lt;OOV&gt;</code> pour les mots inconnus en prod. <strong>2. Padding :</strong> dimension fixe de 100 tokens (<code>pad_sequences</code>) avec padding à zéros. 100 tokens couvrent la totalité des SMS réels sans perte de signal utile, transformant le texte brut en tenseurs numériques fixes. »
      </div>
      <ul class="key-points">
        <li><strong>Tokenizer :</strong> Vocabulaire 10 000 mots + Token Out-Of-Vocabulary (&lt;OOV&gt;).</li>
        <li><strong>Padding :</strong> Longueur fixe maxlen = 100 tokens (Tenseurs Keras normalisés).</li>
      </ul>
      <div class="box-metric">
        <span>Vocabulaire : <strong>10 000 tokens</strong></span>
        <span>Longueur séquence : <strong>100 tokens</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 5 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S5</span> Architecture Deep Learning : Bi-LSTM</div>
      <div class="slide-time">02:25 - 03:10 (45s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Notre réseau compte 5 couches (338 753 paramètres) : <strong>1. Embedding dense dim 32</strong> (les mots proches comme free et win se regroupent dans l'espace continu). <strong>2. Bidirectional LSTM 32 unités</strong> (résout l'évanouissement du gradient via 3 portes : oubli, entrée, sortie, et lit le SMS dans les 2 sens). <strong>3. Dense 32 ReLU</strong>. <strong>4. Dropout 20 %</strong> anti-overfitting. <strong>5. Dense 1 Sigmoïde</strong> délivrant la probabilité de spam entre 0 et 1. »
      </div>
      <ul class="key-points">
        <li><strong>Embedding :</strong> Projection continue 32D (sémantique partagée).</li>
        <li><strong>Bi-LSTM :</strong> Contexte bidirectionnel + 3 portes de régulation mémorielle.</li>
      </ul>
      <div class="box-metric">
        <span>Paramètres entraînables</span>
        <strong>338 753 paramètres (Inférence CPU &lt; 5ms)</strong>
      </div>
    </div>
  </div>

  <!-- SLIDE 6 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S6</span> Entraînement &amp; Convergence Propre</div>
      <div class="slide-time">03:10 - 03:50 (40s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Entraînement rigoureux : fonction de perte <strong>Binary Crossentropy</strong>, optimiseur <strong>Adam (lr = 0,001)</strong> avec momentum. Régularisation par <strong>EarlyStopping (patience 3)</strong> surveillant la perte de validation avec restauration automatique des meilleurs poids. Résultat : convergence ultra-rapide, val_loss minimale à <strong>0,045 dès l'epoch 2</strong>, arrêt net à l'epoch 5 sans aucun surapprentissage. »
      </div>
      <ul class="key-points">
        <li><strong>Optimisation :</strong> Adam + Binary Crossentropy (pénalisation logarithmique).</li>
        <li><strong>Anti-Overfitting :</strong> Dropout 20% + EarlyStopping (restauration meilleurs poids).</li>
      </ul>
      <div class="box-metric">
        <span>Perte validation minimale : <strong>0,045 (Epoch 2)</strong></span>
        <span>Arrêt précoce : <strong>Epoch 5</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 7 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S7</span> Évaluation &amp; Performance sur Test Set</div>
      <div class="slide-time">03:50 - 04:25 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Sur les 1 115 SMS du test set indépendant : notre Bi-LSTM atteint une <strong>accuracy globale de 98,7 %</strong> (+1,4 pt vs baseline) et un <strong>F1-Score spam de 0,891</strong>. Matrice de confusion à seuil standard 0,50 : sur les 149 spams réels, le modèle en intercepte 122 (rappel 82 %) pour seulement 3 faux positifs sur 966 hams. La mémoire séquentielle capture les formulations complexes et masquées que le TF-IDF manquait. »
      </div>
      <ul class="key-points">
        <li><strong>Accuracy Test :</strong> 98,7 % (+1,4 pt vs TF-IDF Baseline).</li>
        <li><strong>Matrice de confusion :</strong> 122/149 spams arrêtés · Seulement 3 faux positifs.</li>
      </ul>
      <div class="box-metric">
        <span>F1 Spam Bi-LSTM : <strong>0,891</strong></span>
        <span>Accuracy Globale : <strong>98,7 %</strong></span>
      </div>
    </div>
  </div>

  <!-- SLIDE 8 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title"><span class="num">S8</span> Déploiement Industriel &amp; Seuil Asymétrique</div>
      <div class="slide-time">04:25 - 05:00 (35s)</div>
    </div>
    <div class="slide-body">
      <div class="speech-prompt">
        « Pour satisfaire l'exigence d'AT&amp;T, en production nous réglons le <strong>seuil décisionnel à 0,85-0,90</strong> : cela garantit <strong>ZÉRO faux positif</strong> (aucun SMS légitime n'est jamais bloqué). Les messages suspects (probabilité entre 0,50 et 0,85) sont dirigés vers le dossier Indésirables avec bandeau d'alerte sans suppression brutale. Déploiement : application Streamlit interactive sur le port 8501 avec jauge temps réel. »
      </div>
      <ul class="key-points">
        <li><strong>Seuil Asymétrique :</strong> Rehaussé à 0.85 &rarr; Zéro faux positif critique.</li>
        <li><strong>Zone Grise [0.50 - 0.85] :</strong> Notification préventive sans blocage destructif.</li>
      </ul>
      <div class="box-metric">
        <span>Production AT&amp;T</span>
        <strong>Politique asymétrique · Streamlit Port 8501</strong>
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

SPEECH_TEXT = """Bonjour à tous. Aujourd'hui, je vous présente notre projet de Deep Learning appliqué au traitement du langage naturel, réalisé pour l'opérateur de télécommunications A T et T.
Le sujet est brûlant : c'est la prolifération du smishing, ces tentatives d'escroquerie et de phishing par SMS où des fraudeurs usurpent l'identité de banques, de services de livraison ou d'organismes publics pour dérober des données personnelles ou de l'argent.
Pour un opérateur télécom comme A T et T, il y a une contrainte industrielle majeure : le coût des erreurs est complètement asymétrique.
Si un spam passe entre les mailles du filet, l'abonné le supprime : c'est un désagrément mineur.
En revanche, si notre filtre bloque par erreur un SMS authentique, comme un code bancaire de validation ou une confirmation de rendez-vous médical, l'impact est catastrophique pour le client et pour l'image de marque de l'opérateur.
Notre mission : bâtir un modèle séquentiel de Deep Learning capable d'intercepter les spams avec une précision chirurgicale, sans jamais bloquer un SMS légitime.

Slide 2 : Exploration du corpus et asymétrie des coûts.
Notre étude s'appuie sur un jeu de données de référence de 5 572 SMS réels en anglais.
Ce corpus présente deux caractéristiques clés :
D'abord, un déséquilibre de classe marqué : 86,6 pour cent de messages légitimes, ce qu'on appelle les hams, et 13,4 pour cent de spams. Soit environ 1 spam pour 6 messages et demi légitimes.
Ensuite, des formats très contrastés : les messages légitimes sont souvent courts et familiers, tandis que les spams sont plus longs, bourrés de promesses de gains, d'appels à l'action urgents, de numéros surtaxés et de liens hypertextes.
Nous avons séparé les données en 80 pour cent pour l'entraînement, soit 4 457 SMS, et 20 pour cent pour le test, soit 1 115 SMS, en appliquant un découpage stratifié pour conserver scrupuleusement la proportion de 13,4 pour cent de spams dans les deux ensembles.

Slide 3 : Baseline Machine Learning et limites du sac de mots.
Avant de lancer un réseau de neurones profond, nous avons posé une baseline solide en Machine Learning classique : une vectorisation T F - I D F combinée à une régression logistique.
Cette baseline donne des résultats honorables : 97,2 pour cent de précision globale et un F 1 Score de 0,885 sur les spams, avec un seul faux positif sur les 966 messages légitimes du test.
Mais elle a une limite structurelle majeure : le T F - I D F traite les SMS comme un sac de mots. Il compte les fréquences de mots de façon totalement désordonnée. Or, dans un SMS, l'ordre et le contexte font toute la différence. La phrase « Je ne suis pas une arnaque » et « Arnaque, je ne suis pas » ont exactement les mêmes mots, mais pas du tout la même intention. Pour comprendre la syntaxe et les relations temporelles, il faut passer au Deep Learning séquentiel.

Slide 4 : Préparation textuelle Keras, tokenisation et padding.
Pour préparer le texte brut à entrer dans un réseau de neurones, nous avons conçu un pipeline Keras en deux étapes :
Premièrement, la tokenisation : nous construisons un dictionnaire des 10 000 mots les plus fréquents. Chaque mot reçoit un index entier unique. Les mots rares ou inconnus en production sont automatiquement remplacés par un token spécial O O V pour Out Of Vocabulary.
Deuxièmement, le padding : un réseau de neurones réclame des tenseurs de dimensions fixes en entrée. Nous avons donc fixé une longueur de séquence à 100 tokens. Les SMS plus courts sont complétés par des zéros, et les SMS plus longs sont tronqués à la fin. 100 tokens permettent de couvrir la quasi-totalité des SMS sans perte d'information utile.

Slide 5 : Architecture Deep Learning, Bi-LSTM et Embedding.
Notre architecture séquentielle a été pensée pour capturer toute la richesse du texte :
Couche 1 : Une couche d'Embedding de dimension 32. Contrairement au codage ouane hot qui crée des vecteurs creux et froids, l'embedding projette chaque mot dans un espace vectoriel dense où les mots sémantiquement proches comme free, win et prize se regroupent naturellement.
Couche 2 : Un L S T M Bidirectionnel de 32 unités, soit 64 caractéristiques en sortie. Les cellules L S T M résolvent le problème de l'évanouissement du gradient grâce à leur mémoire interne régie par trois portes : oubli, entrée et sortie. La bidirectionnalité permet au réseau de lire chaque SMS de gauche à droite, mais aussi de droite à gauche, pour comprendre le contexte complet d'un mot par rapport à ce qui le précède et ce qui le suit.
Couches 3 et 4 : Une couche dense de 32 neurones avec activation Re L U, suivie d'un Dropout à 20 pour cent pour casser les co-adaptations entre neurones et éviter le surapprentissage.
Couche 5 : Un neurone unique de sortie avec activation sigmoïde, qui délivre directement la probabilité que le SMS soit un spam, entre 0 et 1. Au total, le modèle compte 338 753 paramètres entraînables.

Slide 6 : Entraînement et convergence.
Pour l'entraînement, nous avons combiné les meilleures pratiques :
La fonction de perte retenue est la Binary Crossentropy, la référence absolue pour pénaliser les mauvaises prédictions de probabilité.
L'optimiseur est Adam avec un taux d'apprentissage de 0,001, combinant le momentum et l'adaptation individuelle des pas de gradient.
Pour garantir une généralisation parfaite, nous avons intégré un callback d'Early Stopping avec une patience de 3 epochs sur la perte de validation, avec restauration automatique des meilleurs poids.
Résultat : le modèle converge très vite. Dès la deuxième epoch, la perte de validation atteint son minimum à 0,045, et l'entraînement s'arrête proprement à l'epoch 5 sans jamais entrer en surapprentissage.

Slide 7 : Évaluation et performance sur le jeu de test.
Sur le jeu de test indépendant de 1 115 messages réels :
Notre réseau B i - L S T M atteint une précision globale de 98,7 pour cent et fait grimper le F 1 Score des spams à 0,891.
En regardant la matrice de confusion à seuil standard de 0,50 : sur les 149 spams du jeu de test, le modèle en détecte 122 avec succès, soit un rappel de près de 82 pour cent, tout en ne générant que 3 faux positifs sur les 966 messages légitimes.
Par rapport à la baseline, le Deep Learning fait gagner 1,4 point de précision et attrape des spams plus subtils et mieux déguisés grâce à sa mémoire séquentielle.

Slide 8 : Déploiement industriel et seuil asymétrique.
Pour répondre à l'exigence industrielle d'A T et T, nous ne laissons pas le seuil à 0,50 en production.
En relevant le seuil de décision à 0,85 ou 0,90, nous passons en mode zéro faux positif garanti : aucun SMS légitime n'est jamais bloqué. Les messages suspects entre 0,50 et 0,85 peuvent alors être redirigés vers un dossier indésirables sur le téléphone de l'abonné avec un bandeau d'alerte, plutôt que d'être supprimés unilatéralement.
Le modèle et le tokenizer ont été sérialisés pour être intégrés dans une démonstration interactive en temps réel sous Streamlit sur le port 8501.
Merci pour votre écoute, et je réponds avec plaisir à vos questions.
"""

def clean_for_tts(text):
    t = text
    t = t.replace("%", " pour cent")
    t = t.replace("TF-IDF", "T F - I D F")
    t = t.replace("Bi-LSTM", "B i - L S T M")
    t = t.replace("LSTM", "L S T M")
    t = t.replace("F1", "F 1")
    t = t.replace("ReLU", "Re L U")
    t = t.replace("OOV", "O O V")
    t = t.replace("lr = 0,001", "learning rate de zéro virgule zéro zéro un")
    t = t.replace('"', '')
    t = t.replace('«', '')
    t = t.replace('»', '')
    return t

async def main():
    print("=== GÉNÉRATION BLOC 4 : AT&T SMS SPAM DETECTOR ===")
    
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
    print("=== FIN BLOC 4 ===")

if __name__ == "__main__":
    asyncio.run(main())
