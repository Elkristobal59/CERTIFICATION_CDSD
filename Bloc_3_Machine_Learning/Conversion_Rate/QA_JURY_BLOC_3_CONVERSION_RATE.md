# 🎓 Soutenance Bloc 3 : Conversion Rate Challenge — Questions & Réponses du Jury

> **Fiche Maître de Préparation Orale & Technique (CDSD — RNCP 35288)**  
> **Candidat :** Christopher GILLERON  
> **Projet Soutenu :** Prédiction du Taux de Conversion (*Data Science Weekly*)  
> **Format Oral :** 10 minutes (5 min Pitch + 5 min Q&A)  
> **Fichiers associés :** `Conversion_rate_prediction.ipynb` · `Conversion_rate_presentation.pptx` · `ORAL_SOUTENANCE_BLOC_3_CONVERSION_RATE_SLIDE_PAR_SLIDE.pdf`

---

## 🧭 Sommaire
1. [Fiche d'Identité & Tableau d'Or des Performances](#1-fiche-didentité--tableau-dor-des-performances)
2. [Prétraitement & Architecture du Pipeline Scikit-Learn](#2-prétraitement--architecture-du-pipeline-scikit-learn)
   - [A. Qu'est-ce que le split stratifié (`train_test_split(..., stratify=y)`) ?](#a-quest-ce-que-le-split-stratifié-train_test_split-stratifyy-)
   - [B. Pourquoi `StandardScaler` sur les pages vues et l'âge ?](#b-pourquoi-standardscaler-sur-les-pages-vues-et-lâge-)
   - [C. Pourquoi `OneHotEncoder(drop='first')` sur pays et source ? Le piège de la multicolinéarité](#c-pourquoi-onehotencoderdropfirst-sur-pays-et-source--le-piège-de-la-multicolinéarité)
   - [D. Pourquoi le Pipeline évite-t-il 100% des fuites de données (*Data Leakage*) ?](#d-pourquoi-le-pipeline-évite-t-il-100-des-fuites-de-données-data-leakage-)
3. [Compréhension des Données & Storytelling Exploratoire (EDA)](#3-compréhension-des-données--storytelling-exploratoire-eda)
   - [A. « Âge : Corrélation inverse · Les jeunes convertissent davantage » : Définition & Sens Métier](#a-âge--corrélation-inverse--les-jeunes-convertissent-davantage--définition--sens-métier)
   - [B. « Nature de `total_pages_visited` » : Variable contemporaine vs Fuite de données](#b-nature-de-total_pages_visited--variable-contemporaine-vs-fuite-de-données)
4. [La Baseline Minimale (1 seule variable) : Pourquoi commencer par là ?](#4-la-baseline-minimale-1-seule-variable--pourquoi-commencer-par-là-)
5. [Le Mystère des Coefficients : Log-Odds & Odds Ratios ($\exp(\beta)$)](#5-le-mystère-des-coefficients--log-odds--odds-ratios-expbeta-)
   - [A. Définition mathématique du Log-Odds (Logit)](#a-définition-mathématique-du-log-odds-logit)
   - [B. Définition et passage aux Odds Ratios (OR)](#b-définition-et-passage-aux-odds-ratios-or)
   - [C. Décryptage pas-à-pas des 4 Odds Ratios de la présentation](#c-décryptage-pas-à-pas-des-4-odds-ratios-de-la-présentation)
6. [Décryptage du Tableau Comparatif des Modèles & Optimisation du Seuil](#6-décryptage-du-tableau-comparatif-des-modèles--optimisation-du-seuil)
   - [A. Lecture et progression ligne par ligne du tableau](#a-lecture-et-progression-ligne-par-ligne-du-tableau)
   - [B. Pourquoi avoir abaissé le seuil de 0,50 à 0,45 ?](#b-pourquoi-avoir-abaissé-le-seuil-de-050-à-045-)
7. [Modèles Complexes (Random Forest & XGBoost) vs Régression Logistique](#7-modèles-complexes-random-forest--xgboost-vs-régression-logistique)
   - [A. Pourquoi RF et XGBoost sont-ils des « boîtes noires » non explicables ?](#a-pourquoi-rf-et-xgboost-sont-ils-des--boîtes-noires--non-explicables-)
   - [B. L'Arbitrage d'Ingénieur : Pourquoi retenir la Régression Logistique ?](#b-larbitrage-dingénieur--pourquoi-retenir-la-régression-logistique-)
8. [Comprendre les Métriques Critiques](#8-comprendre-les-métriques-critiques)
   - [A. Qu'est-ce que la ROC-AUC ici et pourquoi vaut-elle 0,9869 ?](#a-quest-ce-que-la-roc-auc-ici-et-pourquoi-vaut-elle-09869-)
   - [B. Pourquoi la moyenne harmonique pour le F1-Score et non arithmétique ?](#b-pourquoi-la-moyenne-harmonique-pour-le-f1-score-et-non-arithmétique-)
9. [Qu'est-ce que SMOTE et pourquoi ne pas l'avoir retenu ?](#9-quest-ce-que-smote-et-pourquoi-ne-pas-lavoir-retenu-)
10. [Questions Pièges du Jury & Réponses Tactiques du Candidat](#10-questions-pièges-du-jury--réponses-tactiques-du-candidat)

---

## 1. Fiche d'Identité & Tableau d'Or des Performances

### Les Chiffres d'Or du Projet (À connaître sur le bout des doigts)
* **Dataset d'entraînement :** **284 580 sessions de navigation** (5 features : `country`, `age`, `new_user`, `source`, `total_pages_visited`).
* **Volume d'évaluation (Split 80/20 stratifié) :** 227 664 sessions train / 56 916 sessions validation.
* **Taux de conversion global :** **3,23 %** (9 180 convertis pour 275 400 non-convertis).
* **Déséquilibre de classe :** Ratio **1 converti pour 30 non-convertis** (classe très minoritaire).
* **Accuracy d'un modèle paresseux (Baseline Dummy) :** **96,77 %** (si on prédit toujours 0). C'est pourquoi l'Accuracy est bannie comme critère de décision.
* **Métrique officielle de compétition / métier :** **F1-Score sur la classe positive (1)**.

### Le Tableau Officiel de Comparaison des Modèles

| Modèle | Seuil | F1-Score | Rappel (Recall) | Précision | ROC-AUC | Statut |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baseline LogReg (1 var)** | 0,50 | 0,7055 | 61,06 % | 83,50 % | 0,9764 | Modèle naïf de référence (`total_pages_visited` seule) |
| **LogReg Complète** | 0,50 | 0,7675 | 68,95 % | 86,54 % | 0,9869 | Toutes features intégrées, seuil standard |
| **LogReg Optimisée 🏆** | **0,45** | **0,7762** | **71,79 %** | **84,49 %** | **0,9869** | **Modèle Champion Retenu** (compromis optimal) |
| **Random Forest (Tuned)** | 0,43 | 0,7611 | 75,49 % | 76,72 % | 0,9844 | Surajustement local, dégrade la précision |
| **XGBoost Classifier** | 0,43 | 0,7763 | 73,80 % | 81,90 % | 0,9858 | Égalité de score (+0,0001), mais boîte noire |

---

## 2. Prétraitement & Architecture du Pipeline Scikit-Learn

```
                         ┌────────────────────────────────────────┐
                         │   JEU BRUT TRAIN (284 580 sessions)    │
                         └────────────────────────────────────────┘
                                              │
                      train_test_split(..., stratify=y, test_size=0.20)
                                              │
                ┌─────────────────────────────┴─────────────────────────────┐
                ▼                                                           ▼
    ┌────────────────────────┐                                  ┌────────────────────────┐
    │  X_train (227 664 lig) │                                  │   X_val (56 916 lig)   │
    │  3,23 % de convertis   │                                  │  3,23 % de convertis   │
    └────────────────────────┘                                  └────────────────────────┘
                │                                                           │
        .fit_transform()                                                .transform()
                │                                                           │
    ┌───────────────────────────────────────────────────────────────────────┴────────────┐
    │ COLUMN TRANSFORMER ÉTANCHE (Zéro fuite de données)                                 │
    │  • Numériques (age, total_pages_visited)  ──► StandardScaler()                     │
    │  • Catégorielles (country, source)        ──► OneHotEncoder(drop='first')          │
    │  • Binaire (new_user)                     ──► Reste 0 / 1                          │
    └────────────────────────────────────────────────────────────────────────────────────┘
```

### A. Qu'est-ce que le split stratifié (`train_test_split(..., stratify=y)`) ?
* **Principe :** La stratification consiste à forcer l'algorithme de découpage aléatoire à respecter **rigoureusement les mêmes proportions de classes** dans l'échantillon d'entraînement (`X_train`) et dans l'échantillon de test/validation (`X_val`).
* **Pourquoi est-ce obligatoire ici ?**
  Comme la classe positive ne représente que **3,23 %**, un tirage aléatoire simple sans stratification risquerait d'introduire un biais d'échantillonnage : par exemple 2,8 % de convertis dans le train et 4,0 % dans le test.
  Grâce à `stratify=y`, nous garantissons que `y_train` et `y_val` contiennent **exactement 3,23 % d'abonnés**. L'évaluation des performances est ainsi exempte de distorsion d'échantillonnage.

---

### B. Pourquoi `StandardScaler` sur les pages vues et l'âge ?
* **La formule mathématique :**
  $$z = \frac{x - \mu}{\sigma}$$
  Chaque valeur est centrée en soustrayant la moyenne $\mu$, puis réduite en divisant par l'écart-type $\sigma$. La variable résultante a une moyenne de 0 et une variance de 1.
* **Pourquoi la Régression Logistique l'exige absolument :**
  1. **Convergence mathématique :** La régression logistique utilise un solveur d'optimisation (algorithme quasi-Newton `lbfgs`). Si une variable oscille entre 1 et 30 (`total_pages_visited`) et une autre entre 17 et 123 (`age`), la surface de coût forme une ellipse très étirée. La descente de gradient zigzague et met beaucoup plus de temps à converger.
  2. **Régularisation équitable ($L_2$ Ridge) :** Scikit-learn applique par défaut une pénalité sur la somme des carrés des coefficients ($\lambda \sum \beta_j^2$). Si les variables n'ont pas la même échelle, l'algorithme va pénaliser arbitrairement la variable avec la plus grande amplitude brute sans rapport avec son importance réelle.
  3. **Comparabilité des coefficients :** Une fois standardisées, les variables continues sont sur un pied d'égalité : un coefficient de $+2,53$ pour les pages vues signifie directement « l'effet d'une augmentation de 1 écart-type (+3,3 pages) ».

---

### C. Pourquoi `OneHotEncoder(drop='first')` sur pays et source ? Le piège de la multicolinéarité
* **Le piège de la fausse variable (*Dummy Variable Trap*) :**
  Prenons la variable `country` qui comporte 4 modalités : `China`, `Germany`, `UK`, `US`.
  Si on crée 4 colonnes indicatrices $D_{\text{China}}, D_{\text{Germany}}, D_{\text{UK}}, D_{\text{US}}$, pour chaque ligne, la somme de ces 4 variables vaut obligatoirement 1 :
  $$D_{\text{China}} + D_{\text{Germany}} + D_{\text{UK}} + D_{\text{US}} = 1$$
  Or, le modèle de régression linéaire/logistique inclut déjà un terme constant : l'**intercept** ($\beta_0 \times 1$).
  Il existe donc une combinaison linéaire parfaite entre les 4 colonnes et l'intercept. La matrice de covariance $X^T X$ devient non inversible (déterminant nul), créant une **multicolinéarité parfaite**.
* **La solution `drop='first'` :**
  En supprimant la première modalité par ordre alphabétique (`China`), nous ne gardons que 3 colonnes : `Germany`, `UK`, `US`.
  * Si un visiteur est chinois, les 3 colonnes valent $(0, 0, 0)$. Son effet est capté par l'**intercept de base** $\beta_0$.
  * **La Chine devient la modalité de référence.** Les coefficients de l'Allemagne, du Royaume-Uni et des États-Unis mesurent ainsi directement le **surcroît de chance de conversion par rapport à un internaute chinois**.

---

### D. Pourquoi le Pipeline évite-t-il 100% des fuites de données (*Data Leakage*) ?
* **Qu'est-ce qu'une fuite de données ?**  
  C'est le fait d'utiliser involontairement des informations de l'ensemble de test lors de la préparation ou de l'entraînement du modèle, ce qui produit des scores artificiellement gonflés en laboratoire qui s'effondrent en production.
* **L'erreur classique des débutants :**  
  Faire `StandardScaler().fit_transform(X)` sur les 284 580 lignes avant de séparer en train et test. Dans ce cas, la moyenne $\mu$ et l'écart-type $\sigma$ calculés contiennent déjà l'information du jeu de test !
* **La garantie Scikit-Learn :**  
  En encapsulant le préprocesseur :
  ```python
  # 1. On APPREND les paramètres (moyenne, écart-type, catégories) UNIQUEMENT sur le train :
  X_train_proc = preprocessor.fit_transform(X_train)

  # 2. On TRANSFORME le test en réutilisant STRICTEMENT les moyennes du train (SANS refit) :
  X_val_proc = preprocessor.transform(X_val)
  ```
  Le jeu de validation reste hermétique et totalement inconnu du modèle jusqu'au moment de la prédiction finale.

---

## 3. Compréhension des Données & Storytelling Exploratoire (EDA)

### A. « Âge : Corrélation inverse · Les jeunes convertissent davantage » : Définition & Sens Métier

#### 1. Que signifie « Corrélation inverse » ?
* En statistique, **corrélation inverse** est le synonyme exact de **corrélation négative** ($r < 0$).
* Cela signifie que les deux grandeurs évoluent en sens opposés :  
  **Plus l'âge d'un visiteur AUGMENTE, plus sa probabilité de conversion DIMINUE** (ou formulé à l'endroit : plus un visiteur est jeune, plus il a de chances de s'abonner).
* Dans le modèle logistique, le coefficient de l'âge est négatif : $\beta_{\text{age}} = -0,61$, ce qui donne un Odds Ratio de $e^{-0,61} = 0,54$ (à chaque écart-type d'âge supplémentaire, la cote de conversion est quasiment divisée par 2).

#### 2. Les chiffres réels observés dans le dataset :
* **Moyenne d'âge des convertis :** **~25,5 ans**.
* **Moyenne d'âge des non-convertis :** **~30,7 ans**.
* Les tranches d'âge 18-25 ans affichent un taux de conversion proche de 5 %, alors que chez les plus de 45 ans, le taux tombe en dessous de 1 %.

#### 3. L'explication business pour le jury :
> *« Data Science Weekly est une newsletter technique spécialisée dans les tutoriels Python, les benchmarks de frameworks IA et les opportunités d'emploi dans la data. Ce contenu séduit en priorité les étudiants en fin de cursus, les profils en reconversion et les développeurs juniors qui cherchent activement à monter en compétences. Les profils plus seniors consultent parfois un article ponctuel mais ressentent moins le besoin vital de s'abonner à une veille hebdomadaire généraliste. »*

---

### B. « Nature de `total_pages_visited` » : Variable contemporaine vs Fuite de données

Le texte du prompteur précise :  
*« Attention : ce n'est pas une fuite de données, mais une variable contemporaine de la visite. Elle est parfaite pour scorer en direct, mais exige de travailler l'UX multi-pages. »*

#### 1. Pourquoi ce n'est PAS une fuite de données (*Data Leakage*) ?
* Une fuite de données survient quand une variable contient directement le résultat futur (par exemple une colonne `has_clicked_confirmation_email_link`).
* `total_pages_visited` est une véritable variable de mesure comportementale de l'internaute : elle compte simplement le nombre d'URL distinctes appelées pendant la session HTTP. Elle est parfaitement légitime.

#### 2. Pourquoi parle-t-on de « variable contemporaine de la visite » ?
* **Le piège de la cinématique temporelle :**  
  À l'instant $t = 0$ (la première seconde où l'internaute arrive sur la page d'accueil), son `total_pages_visited` vaut **1** !  
  La valeur finale de 14 pages n'est connue qu'au moment précis où la session se termine.
* On ne peut donc pas utiliser un modèle basé sur 14 pages pour décider dès la page d'accueil s'il faut lui afficher une offre agressive.
* **Comment l'utiliser intelligemment en production ?**  
  En faisant du **scoring dynamique au fil de l'eau** :
  * À la page 1 : probabilité faible.
  * À la page 4 : le score monte à 15 %.
  * **À la page 9 :** le score dépasse le seuil critique de 0,45. C'est à ce clic précis que le site déclenche un pop-in contextuel : *« Vous aimez nos articles ? Abonnez-vous pour recevoir notre synthèse chaque vendredi. »*

#### 3. L'implication UX (Produit) :
* On ne peut pas « forcer » un visiteur à lire 14 pages.
* En revanche, l'équipe produit doit structurer le site pour **faciliter la navigation multi-pages** : ajouter des blocs d'articles recommandés en fin de page, des résumés en 3 points, des sommaires cliquables et une vitesse de chargement instantanée pour faire franchir aux visiteurs la barre des 8 pages.

---

## 4. La Baseline Minimale (1 seule variable) : Pourquoi commencer par là ?

Dans la démarche scientifique, avant de tester des algorithmes sophistiqués (Random Forest, XGBoost), un Data Scientist d'élite établit toujours une **Baseline Naïve**.

### 1. En quoi consiste cette Baseline ?
* Une simple Régression Logistique entraînée sur **une seule variable** : `total_pages_visited`.
* Sans pays, sans âge, sans source, sans statut de visiteur.

### 2. Quels sont ses résultats ?
* **F1-Score :** **0,7055**
* **Rappel :** **61,06 %**
* **Précision :** **83,50 %**
* **ROC-AUC :** **0,9764**

### 3. Pourquoi le jury apprécie énormément cette étape ?
1. **Démonstration de bon sens :** Elle prouve que plus de 90 % du signal prédictif provient du simple niveau d'engagement de lecture du visiteur.
2. **Justification de la complexité :** Elle fixe un jalon chiffré incontestable ($F_1 = 0,7055$). Tout modèle plus complexe intégrant les autres variables doit obligatoirement battre ce score pour justifier les coûts d'infrastructure et de calcul supplémentaires. (Notre modèle complet monte à $0,7762$, validant ainsi l'apport des 4 autres variables).

---

## 5. Le Mystère des Coefficients : Log-Odds & Odds Ratios ($\exp(\beta)$)

### A. Définition mathématique du Log-Odds (Logit)
La Régression Logistique ne modélise pas directement une droite $y = ax + b$ (qui pourrait donner des valeurs négatives ou supérieures à 1), mais la **probabilité** $p = P(Y=1|X)$ via la fonction sigmoïde :
$$p = \frac{1}{1 + e^{-z}} \quad \text{avec} \quad z = \beta_0 + \beta_1 X_1 + \dots + \beta_k X_k$$

Si on isole la combinaison linéaire $z$, on obtient la relation fondamentale :
$$\ln\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_k X_k$$

* Le ratio $\frac{p}{1-p}$ s'appelle la **cote** (*odds* en anglais). C'est le rapport entre la probabilité de succès et la probabilité d'échec.  
  *(Exemple : si un cheval a $p = 0,80$ de chances de gagner, sa cote est de $\frac{0,80}{0,20} = 4$ contre 1).*
* Le terme $\ln\left(\frac{p}{1-p}\right)$ s'appelle le **Log-Odds** (ou fonction *logit*).
* **Le problème pour le jury et le business :** Dire à un directeur marketing que *« le coefficient de l'Allemagne est de +3,57 log-odds »*, c'est incompréhensible.

---

### B. Définition et passage aux Odds Ratios (OR)
Pour traduire ces coefficients abstraits en langage métier, on applique l'exponentielle :
$$\text{Odds Ratio (OR)} = e^{\beta_j}$$

* **L'Odds Ratio représente le facteur multiplicateur de la cote de conversion lorsque la variable $X_j$ augmente d'une unité (ou est activée dans le cas binaire).**
* Si $\beta > 0 \implies \text{OR} > 1$ : la variable **augmente** la cote de conversion.
* Si $\beta < 0 \implies \text{OR} < 1$ : la variable **diminue** la cote de conversion.
* Si $\beta = 0 \implies \text{OR} = 1$ : la variable n'a aucun effet.

---

### C. Décryptage pas-à-pas des 4 Odds Ratios de la présentation

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           DÉCRYPTAGE DES COEFFICIENTS ET ODDS RATIOS                          │
├──────────────────────────────┬───────────────┬─────────────────┬──────────────────────────────┤
│ Variable / Modalité          │ Coef (β)      │ Odds Ratio e^(β)│ Interprétation Métier        │
├──────────────────────────────┼───────────────┼─────────────────┼──────────────────────────────┤
│ Allemagne (Réf: Chine)       │ +3,567        │ 35,4            │ Cote x35,4 par rapport Chine │
│ Royaume-Uni (Réf: Chine)     │ +3,398        │ 29,9            │ Cote x29,9 par rapport Chine │
│ États-Unis (Réf: Chine)      │ +3,059        │ 21,3            │ Cote x21,3 par rapport Chine │
│ Pages Vues (+1 écart-type)   │ +2,525        │ 12,5            │ Cote x12,5 pour +3,3 pages   │
│ Nouveau Visiteur (new_user=1)│ -0,777        │ 0,46            │ Cote divisée par plus de 2   │
│ Âge (+1 écart-type)          │ -0,612        │ 0,54            │ Cote divisée par 1,85        │
└──────────────────────────────┴───────────────┴─────────────────┴──────────────────────────────┘
```

1. **Pays (Référence Chine) : Allemagne $\text{OR} = 35,4$ | UK $\text{OR} = 29,9$ | US $\text{OR} = 21,3$**
   * *Explication :* À caractéristiques de navigation rigoureusement identiques (même âge, même nombre de pages vues, même statut), un visiteur situé en Allemagne a une cote d'inscription **35,4 fois supérieure** à celle d'un internaute chinois.
   * *Conclusion décisionnelle :* La Chine présente un blocage critique (technique, linguistique ou Grand Firewall). Débloquer la Chine est le plus gros levier de croissance dormeur.
2. **Pages Vues : $\text{OR} = 12,5$**
   * *Explication :* Comme la variable a été centrée-réduite par `StandardScaler`, 1 unité correspond à 1 écart-type (soit environ **+3,3 pages supplémentaires**).  
     Chaque tranche de 3,3 pages lues multiplie la cote de conversion par **12,5**. C'est le moteur numéro 1 de la signature.
3. **Nouveau Visiteur (`new_user` = 1) : $\text{OR} = 0,46$**
   * *Explication :* $e^{-0,78} \approx 0,46$. Le fait d'être un nouveau visiteur plutôt qu'un habitué réduit la cote de plus de moitié ($1 / 0,46 \approx 2,17$). Un internaute récurrent convertit 5 fois plus en brut.
4. **Arbitrage LogReg vs XGBoost :**
   * XGBoost atteint un F1 équivalent ($0,7763$), mais n'offre aucun coefficient direct de ce type. La Régression Logistique est retenue pour cette transparence totale.

---

## 6. Décryptage du Tableau Comparatif des Modèles & Optimisation du Seuil

### A. Lecture et progression ligne par ligne du tableau
Le tableau retrace la démarche d'expérimentation méthodique menée tout au long du projet :

1. **Ligne 1 : Baseline LogReg 1 variable ($F_1 = 0,7055$ | Rappel $61,06\%$ | ROC-AUC $0,9764$)**  
   Preuve d'un signal fort sur les pages vues seules, mais le rappel est faible : on rate 39 % des futurs inscrits.
2. **Ligne 2 : LogReg Complète seuil par défaut 0,50 ($F_1 = 0,7675$ | Rappel $68,95\%$ | ROC-AUC $0,9869$)**  
   L'ajout des variables pays, âge, fidélité et source apporte **+6,2 points de F1-Score**. Le modèle s'enrichit significativement.
3. **Ligne 3 : LogReg Optimisée seuil 0,45 ($F_1 = 0,7762$ | Rappel $71,79\%$ | ROC-AUC $0,9869$) 🏆**  
   En ajustant simplement le seuil sans toucher au modèle, le rappel bondit à près de 72 %. C'est notre point d'équilibre maximal.
4. **Ligne 4 : Random Forest Tuned ($F_1 = 0,7611$ | Rappel $75,49\%$ | ROC-AUC $0,9844$)**  
   La Forêt Aléatoire obtient un bon rappel (75,5 %), mais au prix d'un effondrement de la précision (76,7 % contre 84,5 % pour la logistique). Elle crée beaucoup trop de faux positifs (fausses alertes d'inscription).
5. **Ligne 5 : XGBoost Classifier ($F_1 = 0,7763$ | Rappel $73,80\%$ | ROC-AUC $0,9858$)**  
   XGBoost fait $0,7763$ contre $0,7762$ pour la LogReg. L'écart est de **0,0001** (un dix-millième de point), ce qui est statistiquement indiscernable.

---

### B. Pourquoi avoir abaissé le seuil de 0,50 à 0,45 ?

```
     Précision (Faux positifs)                          Rappel (Détection des abonnés)
                │                                                     ▲
                │        ──► Compromis Optimal à SEUIL = 0,45 ◄──     │
                ▼                                                     │
 ──────────────────────────────────────────────────────────────────────────────────►
 Seuil : 0,10        0,20        0,30        0,40   [0,45]   0,50        0,60
                     Agressif (Beaucoup d'alertes)            Frileux (Beaucoup de ratés)
```

1. **La cause : Le déséquilibre naturel de la cible (3,23 %)**  
   Par défaut, scikit-learn prédit la classe positive dès que $P(\text{convert}) \ge 0,50$.  
   Mais dans un univers où 96,8 % des gens ne convertissent pas, une probabilité prédite de 46 % ou 48 % représente déjà une **intention d'achat colossale** (15 fois la moyenne normale !). Exiger 50 % est trop frileux et fait rater des centaines de conversions.
2. **Le mécanisme mathématique du balayage de seuil :**  
   En abaissant le seuil de 0,50 à 0,45 :
   * Le **Rappel** augmente de **+2,84 points** (de 68,95 % à 71,79 %). Sur notre jeu de validation de 56 916 sessions, nous capturons **1 318 abonnés réels** au lieu de 1 266.
   * La **Précision** ne baisse que très marginalement (de 86,5 % à 84,5 %, avec seulement 242 faux positifs).
   * Le **F1-Score**, qui est le compromis officiel, atteint son apogée à **0,7762**.
3. **La stabilité du plateau :**  
   La courbe de F1-Score entre 0,40 et 0,50 forme un plateau très stable. Cela garantit que le réglage à 0,45 n'est pas un artefact de surapprentissage (*overfitting*) mais une frontière robuste.

---

## 7. Modèles Complexes (Random Forest & XGBoost) vs Régression Logistique

### A. Pourquoi RF et XGBoost sont-ils des « boîtes noires » non explicables ?

* **Régression Logistique = Modèle « Boîte Blanche » (*White Box*) :**  
  La règle de décision est une équation mathématique unique, explicite et fermée :
  $$\text{Score} = \beta_0 + 3,57 \times \text{Allemagne} + 2,53 \times \text{Pages} - 0,61 \times \text{Âge} \dots$$
  N'importe quel développeur ou analyste peut auditer et justifier chaque décision prise pour un utilisateur donné en quelques secondes.

* **Random Forest et XGBoost = Modèles Ensemblistes « Boîtes Noires » (*Black Box*) :**  
  * Un Random Forest ou un XGBoost combine **100 à 250 arbres de décision profonds**.
  * Chaque arbre effectue des découpages croisés sur des sous-ensembles de features et d'échantillons (ex: *« Si pages > 8,2 ET âge < 27 ET pays != Chine ET new_user == 0... »*).
  * La prédiction finale est la moyenne pondérée ou la somme des résidus de 150 arbres distincts.
  * **Conséquence :** On ne peut pas exprimer la règle sous forme d'Odds Ratios simples. Pour comprendre ce qu'ils font, il faut recourir à des méthodes d'approximation post-hoc lourdes (SHAP values, calcul de Shapley exponentiel en temps de calcul).

---

### B. L'Arbitrage d'Ingénieur : Pourquoi retenir la Régression Logistique ?

C'est la question reine posée en soutenance CDSD :  
*« Si XGBoost fait 0,7763 et LogReg fait 0,7762, pourquoi choisir le modèle le plus basique ? »*

**La réponse magistrale du candidat :**
> *« En ingénierie de la donnée, la règle fondamentale est le **principe de parcimonie (rasoir d'Ockham)** : à performance égale, la solution la plus simple est toujours la meilleure.*  
> 
> *1. **L'écart de score est insignifiant :** 0,0001 de F1-Score sur 56 000 lignes représente une variation de prédiction sur à peine 2 ou 3 individus. C'est du bruit statistique.*  
> *2. **Performance en production :** Une inférence de Régression Logistique consiste en une simple multiplication matricielle qui s'exécute en **0,05 milliseconde**, contre plusieurs millisecondes pour évaluer 100 arbres XGBoost.*  
> *3. **Taille et coût mémoire :** Le modèle sérialisé pèse **quelques kilo-octets**, contre des dizaines de méga-octets pour une forêt.*  
> *4. **Valeur ajoutée métier :** La Logistique fournit immédiatement les Odds Ratios qui ont permis de découvrir le blocage en Chine et l'impact quantifié du parcours multi-pages. XGBoost n'aurait apporté aucune réponse actionnable à la direction du journal. »*

---

## 8. Comprendre les Métriques Critiques

### A. Qu'est-ce que la ROC-AUC ici et pourquoi vaut-elle 0,9869 ?

#### 1. Définition de la courbe ROC et de l'AUC :
* **ROC (Receiver Operating Characteristic) :** C'est une courbe qui trace le **Taux de Vrais Positifs (Rappel, TPR)** en ordonnée en fonction du **Taux de Faux Positifs (FPR)** en abscisse, pour **tous les seuils de décision possibles de 0 à 1**.
* **AUC (Area Under the Curve) :** C'est l'aire sous cette courbe ROC, comprise entre :
  * $0,50$ : le hasard complet (modèle qui tire à pile ou face).
  * $1,00$ : le classifieur parfait (sépare 100 % des positifs des négatifs sans aucune fausse alerte).

#### 2. L'interprétation probabiliste intuitive (celle qui épate le jury) :
> *« L'AUC-ROC mesure la capacité intrinsèque du modèle à ordonner les sessions. Si je pioche au hasard une session d'un abonné réel et une session d'un non-abonné, l'AUC de 0,9869 signifie qu'il y a **98,7 % de chances que mon modèle attribue un score de probabilité plus élevé à l'abonné qu'au non-abonné** ! »*

#### 3. Pourquoi la ROC-AUC est-elle complémentaire du F1-Score ?
* **La ROC-AUC est indépendante du seuil :** Elle évalue la qualité globale du classement des probabilités.
* **Le F1-Score dépend strictement du seuil :** Il évalue la décision concrète à un seuil donné ($0,45$).
* Notre ROC-AUC exceptionnelle ($0,9869$) prouvait d'avance que les probabilités étaient remarquablement ordonnées, et qu'il suffisait de caler le bon seuil de décision pour obtenir un F1 optimal.

---

### B. Pourquoi la moyenne harmonique pour le F1-Score et non arithmétique ?

#### 1. Comparaison des formules :
* **Moyenne Arithmétique :**
  $$\text{Moyenne} = \frac{\text{Précision} + \text{Rappel}}{2}$$
* **Moyenne Harmonique (F1-Score) :**
  $$F_1 = 2 \times \frac{\text{Précision} \times \text{Rappel}}{\text{Précision} + \text{Rappel}} = \frac{2}{\frac{1}{\text{Précision}} + \frac{1}{\text{Rappel}}}$$

#### 2. Pourquoi la moyenne harmonique pénalise impitoyablement les erreurs ?
La moyenne harmonique a une propriété mathématique stricte : **elle est toujours dominée et tirée vers le bas par la plus petite des deux valeurs**. Dès qu'un des deux indicateurs s'effondre, le F1-Score plonge vers zéro.

#### 3. Démonstration chiffrée par l'absurde (L'exemple du modèle paresseux) :
Imaginons un modèle idiot qui prédit "1" (Abonné) pour **l'intégralité des 284 580 sessions** du site :
* **Rappel :** Il attrape 100 % des abonnés réels $\implies \text{Rappel} = 1,00$ (**100 %**).
* **Précision :** Comme il n'y a que 3,23 % d'abonnés dans la masse, 96,77 % de ses alertes sont fausses $\implies \text{Précision} = 0,0323$ (**3,23 %**).

Calculons les deux moyennes :
* **Moyenne arithmétique :**
  $$\frac{1,00 + 0,0323}{2} = \frac{1,0323}{2} = \mathbf{0,516} \quad (51,6 \%)$$
  *Un jury non averti pourrait croire que ce modèle est "moyen", alors qu'il est totalement inutile et inonderait le marketing d'erreurs !*
* **Moyenne harmonique (F1-Score) :**
  $$2 \times \frac{1,00 \times 0,0323}{1,00 + 0,0323} = \frac{0,0646}{1,0323} = \mathbf{0,0626} \quad (6,2 \%)$$
  *Le F1-Score sanctionne immédiatement le désastre de la précision et renvoie une note proche de zéro.*

---

## 9. Qu'est-ce que SMOTE et pourquoi ne pas l'avoir retenu ?

### A. Définition et principe de SMOTE
* **SMOTE** signifie *Synthetic Minority Over-sampling Technique*.
* C'est un algorithme de sur-échantillonnage de la classe minoritaire.
* **Fonctionnement :**
  1. Pour chaque point $A$ appartenant à la classe minoritaire (convertis), SMOTE cherche ses $k$ plus proches voisins ($k\text{-NN}$) appartenant à la même classe dans l'espace multidimensionnel.
  2. Il choisit un voisin $B$ au hasard.
  3. Il crée un **point synthétique artificiel** situé sur le segment de droite qui relie $A$ et $B$ :
     $$\text{Nouveau point} = A + \lambda \times (B - A) \quad \text{avec } \lambda \in [0, 1]$$
  4. Il répète l'opération jusqu'à obtenir un équilibre 50/50 entre convertis et non-convertis.

---

### B. Pourquoi l'avons-nous écarté au profit de l'optimisation du seuil ?
1. **Incompatibilité avec les variables catégorielles encodées :**  
   Dans notre jeu de données, la plupart des features sont discrètes ou catégorielles (`country_Germany`, `source_Ads`, `new_user`).  
   Interpoler un point artificiel à mi-chemin entre deux individus crée des profils hybrides absurdes (par exemple un individu qui serait à 0,34 allemand et 0,66 anglais, ou à 0,40 nouveau visiteur). Même avec des variantes comme SMOTE-NC, le réalisme des données est altéré.
2. **Destruction de la calibration des probabilités :**  
   En forçant artificiellement un dataset équilibré 50/50, le modèle apprend que la conversion a 1 chance sur 2 d'arriver ! En production, ses probabilités de sortie sont totalement faussées et surestimées.
3. **Supériorité de l'optimisation de seuil :**  
   Entraîner le modèle sur la distribution naturelle réelle (3,23 %) et déplacer le seuil de décision à $0,45$ permet d'obtenir un rappel exceptionnel (71,8 %) tout en conservant des **probabilités parfaitement calibrées et fiables**.

---

## 10. Questions Pièges du Jury & Réponses Tactiques du Candidat

### Q1 : « Votre modèle affiche 98,7 % d'accuracy. Pourquoi ne pas vous être arrêté là ? »
**Réponse tactique :**  
*« Parce que l'Accuracy sur des données déséquilibrées est une illusion d'optique dangereuse. Si je construis un modèle qui renvoie systématiquement zéro sans même regarder les données, il obtient 96,8 % d'accuracy tout en ratant 100 % des abonnés réels. La valeur métier d'un tel algorithme est nulle. C'est pourquoi notre unique boussole a été le F1-Score sur la classe positive, qui combine précision et rappel et ne laisse passer aucune complaisance. »*

---

### Q2 : « Dans vos coefficients, l'Allemagne est à +3,57 et les pages vues à +2,53. L'Allemagne a-t-elle plus d'impact que les pages lues ? »
**Réponse tactique :**  
*« Non, attention à ne pas comparer des grandeurs d'échelles différentes !  
Le coefficient de l'Allemagne (+3,57) est un effet fixe binaire One-Hot : on l'ajoute une seule fois si l'utilisateur réside en Allemagne plutôt qu'en Chine.  
En revanche, le coefficient des pages vues (+2,53) s'applique à une variable continue standardisée. Il correspond à l'impact d'une augmentation de un écart-type (+3,3 pages). Un visiteur qui lit 10 pages supplémentaires accumule plusieurs fois cet incrément, ce qui surpasse largement le bonus géographique. Les pages vues restent la variable la plus puissante du modèle. »*

---

### Q3 : « Vous avez ajusté votre seuil à 0,45 sur le jeu de validation. N'avez-vous pas overfitté le seuil ? »
**Réponse tactique :**  
*« Ce risque théorique est totalement écarté dans notre projet pour deux raisons :  
D'abord, la taille volumétrique de notre jeu de validation : il compte 56 916 sessions, ce qui garantit une puissance statistique massive sans risque de surajustement d'un micro-échantillon.  
Ensuite, la topologie de la courbe de F1-Score : elle forme un plateau remarquablement large et plat entre 0,40 et 0,50. Le score ne s'effondre pas à 0,44 ou 0,46, ce qui prouve la très grande stabilité de cette frontière de décision en production. »*

---

### Q4 : « Si le marketing dit : "Le coût d'un email est nul, trouvez-moi un maximum d'abonnés même s'il y a des erreurs", que faites-vous ? »
**Réponse tactique :**  
*« C'est la beauté d'avoir retenu une Régression Logistique avec des probabilités bien calibrées : je n'ai absolument pas besoin de réentraîner le modèle.  
Il me suffit de modifier le seuil de décision de l'API en le passant par exemple de 0,45 à 0,25. Le modèle deviendra beaucoup plus agressif, fera passer le rappel à plus de 85 % et capturera la quasi-totalité des abonnés potentiels. La flexibilité est totale et instantanée. »*

---

### Q5 : « Pourquoi deux personnes de 123 ans sont-elles restées dans votre analyse exploratoire ? »
**Réponse tactique :**  
*« Deux lignes sur 284 580 représentent moins de 0,0007 % des données : leur poids mathématique sur les gradients est rigoureusement nul.  
Mais en tant que futur Lead Data Scientist, mon rôle ne s'arrête pas au nettoyage silencieux : j'ai utilisé cette découverte pour remonter une anomalie à l'équipe technique de Data Science Weekly, afin qu'elle ajoute un contrôle d'intégrité sur les formulaires d'inscription frontend (ex: borner l'âge entre 13 et 100 ans). »*
