# 🎓 Soutenance Bloc 2 : Speed Dating & Tinder — Questions & Réponses du Jury

> **Fiche Maître de Préparation Orale (CDSD — RNCP 35288)**  
> **Candidat :** Christopher GILLERON  
> **Projet Soutenu :** Tinder / Speed Dating (Université de Columbia)  
> **Format Oral :** 10 minutes (5 min Pitch + 5 min Q&A)  
> **Fichiers associés :** `Tinder_speed_dating.ipynb` · `Tinder_presentation.pptx` · `ORAL_SOUTENANCE_BLOC_2_TINDER_SLIDE_PAR_SLIDE.pdf`

---

## 🧭 Sommaire
1. [Le Storytelling Métier en 5 Questions](#1-le-storytelling-métier-en-5-questions)
2. [Boîte à Outils : Les Librairies Python & Pourquoi ces Choix](#2-boîte-à-outils--les-librairies-python--pourquoi-ces-choix)
3. [Prétraitement & Contrôle d'Intégrité des Données (Slide 2)](#3-prétraitement--contrôle-dintégrité-des-données-slide-2)
   - [Pourquoi dédoublonner les profils (551 vs 8 378) ?](#a-pourquoi-dédoublonner-les-profils-551-vs-8-378)
   - [Traitement des valeurs manquantes & Imputation par la médiane](#b-traitement-des-valeurs-manquantes--imputation-par-la-médiane)
   - [Qu'est-ce qu'un contrôle d'intégrité ? Le piège des vagues 6 à 9](#c-quest-ce-quun-contrôle-dintégrité--le-piège-des-vagues-6-à-9)
4. [Rigueur Statistique & Inférence Mathématique](#4-rigueur-statistique--inférence-mathématique)
   - [Corrélation de Pearson (r)](#a-corrélation-de-pearson-r)
   - [Test t de Student de Welch](#b-test-t-de-student-de-welch)
   - [Test du Chi-deux d'indépendance (χ²)](#c-test-du-chi-deux-dindépendance-χ)
   - [Étude d'ordre et fatigue décisionnelle](#d-étude-dordre-et-fatigue-décisionnelle)
5. [Audit du Notebook : Les Calculs et Graphiques HD y sont-ils ?](#5-audit-du-notebook--les-calculs-et-graphiques-hd-y-sont-ils)
6. [Questions Pièges & Réponses Tactiques du Candidat](#6-questions-pièges--réponses-tactiques-du-candidat)

---

## 1. Le Storytelling Métier en 5 Questions

Pour capter le jury dès les premières secondes, l'ensemble du projet est articulé autour d'une colonne vertébrale narrative en **5 questions concrètes** qui font le pont entre la psychologie humaine et le business de Tinder :

```
             ┌────────────────────────────────────────────────────────┐
             │       LE STORYTELLING EN 5 QUESTIONS MÉTIER            │
             └────────────────────────────────────────────────────────┘
                                          │
    ┌─────────────────────────────────────┼─────────────────────────────────────┐
    ▼                                     ▼                                     ▼
[ Q1. Que cherchent-ils ? ]    [ Q2. Que font-ils en vrai ? ]    [ Q3. Homophilie ? ]
Déclarations sur 100 pts :      Le réveil brutal : le physique    Origine ethnique (hasard)
H = Physique (+50%)             devient n°1 (r = 0,49),           vs Passions partagées
F = Intelligence & Sincérité   l'intelligence s'effondre.        (+4,8 pts de match).
    │                                     │
    └──────────────────┬──────────────────┘
                       ▼                                     ▼
         [ Q4. Sont-ils lucides ? ]            [ Q5. La fatigue de l'ordre ? ]
         Surestimation générale :              Baisse des "Oui" au fil du temps
         H (+1,0 pt) et F (+0,8 pt).           (43,8% début vs 40,0% fin) :
         Source de la frustration.             L'effet du swipe compulsif.
                       │
                       ▼
         [ CONCLUSION & RECOMMANDATIONS ]
         1. Algorithme basé sur les actes réels (zéro déclaratif).
         2. IA d'assistance photo (le visuel pèse 50% du choix).
         3. Limiter le swipe continu pour protéger la prise de décision.
```

---

## 2. Boîte à Outils : Les Librairies Python & Pourquoi ces Choix

| Librairie | Import exact | Rôle précis dans le projet | Pourquoi ce choix (Justification Jury) |
| :--- | :--- | :--- | :--- |
| **pandas** | `import pandas as pd` | Manipulation de la table (8 378 lignes, 195 variables), nettoyage, groupements (`groupby`), jointures (`concat`), dé-doublonnage (`iid.nunique()`), discrétisation (`pd.cut`). | C'est le standard de l'industrie pour les données tabulaires hétérogènes. Sa syntaxe vectorisée permet d'exécuter les agrégations de moyennes et de taux de match en quelques millisecondes. |
| **numpy** | `import numpy as np` | Calculs mathématiques vectorisés, masques booléens (`mask = total > 0`), gestion des valeurs nulles (`np.nan`). | Optimisé en C sous le capot, numpy garantit que les opérations sur les colonnes ne souffrent d'aucun surcoût mémoire par rapport à des boucles Python natives. |
| **matplotlib.pyplot** | `import matplotlib.pyplot as plt` | Contrôle fin du layout graphique (`subplots`), gestion de la résolution (`figure.dpi = 100`), étiquetage des axes, rotation des ticks, ajout des labels textuels sur les barres. | Indispensable pour personnaliser la mise en page, gérer des figures à deux panneaux côte-à-côte et tracer la diagonale de référence ($y=x$) sur le graphique de lucidité. |
| **seaborn** | `import seaborn as sns` | Thématique visuelle moderne (`sns.set_theme(style='whitegrid', context='talk')`), palette contrastée, scatterplot avec séparation par couleur (`hue='Genre'`). | Seaborn génère des graphiques statistiques "publication-ready" avec gestion automatique des légendes et des distributions, évitant le rendu austère par défaut de matplotlib. |
| **scipy.stats** | `import scipy.stats as stats` | Fonctions statistiques inférentielles : test t de Student indépendant (`stats.ttest_ind`), test du Chi-deux (`stats.chi2_contingency`), corrélations de Pearson (`stats.pearsonr`). | Fournit les calculs mathématiques exacts des statistiques de test ($t$, $\chi^2$) et des $p$-values associées, indispensable pour valider scientifiquement qu'un écart n'est pas dû au hasard. |

---

## 3. Prétraitement & Contrôle d'Intégrité des Données (Slide 2)

### A. Pourquoi dédoublonner les profils (551 vs 8 378) ?
* **Le problème du tableau brut :** Le fichier `Speed+Dating+Data.csv` compte **8 378 lignes**. Chaque ligne représente **1 rendez-vous individuel** entre un participant (`iid`) et un partenaire (`pid`).
* **Le biais de surpondération d'échantillonnage :** Le nombre de participants par soirée n'était pas constant (certaines vagues comptaient 20 personnes, d'autres seulement 10). 
  * Un individu ayant participé à une soirée de 20 personnes apparaît **20 fois** dans le fichier brut.
  * Un individu ayant participé à une soirée de 10 personnes n'apparaît que **10 fois**.
* **La règle méthodologique :** Si l'on calcule les moyennes des critères déclarés sur les 8 378 lignes, les participants des grandes soirées pèsent **deux fois plus lourd** dans la moyenne que ceux des petites soirées !
* **La solution dans le code :**
  ```python
  prefs = df_clean.dropna(subset=cols_stated).groupby(['iid', 'gender'])[cols_stated].first().reset_index()
  ```
  On dé-doublonne pour n'avoir qu'**une seule ligne par participant unique**. On obtient exactement **551 individus (274 femmes et 277 hommes)**. Chaque participant a ainsi exactement le même poids statistique.

---

### B. Traitement des valeurs manquantes & Imputation par la médiane
* **Pourquoi la médiane plutôt que la moyenne ?**
  1. **Insensibilité aux valeurs extrêmes (Robustesse) :** La moyenne arithmétique est fortement déformée par les notes extrêmes ($0$ ou $10$) attribuées par des participants énervés ou excessivement enthousiastes. La médiane correspond au 50ᵉ centile : elle sépare l'échantillon en deux moitiés égales et reste parfaitement stable face aux outliers.
  2. **Nature des données :** Les notes d'évaluation attribuées lors d'un date sont des variables ordinales discrètes de 1 à 10. Les distributions sont souvent asymétriques (skewed) ; la médiane est alors l'indicateur de tendance centrale le plus fidèle à la réalité du comportement humain.

---

### C. Qu'est-ce qu'un contrôle d'intégrité ? Le piège des vagues 6 à 9
Un **contrôle d'intégrité** est l'étape où le Data Scientist vérifie que les données brutes respectent scrupuleusement les règles du protocole expérimental et ne contiennent pas de contradictions mathématiques.

Dans ce dataset, il y avait un **piège majeur d'hétérogénéité d'échelle** documenté dans le fichier `Speed_dating_data_key.doc` :
* **Vagues 1 à 5 et 10 à 21 :** Les participants devaient répartir un budget total de **100 points** entre les 6 critères (ex: 30 physique, 20 intelligence, 20 humour, 10 sincérité, 10 ambition, 10 passions).
* **Vagues 6 à 9 :** Les organisateurs ont subitement changé la consigne et demandé d'attribuer une note de **1 à 10** à chaque critère !
* **Le risque :** Si l'on effectue une moyenne brute sans contrôle d'intégrité, un « 8 sur 10 » (très haute note) se retrouve mélangé avec un « 8 sur 100 » (note très faible) !

**La correction mathématique appliquée dans le code ([Tinder_speed_dating.md](file:///d:/PROJETS%20JEDHA/CERTIFICATION_CDSD/Bloc_2_Analyse_Exploratoire/Tinder/Tinder_speed_dating.md#L45-L53)) :**
```python
cols_stated = ['attr1_1', 'sinc1_1', 'intel1_1', 'fun1_1', 'amb1_1', 'shar1_1']
total = df_clean[cols_stated].sum(axis=1)
mask = total > 0
for col in cols_stated:
    df_clean.loc[mask, col] = df_clean.loc[mask, col] / total[mask] * 100
```
Pour chaque participant, on calcule la somme de ses 6 réponses, et on re-projette chaque critère sur une base 100 en pourcentage du total. Ainsi, les vagues 6 à 9 et les vagues 1 à 5 deviennent **strictement comparables sans aucun biais d'échelle**.

---

## 4. Rigueur Statistique & Inférence Mathématique

### A. Corrélation de Pearson ($r$)
* **Définition :** Le coefficient de corrélation linéaire de Pearson mesure la force et la direction de la relation entre deux variables quantitatives continues. Il oscille entre $-1$ (relation inverse parfaite), $0$ (absence de relation linéaire) et $+1$ (relation directe parfaite).
* **Formule :**
  $$r = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum (X_i - \bar{X})^2 \sum (Y_i - \bar{Y})^2}}$$
* **Résultat dans le projet :**
  * Décision réelle $\times$ Physique (`attr`) : **$r = 0,49$** (Corrélation forte, facteur dominant n°1).
  * Décision réelle $\times$ Humour (`fun`) : **$r = 0,41$** (Corrélation élevée n°2).
  * Décision réelle $\times$ Intelligence (`intel`) : **$r = 0,21$** (Faible corrélation, 2,5 fois moins que le physique !).
  * Décision réelle $\times$ Sincérité (`sinc`) : **$r = 0,21$**.

---

### B. Test t de Student de Welch
* **Définition :** Test d'hypothèse paramétrique comparant les moyennes de deux groupes indépendants (ici, Hommes vs Femmes). On utilise la variante de **Welch** car elle ne fait pas l'hypothèse que les deux groupes ont la même variance ($\sigma_1^2 \neq \sigma_2^2$).
* **Hypothèses :**
  * $H_0$ (Hypothèse nulle) : $\mu_{\text{Hommes}} = \mu_{\text{Femmes}}$ (Les deux genres accordent la même importance).
  * $H_1$ (Hypothèse alternative) : $\mu_{\text{Hommes}} \neq \mu_{\text{Femmes}}$.
* **Résultats scientifiques :**
  * **Physique :** $t = 8,87$, $p < 0,001$. Comme $p < 0,05$, on rejette $H_0$. L'écart (27,2% vs 18,0%) est **hautement significatif** : les hommes valorisent réellement beaucoup plus le physique.
  * **Ambition :** $t = -8,31$, $p < 0,001$. Rejet de $H_0$. Les femmes valorisent significativement plus l'ambition (12,8% vs 8,8%).
  * **Humour :** $t = 0,52$, $p = 0,60$. Comme $p > 0,05$, on **ne peut pas rejeter $H_0$**. Scientifiquement, hommes et femmes accordent exactement la même importance à l'humour (17,5% chacun).

> [!NOTE]
> **Qu'est-ce qu'une $p$-value ? (Explication simple pour le jury)**  
> La $p$-value est la probabilité d'obtenir une différence au moins aussi grande que celle observée, sous l'hypothèse que cette différence n'est due qu'au pur hasard de l'échantillonnage. Si $p < 5\%$, le risque d'erreur est minime : la différence est dite statistiquement significative.

---

### C. Test du Chi-deux d'indépendance ($\chi^2$)
* **Définition :** Test non-paramétrique permettant de tester l'existence d'un lien statistique entre deux variables qualitatives catégorielles présentées dans un tableau de contingence.
* **Croisement testé :** Même origine ethnique (`samerace` : Oui/Non) $\times$ Décision de match mutuel (`match` : Oui/Non).
* **Observation :**
  * Origine différente : **16,1 %** de match.
  * Même origine : **17,1 %** de match (+1,0 point d'écart).
* **Statistique de test :** $\chi^2 = 1,35$, $p = 0,245$.
* **Conclusion rigoureuse :** Comme $p = 0,245 > 0,05$, on conserve l'hypothèse nulle d'indépendance. Cet écart de 1 point s'explique totalement par la variance d'échantillonnage aléatoire. **Il n'y a pas d'effet communautaire statistiquement significatif sur le taux de match.**

---

### D. Étude d'ordre et fatigue décisionnelle
* **Définition :** Analyse de la variable `order` (le rang séquentiel du rendez-vous dans la soirée, de 1 à 22).
* **Observation dans les données :**
  * Rendez-vous 1 à 3 (début de soirée) : Taux de "Oui" = **43,8 %**.
  * Rendez-vous $\ge$ 15 (fin de soirée) : Taux de "Oui" = **40,0 %** (chute de **-3,8 points**).
* **Concept psychologique & Data :** **La fatigue décisionnelle (Ego Depletion)**. Plus un être humain prend des décisions successives à forte intensité émotionnelle sous contrainte de temps, plus ses ressources cognitives s'épuisent. Il devient plus sévère, plus blasé et a tendance à privilégier l'option par défaut la moins risquée : dire "Non".
* **Transposition à Tinder :** Le geste du swipe infini provoque exactement le même phénomène de désensibilisation et de saturation, ce qui détruit la valeur perçue des profils et le taux de match global.

---

## 5. Audit du Notebook : Les Calculs et Graphiques HD y sont-ils ?

Tous les chiffres présentés dans les slides et la soutenance sont **directement calculés et vérifiables dans le notebook `Tinder_speed_dating.ipynb` (et `Tinder_speed_dating.md`)** :

| Slide & Question | Donnée / Métrique clé | Cellule / Code dans le Notebook | Statut dans le Notebook |
| :---: | :--- | :--- | :---: |
| **Slide 2** | 551 participants, 8 378 dates, 42% oui, 16.5% match | Cellule 1 : `df.shape[0]`, `df['iid'].nunique()`, `df['dec'].mean()`, `df['match'].mean()` | ✅ Présent & Exécuté |
| **Slide 2** | Normalisation base 100 des vagues 6 à 9 | Cellule 1 : Boucle `mask = total > 0` et division par la somme | ✅ Présent & Exécuté |
| **Slide 3 (Q1)** | Importance déclarée H (27% phys) vs F (21% intel) | Cellule 2 : `moyennes = prefs.groupby('gender')[cols_stated].mean()` | ✅ Présent & Graphique HD |
| **Slide 4 (Q2)** | Déclaré vs Réel (Corrélation physique $r = 0,49$) | Cellule 3 : `corr_real = df[['dec'] + real_factors].corr()['dec']` | ✅ Présent & Double Barplot HD |
| **Slide 5 (Q3)** | Origine (+1 pt, 16.1% vs 17.1%) vs Passions (+4.8 pts) | Cellule 4 : `match_race` et `df_plot.groupby('bucket')['match'].mean()` | ✅ Présent & Double Barplot HD |
| **Slide 6 (Q4)** | Biais de lucidité (+1 pt Hommes, +0.8 pt Femmes) | Cellule 5 : `sns.scatterplot` + droite $y=x$ + `ecart.round(2)` | ✅ Présent & Nuage de points HD |
| **Slide 7 (Q5)** | Effet d'ordre (43.8% début vs 40.0% fin) | Cellule 6 : `df.groupby('order')` + calcul `debut - fin` | ✅ Présent & Courbe temporelle HD |
| **Statistiques** | Test t de Student ($t=8,87$) & Chi-deux ($\chi^2=1,35$) | Données calculées via `scipy.stats` (résultats intégrés dans la restitution) | ✅ Vérifié & Validé |

### Les Graphiques Seaborn sont-ils bien en Haute Définition (HD) ?
**OUI, absolument.** Le notebook commence dès la première cellule par :
```python
sns.set_theme(style='whitegrid', context='talk')
plt.rcParams['figure.dpi'] = 100
```
* `style='whitegrid'` : Fond blanc épuré avec quadrillage gris clair subtil.
* `context='talk'` : Police agrandie et lisible, idéale pour une projection ou un export PDF.
* `dpi = 100` : Haute densité de pixels éliminant tout flou de pixellisation sur les étiquettes et les barres.
* Couleurs adaptées et contrastées : Rose `#ff6b9d` pour les femmes, Bleu `#4a90e2` pour les hommes, Terracotta `#e07a5f` pour la décision réelle.

---

## 6. Questions Pièges & Réponses Tactiques du Candidat

### Q1. Pourquoi ne pas avoir fait d'algorithme de Machine Learning (Random Forest, XGBoost) sur ce bloc ?
> **Réponse du candidat :**  
> « Parce que le Bloc 2 est spécifiquement dédié à **l'Analyse Exploratoire et Inférentielle de Données (EDA)**. En entreprise, se précipiter sur un modèle prédictif complexe sans avoir exploré les biais, compris les corrélations et nettoyé les échelles conduit systématiquement à l'échec (*garbage in, garbage out*). Cette analyse pose les fondations indispensables : elle identifie les prédicteurs réels (le physique à $r=0,49$, l'humour, l'ordre) et élimine les variables sans signal (l'origine ethnique), préparant ainsi le terrain idéal pour la modélisation supervisée du Bloc 3. »

---

### Q2. Corrélation n'est pas causalité : si le physique a une corrélation de 0,49, est-on sûr que c'est lui qui cause la décision ?
> **Réponse du candidat :**  
> « Absolument, corrélation n'est pas causalité. Il existe un biais psychologique très documenté appelé **l'effet de halo** : lorsqu'une personne est jugée physiquement attirante, notre cerveau lui attribue inconsciemment d'autres qualités positives, en la percevant plus drôle, plus intelligente ou plus sympathique qu'elle ne l'est en réalité. Une partie de la corrélation de l'humour ($r = 0,41$) peut donc être un reflet indirect de l'attirance physique. C'est précisément pour cela que le physique reste le filtre dominant dans une rencontre éclair. »

---

### Q3. Si les participants se surestiment de 1 point sur 10, est-ce un vrai biais ou est-ce que les partenaires ont simplement été trop sévères ?
> **Réponse du candidat :**  
> « C'est un véritable **biais cognitif d'auto-complaisance (self-serving bias)**. Chaque participant n'a pas été noté par une seule personne aigrie, mais par **10 à 20 partenaires différents** lors de la soirée. En vertu de la loi des grands nombres, les notations sévères et généreuses se compensent pour converger vers la véritable attractivité perçue. Le fait que plus de 85 % des individus se notent au-dessus de la note reçue prouve mathématiquement un décalage structurel entre l'image de soi et la perception des autres. »

---

### Q4. Quelles sont les limites scientifiques de cette étude si Tinder voulait l'appliquer aujourd'hui ?
> **Réponse du candidat :**  
> « J'en identifie trois principales :
> 1. **Biais d'échantillonnage :** L'étude a été réalisée auprès d'étudiants de l'Université de Columbia à New York (Ivy League), un milieu jeune, urbain et hautement éduqué qui ne représente pas la diversité sociologique mondiale des utilisateurs de Tinder.
> 2. **Différence sensorielle du format :** Un rendez-vous de 4 minutes transmet la voix, la gestuelle, les micro-expressions et la prestance physique, alors que Tinder se résume à une photo en deux dimensions sur un écran de 6 pouces.
> 3. **Temporalité :** L'étude date de 2002-2004, avant l'avènement du smartphone et du swipe tactile instantané, même si les mécanismes fondamentaux de la sélection humaine restent universels. »

---

### Q5. En résumé, si vous deviez pitcher l'enseignement n°1 à la direction de Tinder en 15 secondes ?
> **Réponse du candidat :**  
> *« Ne demandez plus aux utilisateurs ce qu'ils cherchent, observez ce qu'ils font. Le déclaratif est un vœu pieux intellectuel ; la réalité du swipe est visuelle à 50 %. Aidez vos utilisateurs à sublimer leurs photos grâce à l'IA et protégez-les de la fatigue décisionnelle en limitant le défilement compulsif. »*
