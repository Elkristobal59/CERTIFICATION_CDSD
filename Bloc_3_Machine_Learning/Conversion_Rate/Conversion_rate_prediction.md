---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: base
    language: python
    name: python3
---

<img src="data:image/png;base64,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" alt="DSW LOGO" />

<!-- #region colab_type="text" id="0eiKSLYG8XvO" -->
# Challenge : predict conversions 🏆🏆

This is the template that shows the different steps of the challenge. In this notebook, all the training/predictions steps are implemented for a very basic model (logistic regression with only one variable). Please use this template and feel free to change the preprocessing/training steps to get the model with the best f1-score ! May the force be with you 🧨🧨  

**For a detailed description of this project, please refer to *02-Conversion_rate_challenge.ipynb*.**
<!-- #endregion -->

# Import libraries

```python colab={} colab_type="code" id="AGhdl7Bt2xZd"
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, confusion_matrix

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
# setting Jedha color palette as default
pio.templates["jedha"] = go.layout.Template(
    layout_colorway=["#4B9AC7", "#4BE8E0", "#9DD4F3", "#97FBF6", "#2A7FAF", "#23B1AB", "#0E3449", "#015955"]
)
pio.templates.default = "jedha"
pio.renderers.default = "svg" # to be replaced by "iframe" if working on JULIE
from IPython.display import display
```

<!-- #region colab_type="text" id="LHgro65rxKF7" -->
# Read file with labels
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 34} colab_type="code" id="W1AU8AH8u0qd" outputId="00698a97-027b-493b-a2e4-33fdcc295abb"
data = pd.read_csv('conversion_data_train.csv')
print('Set with labels (our train+test) :', data.shape)
```

```python
data.head()
```

<!-- #region colab_type="text" id="0XwjKBc63B1n" -->
# Explore dataset
<!-- #endregion -->

```python colab={} colab_type="code" id="NM0feCss5sLZ"
# The dataset is quite big : you must create a sample of the dataset before making any visualizations !
data_sample = data.sample(10000)
```

<!-- #region colab_type="text" id="70MwsoCS3QD5" -->
# Make your model
<!-- #endregion -->

<!-- #region colab_type="text" id="dPh1qPTf3wZU" -->
## Choose variables to use in the model, and create train and test sets
**From the EDA, we know that the most useful feature is total_pages_visited. Let's create a baseline model by using at first only this feature : in the next cells, we'll make preprocessings and train a simple (univariate) logistic regression.**
<!-- #endregion -->

```python colab={} colab_type="code" id="sjEHMGoY3kMB"
features_list = ['total_pages_visited']
numeric_indices = [0]
categorical_indices = []
target_variable = 'converted'
```

```python colab={"base_uri": "https://localhost:8080/", "height": 50} colab_type="code" id="SV5E9KMs4xcq" outputId="9d1ed76e-e82e-45e7-f3e5-6d47962caa5a"
X = data.loc[:, features_list]
Y = data.loc[:, target_variable]

print('Explanatory variables : ', X.columns)
print()
```

```python colab={"base_uri": "https://localhost:8080/", "height": 67} colab_type="code" id="W8K5DQEvvQgl" outputId="d280ebc9-4d4b-4723-b9fe-32513f898abc"
# Divide dataset Train set & Test set 
print("Dividing into train and test sets...")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
print("...Done.")
print()
```

<!-- #region colab_type="text" id="7b_aU7ij7K3Q" -->
## Training pipeline
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 235} colab_type="code" id="_9bEZ5bn7I5Z" outputId="ad5c8f97-2d25-4827-f1ee-43c665a97fa0"
# Put here all the preprocessings
print("Encoding categorical features and standardizing numerical features...")

featureencoder = StandardScaler()
X_train = featureencoder.fit_transform(X_train)
print("...Done")
print(X_train[0:5,:])
```

```python colab={"base_uri": "https://localhost:8080/", "height": 104} colab_type="code" id="1qhidLbq7o-5" outputId="6bfb746c-1ff4-41c9-b0d6-a98fd09a444d"
# Train model
print("Train model...")
classifier = LogisticRegression() # 
classifier.fit(X_train, Y_train)
print("...Done.")
```

```python colab={"base_uri": "https://localhost:8080/", "height": 84} colab_type="code" id="Au2TK_vw7rD-" outputId="702789a8-4631-4c29-f297-e4b2901f3195"
# Predictions on training set
print("Predictions on training set...")
Y_train_pred = classifier.predict(X_train)
print("...Done.")
print(Y_train_pred)
print()
```

<!-- #region colab_type="text" id="7TY_v9uH_CE7" -->
## Test pipeline
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 134} colab_type="code" id="ngOSdG6-_Cvb" outputId="1e19e8ee-222f-413b-9bc0-e9f41dcca1c0"
# Use X_test, and the same preprocessings as in training pipeline, 
# but call "transform()" instead of "fit_transform" methods (see example below)

print("Encoding categorical features and standardizing numerical features...")

X_test = featureencoder.transform(X_test)
print("...Done")
print(X_test[0:5,:])
```

```python colab={"base_uri": "https://localhost:8080/", "height": 84} colab_type="code" id="QS1XrzzE_jQI" outputId="866a96d2-4180-4bd1-ce54-ba052e75d485"
# Predictions on test set
print("Predictions on test set...")
Y_test_pred = classifier.predict(X_test)
print("...Done.")
print(Y_test_pred)
print()
```

<!-- #region colab_type="text" id="zxJCTlz0_2it" -->
## Performance assessment
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 50} colab_type="code" id="6x7p1nyr_3UV" outputId="8e5b91ba-ca06-4486-d808-37a6aaaa8cf7"
# WARNING : Use the same score as the one that will be used by Kaggle !
# Here, the f1-score will be used to assess the performances on the leaderboard
print("f1-score on train set : ", f1_score(Y_train, Y_train_pred))
print("f1-score on test set : ", f1_score(Y_test, Y_test_pred))
```

```python colab={"base_uri": "https://localhost:8080/", "height": 151} colab_type="code" id="KhDTCeBy__JK" outputId="72c82d66-d765-437e-e9ef-4ccc80e7183f"
# You can also check more performance metrics to better understand what your model is doing
print("Confusion matrix on train set : ")
print(confusion_matrix(Y_train, Y_train_pred))
print()
print("Confusion matrix on test set : ")
print(confusion_matrix(Y_test, Y_test_pred))
print()
```

**Our baseline model reaches a f1-score of almost 70%. Now, feel free to refine your model and try to beat this score ! 🚀🚀**

<!-- #region colab_type="text" id="6tVVDRABv91O" -->
# Train best classifier on all data and use it to make predictions on X_without_labels
**Before making predictions on the file conversion_data_test.csv, let's train our model on ALL the data that was in conversion_data_train.csv. Sometimes, this allows to make tiny improvements in the score because we're using more examples to train the model.**
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 154} colab_type="code" id="M14RHUadzE2p" outputId="abcfcfec-9461-4579-adbd-f23270f984eb"
# Concatenate our train and test set to train your best classifier on all data with labels
X = np.append(X_train,X_test,axis=0)
Y = np.append(Y_train,Y_test)

classifier.fit(X,Y)
```

```python colab={"base_uri": "https://localhost:8080/", "height": 151} colab_type="code" id="Tr4CEaPzzbP-" outputId="f0d1c8ed-be4b-4974-d7b9-f23a49344d9d"
# Read data without labels
data_without_labels = pd.read_csv('conversion_data_test.csv')
print('Prediction set (without labels) :', data_without_labels.shape)

# Warning : check consistency of features_list (must be the same than the features 
# used by your best classifier)
features_list = ['total_pages_visited']
X_without_labels = data_without_labels.loc[:, features_list]

# Convert pandas DataFrames to arrays before using scikit-learn
print("Convert pandas DataFrames to arrays...")
X_without_labels = X_without_labels.values
print("...Done")

print(X_without_labels[0:5,:])
```

```python colab={"base_uri": "https://localhost:8080/", "height": 134} colab_type="code" id="LoUISfsT0HMR" outputId="e42dc389-5e77-4e13-ccbc-1fef4aa2c0ca"
# WARNING : PUT HERE THE SAME PREPROCESSING AS FOR YOUR TEST SET
# CHECK YOU ARE USING X_without_labels
print("Encoding categorical features and standardizing numerical features...")

X_without_labels = featureencoder.transform(X_without_labels)
print("...Done")
print(X_without_labels[0:5,:])
```

```python colab={} colab_type="code" id="7DuWSEHuwEQJ"
# Make predictions and dump to file
# WARNING : MAKE SURE THE FILE IS A CSV WITH ONE COLUMN NAMED 'converted' AND NO INDEX !
# WARNING : FILE NAME MUST HAVE FORMAT 'conversion_data_test_predictions_[name].csv'
# where [name] is the name of your team/model separated by a '-'
# For example : [name] = AURELIE-model1
data = {
    'converted': classifier.predict(X_without_labels)
}

Y_predictions = pd.DataFrame(columns=['converted'],data=data)
Y_predictions.to_csv('conversion_data_test_predictions_EXAMPLE.csv', index=False)

```

## Analyzing the coefficients and interpreting the result
**In this template, we just trained a model with only one feature (total_pages_visited), so there's no analysis to be done about the feature importance 🤔**

**Once you've included more features in your model, please take some time to analyze the model's parameters and try to find some lever for action to improve the newsletter's conversion rate 😎😎**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
# --- AJOUTER LES FONCTIONS DE MÉTRIQUES ---
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix 
import numpy as np

# --- 1. PRÉPARATION DES DONNÉES ET DIVISION EN TRAIN/TEST ---
dataset = pd.read_csv('conversion_data_train.csv')
features_list = ['country', 'age', 'new_user', 'source', 'total_pages_visited']
target_variable = 'converted'

X = dataset.loc[:, features_list]
Y = dataset.loc[:, target_variable]

# ### AJOUTER LE SPLIT pour créer un ensemble de test AVEC étiquettes connues
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, stratify=Y, random_state=0)
print(f"Tailles (Train/Test) après division: X_train: {X_train.shape}, X_test: {X_test.shape}")


# Redéfinition du ColumnTransformer
numerical_features = ['age', 'total_pages_visited']
categorical_features = ['country', 'new_user', 'source'] 

featureencoder = ColumnTransformer(
    transformers=[
        ('scaling', StandardScaler(), numerical_features),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
)
classifier_rf = RandomForestClassifier(random_state=0, n_jobs=-1, n_estimators=100) 

# Prétraitement sur l'ensemble d'ENTRAÎNEMENT (X_train)
print("Prétraitement de l'ensemble de données d'entraînement...")
X_train_processed = featureencoder.fit_transform(X_train) 
X_test_processed = featureencoder.transform(X_test) # Transformation du TEST
print("...Terminé.")

# --- 2. ENTRAÎNEMENT DU MODÈLE (sur l'ensemble d'entraînement) ---
print("Entraînement du Random Forest sur les données d'entraînement...")
classifier_rf.fit(X_train_processed, Y_train) 
print("...Modèle entraîné.")


# --- 3. ÉVALUATION DES RÉSULTATS SUR L'ENSEMBLE DE TEST (X_test) ---

# Prédiction sur l'ensemble de test
Y_predictions_test = classifier_rf.predict(X_test_processed)

# ### CALCULER ET AFFICHER LE F1-SCORE
f1_test = f1_score(Y_test, Y_predictions_test)

print("\n--- RÉSULTATS DE PERFORMANCE SUR L'ENSEMBLE DE TEST (Évaluation) ---")
print(f"**F1-Score : {f1_test:.4f}**")
print(f"Rappel : {recall_score(Y_test, Y_predictions_test):.4f}")
print(f"Précision : {precision_score(Y_test, Y_predictions_test):.4f}")
print("Matrice de Confusion :\n", confusion_matrix(Y_test, Y_predictions_test))

# --- 4. PRÉDICTIONS ET EXPORT (sur le fichier sans étiquettes 'conversion_data_test.csv') ---
# (Cette partie reste identique pour générer le fichier de soumission)
data_without_labels = pd.read_csv('conversion_data_test.csv')
X_without_labels = data_without_labels.loc[:, features_list]
X_without_labels_processed = featureencoder.transform(X_without_labels)
Y_predictions_rf = classifier_rf.predict(X_without_labels_processed)

predictions_df = pd.DataFrame(
    {'converted': Y_predictions_rf}
)

# WARNING: Remplacer [VOTRE-NOM] par un nom d'équipe unique !
#predictions_df.to_csv('conversion_data_test_predictions_evaluation.csv', index=False) 
#print("\nFichier de soumission créé pour 'conversion_data_test.csv'.")
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix
import numpy as np

# --- PARAMÈTRES OPTIMAUX (Tirés des étapes précédentes) ---
BEST_RF_PARAMS = {'max_depth': 12, 'min_samples_leaf': 7, 'n_estimators': 250}
BEST_THRESHOLD = 0.43 # Seuil optimal pour maximiser le F1-Score

# --- 1. PRÉPARATION DES DONNÉES ET DIVISION EN TRAIN/TEST ---
dataset = pd.read_csv('conversion_data_train.csv')
features_list = ['country', 'age', 'new_user', 'source', 'total_pages_visited']
target_variable = 'converted'

X = dataset.loc[:, features_list]
Y = dataset.loc[:, target_variable]

# Division des données pour l'évaluation
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=0)
print(f"Tailles (Train/Test) après division: X_train: {X_train.shape}, X_test: {X_test.shape}")

# --- 2. TARGET ENCODING POUR 'country' (Optimisation Clé) ---
print("\nApplication du Target Encoding sur 'country'...")
# Calcul de l'encodage sur le TRAIN
country_mean_encoding = Y_train.groupby(X_train['country']).mean()
global_mean_conversion = Y_train.mean()

X_train['country_encoded'] = X_train['country'].map(country_mean_encoding)
X_test['country_encoded'] = X_test['country'].map(country_mean_encoding)
X_test['country_encoded'].fillna(global_mean_conversion, inplace=True) 

# Préparation des DataFrames pour le ColumnTransformer
X_train_final = X_train.drop(columns=['country'])
X_test_final = X_test.drop(columns=['country'])

# --- 3. PRÉTRAITEMENT et ENTRAÎNEMENT DU MODÈLE OPTIMAL ---

# 'country_encoded' est maintenant numérique
numerical_features = ['age', 'total_pages_visited', 'country_encoded']
categorical_features = ['new_user', 'source'] 

featureencoder = ColumnTransformer(
    transformers=[
        ('scaling', StandardScaler(), numerical_features),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
)

# Prétraitement
X_train_processed = featureencoder.fit_transform(X_train_final) 
X_test_processed = featureencoder.transform(X_test_final) 
print("Prétraitement terminé.")

# Modèle avec les hyperparamètres optimaux (Grid Search)
classifier_rf = RandomForestClassifier(random_state=0, n_jobs=-1, **BEST_RF_PARAMS) 

print("Entraînement du Random Forest (Optimal) sur l'ensemble d'ENTRAÎNEMENT...")
classifier_rf.fit(X_train_processed, Y_train) 
print("...Modèle entraîné.")


# --- 4. ÉVALUATION AVEC LE SEUIL OPTIMAL (Pour un bon F1-Score) ---

# Prédiction des probabilités sur l'ensemble de test
Y_probabilities_test = classifier_rf.predict_proba(X_test_processed)[:, 1]

# Application du seuil optimal de 0.43
Y_predictions_test = (Y_probabilities_test >= BEST_THRESHOLD).astype(int)

print(f"\n--- RÉSULTATS DE PERFORMANCE OPTIMISÉS (Seuil {BEST_THRESHOLD}) ---")

# Calcul des métriques
f1 = f1_score(Y_test, Y_predictions_test)
recall = recall_score(Y_test, Y_predictions_test)
precision = precision_score(Y_test, Y_predictions_test)
conf_matrix = confusion_matrix(Y_test, Y_predictions_test)

print(f"**F1-Score FINAL sur Test : {f1:.4f}**")
print(f"Rappel (Recall) : {recall:.4f}")
print(f"Précision (Precision) : {precision:.4f}")

# Affichage de la matrice de confusion
print("\nMatrice de Confusion (Test Set) : ")
print(conf_matrix)
print("(Ces résultats devraient être très proches de 0.7651)")
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix
import numpy as np
from xgboost import XGBClassifier 


# --- PARAMÈTRES OPTIMAUX ---
BEST_THRESHOLD = 0.43 
RANDOM_STATE = 20
SUBMISSION_FILE_NAME = 'conversion_predictions_XGB_FINAL.csv'


# --- 1. PRÉPARATION DES DONNÉES ET TARGET ENCODING (Base de données) ---
dataset_train = pd.read_csv('conversion_data_train.csv')
features_list = ['country', 'age', 'new_user', 'source', 'total_pages_visited']
target_variable = 'converted'

X_full = dataset_train.loc[:, features_list]
Y_full = dataset_train.loc[:, target_variable]

# Division temporaire pour l'évaluation du F1-Score
X_train_eval, X_test_eval, Y_train_eval, Y_test_eval = train_test_split(
    X_full, Y_full, test_size=0.15, random_state=RANDOM_STATE
)

# Target Encoding
country_mean_encoding = Y_train_eval.groupby(X_train_eval['country']).mean()
global_mean_conversion = Y_train_eval.mean()

X_train_eval['country_encoded'] = X_train_eval['country'].map(country_mean_encoding)
X_test_eval['country_encoded'] = X_test_eval['country'].map(country_mean_encoding)
X_test_eval['country_encoded'].fillna(global_mean_conversion, inplace=True) 

X_train_final_eval = X_train_eval.drop(columns=['country'])
X_test_final_eval = X_test_eval.drop(columns=['country'])


# --- 2. PRÉTRAITEMENT et ENTRAÎNEMENT DU MODÈLE XGBOOST (ÉVALUATION) ---

numerical_features = ['age', 'total_pages_visited', 'country_encoded']
categorical_features = ['new_user', 'source'] 

featureencoder = ColumnTransformer(
    transformers=[
        ('scaling', StandardScaler(), numerical_features),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
)

X_train_processed = featureencoder.fit_transform(X_train_final_eval) 
X_test_processed = featureencoder.transform(X_test_final_eval) 

classifier_xgb = XGBClassifier(
    n_estimators=100, max_depth=7, learning_rate=0.1, use_label_encoder=False, 
    eval_metric='logloss', random_state=RANDOM_STATE, n_jobs=-1
) 

classifier_xgb.fit(X_train_processed, Y_train_eval) 

# --- 3. ÉVALUATION DES PERFORMANCES (Affichage du F1-Score) ---
Y_probabilities_test = classifier_xgb.predict_proba(X_test_processed)[:, 1]
Y_predictions_test = (Y_probabilities_test >= BEST_THRESHOLD).astype(int)
f1 = f1_score(Y_test_eval, Y_predictions_test)

print(f"\n--- RÉSULTATS DE PERFORMANCE OPTIMISÉS (XGBoost, Seuil {BEST_THRESHOLD}) ---")
print(f"**F1-Score MAXIMAL (Test) : {f1:.4f}**")
print(f"Rappel (Recall) : {recall_score(Y_test_eval, Y_predictions_test):.4f}")
print(f"Précision (Precision) : {precision_score(Y_test_eval, Y_predictions_test):.4f}")


# ====================================================================================
# --- 4. PRÉDICTION SUR LE FICHIER conversion_data_test.csv (PRODUCTION) ---
# ====================================================================================

print("\n--- PRÉPARATION POUR LA SOUMISSION : Modèle final sur 100% des données ---")

# 4a. RECALCULER Target Encoding et Preprocessing sur X_full (POUR MAXIMISER LE MODÈLE)
country_mean_encoding_full = Y_full.groupby(X_full['country']).mean()
global_mean_conversion_full = Y_full.mean()

X_full['country_encoded'] = X_full['country'].map(country_mean_encoding_full)
X_full_final = X_full.drop(columns=['country'])

# FIT Final du Preprocessor sur TOUT l'ensemble d'entraînement
X_full_processed = featureencoder.fit_transform(X_full_final) 

# 4b. ENTRAÎNEMENT DU MODÈLE FINAL
classifier_final = XGBClassifier(
    n_estimators=100, max_depth=7, learning_rate=0.1, use_label_encoder=False, 
    eval_metric='logloss', random_state=RANDOM_STATE, n_jobs=-1
)
classifier_final.fit(X_full_processed, Y_full)

# 4c. PRÉPARATION DU JEU DE TEST/SOUMISSION
data_test_submission = pd.read_csv('conversion_data_test.csv')
X_test_submission = data_test_submission.loc[:, features_list]

# Appliquer Target Encoding (basé sur le calcul complet)
X_test_submission['country_encoded'] = X_test_submission['country'].map(country_mean_encoding_full)
X_test_submission['country_encoded'].fillna(global_mean_conversion_full, inplace=True)
X_submission_final = X_test_submission.drop(columns=['country'])

# Transformation
X_submission_processed = featureencoder.transform(X_submission_final) 

# 4d. PRÉDICTION FINALE et EXPORTATION
Y_probabilities_submission = classifier_final.predict_proba(X_submission_processed)[:, 1]
Y_predictions_submission = (Y_probabilities_submission >= BEST_THRESHOLD).astype(int)

df_submission = pd.DataFrame({'converted': Y_predictions_submission})
submission_file_name_final = f'conversion_data_chrisgilleron__XGB_F1_{f1:.4f}.csv' # Nommage corrigé avec le F1 du test
df_submission.to_csv(submission_file_name_final, index=True, index_label='id')

print(f"\n✅ EXPORTATION RÉUSSIE : Fichier de soumission créé : {submission_file_name_final}")
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.linear_model import LogisticRegression



dataset = pd.read_csv('conversion_data_train.csv')
print('Set with labels (our train+test) :', dataset.shape)

features_list = ['country', 'age', 'new_user', 'source', 'total_pages_visited']
target_variable = 'converted'

X = dataset.loc[:, features_list]
Y = dataset.loc[:, target_variable]

# Division Train/Test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
numerical_features = ['age', 'total_pages_visited']
categorical_features = ['country', 'new_user', 'source']

# Création du ColumnTransformer
featureencoder = ColumnTransformer(
    transformers=[
        ('scaling', StandardScaler(), numerical_features),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
)

print("ColumnTransformer créé.")


# Entrainement du Pipeline

X_train_processed = featureencoder.fit_transform(X_train)
X_test_processed = featureencoder.transform(X_test)

# Entrainement du Modèle

classifier = LogisticRegression(max_iter=1000) # Augmenter max_iter pour éviter les avertissements de convergence
classifier.fit(X_train_processed, Y_train)

# Prédictions
Y_train_pred = classifier.predict(X_train_processed)
Y_test_pred = classifier.predict(X_test_processed)

from sklearn.metrics import f1_score, confusion_matrix

# 1. Faire les prédictions séparément (si ce n'est pas déjà fait)
Y_train_pred_rf = classifier.predict(X_train_processed)
Y_test_pred_rf = classifier.predict(X_test_processed)

# 2. Afficher les scores (la correction est ici)
print("f1-score on train set : ", f1_score(Y_train, Y_train_pred_rf)) # Y_train vs Y_train_pred_rf
print("f1-score on test set : ", f1_score(Y_test, Y_test_pred_rf))   # Y_test vs Y_test_pred_rf

# 3. Afficher la matrice de confusion
print("\nConfusion matrix on test set : ")
print(confusion_matrix(Y_test, Y_test_pred_rf))

```

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
# Importation de toutes les métriques
from sklearn.metrics import f1_score, confusion_matrix, recall_score, precision_score 
import numpy as np

# --- PRÉPARATION DES DONNÉES ET ENTRAÎNEMENT ---
dataset = pd.read_csv('conversion_data_train.csv')
features_list = ['country', 'age', 'new_user', 'source', 'total_pages_visited']
target_variable = 'converted'
X = dataset.loc[:, features_list]
Y = dataset.loc[:, target_variable]

# Division Train/Test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

numerical_features = ['age', 'total_pages_visited']
categorical_features = ['country', 'new_user', 'source']

# ColumnTransformer
featureencoder = ColumnTransformer(
    transformers=[
        ('scaling', StandardScaler(), numerical_features),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
)
X_train_processed = featureencoder.fit_transform(X_train)
X_test_processed = featureencoder.transform(X_test)

# Entrainement du Modèle (Régression Logistique)
classifier = LogisticRegression(max_iter=1000, random_state=0)
classifier.fit(X_train_processed, Y_train)

# --- ÉVALUATION DES PERFORMANCES ---
Y_test_pred = classifier.predict(X_test_processed)

# Calcul et affichage du F1-Score, du Rappel et de la Précision
f1 = f1_score(Y_test, Y_test_pred)
recall = recall_score(Y_test, Y_test_pred)
precision = precision_score(Y_test, Y_test_pred)

print("--- RÉSULTATS D'ÉVALUATION (Régression Logistique) ---")
print(f"F1-Score sur test set : {f1:.4f}")
print(f"Rappel (Recall) sur test set : {recall:.4f}")
print(f"Précision (Precision) sur test set : {precision:.4f}")

print("\nMatrice de Confusion sur test set : ")
print(confusion_matrix(Y_test, Y_test_pred))


# =========================================================================
# --- SECTION 4 : PRÉDICTION FINALE ET EXPORTATION (Production) ---
# =========================================================================

print("\n--- 4. PRÉPARATION POUR LA SOUMISSION FINALE ---")

# 1. Prétraitement de TOUTES les données d'entraînement (X_full)
X_full_processed = featureencoder.fit_transform(X) 

# 2. Entraînement du classifieur sur TOUTES les données étiquetées
classifier_final = LogisticRegression(max_iter=1000, random_state=0)
classifier_final.fit(X_full_processed, Y)

# 3. Chargement et Prétraitement du Fichier Test Sans Étiquettes
data_test_submission = pd.read_csv('conversion_data_test.csv') 
X_test_submission = data_test_submission.loc[:, features_list]

# 4. Transformation du fichier test.csv
X_submission_processed = featureencoder.transform(X_test_submission) 

# 5. Prédiction Finale et Exportation
Y_predictions_submission = classifier_final.predict(X_submission_processed)

df_submission = pd.DataFrame({'converted': Y_predictions_submission})
submission_file_name = 'conversion_predictions_logreg_final.csv'
df_submission.to_csv(submission_file_name, index=True, index_label='id')

print(f"✅ EXPORTATION RÉUSSIE : Fichier de soumission créé : {submission_file_name}")
```

```python

# Load in our libraries
import random
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
# import ensemble methods
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


data = pd.read_csv('conversion_data_train.csv')
print('Set with labels (our train+test) :', data.shape)

X = data.drop("converted", axis=1)
y = data["converted"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, random_state = 0)

# Mettez cela dans votre cellule de définition des features :

numerical_features = ['age', 'total_pages_visited'] 
# Si votre problème contient une colonne 'converted', assurez-vous qu'elle est retirée de X

categorical_features = ['country', 'source', 'new_user'] # 'new_user' est binaire (0/1)



print('Found numeric features:', numerical_features)
print('Found categorical features:', categorical_features)

numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer()), 
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(
    steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), # missing values will be replaced by most frequent value
    ('encoder', OneHotEncoder(drop='first')) # first column will be dropped to avoid creating correlations between features
    ])


preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Preprocessings on train set
print("Performing preprocessings on train set...")
print(X_train.head())
X_train = preprocessor.fit_transform(X_train)
print('...Done.')
print(X_train[0:5]) 
print()

# Preprocessings on test set
print("Performing preprocessings on test set...")
print(X_test.head()) 
X_test = preprocessor.transform(X_test) # Don't fit again !! 
print('...Done.')
print(X_test[0:5,:])

scores_df = pd.DataFrame(columns = ['model', 'accuracy', 'set'])

# RANDOM FOREST CLASSIFIER WITH GRID SEARCH
print("Grid search...")
random_forest = XGBClassifier(random_state=42, n_jobs=-1)

# Grid of values to be tested
params_xgb = {
    'max_depth': [3, 5, 7], # Profondeur maximale de l'arbre
    'learning_rate': [0.05, 0.1, 0.2], # Taux d'apprentissage
    'n_estimators': [50, 100, 200], # Nombre d'arbres
    'subsample': [0.7, 0.9] # Ratio de sous-échantillonnage
}
print(params_xgb)
gridsearch = GridSearchCV(random_forest, param_grid = params_xgb, cv = 2, verbose = 1,n_jobs=-1,scoring='roc_auc') 
gridsearch.fit(X_train, y_train)
print("...Done.")
print("Best hyperparameters : ", gridsearch.best_params_)
print("Best validation accuracy : ", gridsearch.best_score_)
print()
print("Accuracy on training set : ", gridsearch.score(X_train, y_train))
print("Accuracy on test set : ", gridsearch.score(X_test, y_test))


new_rows = [
    {'model': 'random_forest', 'accuracy': gridsearch.score(X_train, y_train), 'set': 'train'},
    {'model': 'random_forest', 'accuracy': gridsearch.score(X_test, y_test), 'set': 'test'}
]

scores_df = pd.concat([scores_df, pd.DataFrame(new_rows)], ignore_index=True)
scores_df



print("\n--- 4. PRÉPARATION POUR LA SOUMISSION FINALE ---")


X_full_processed = preprocessor.fit_transform(X) 
Y = y 

classifier_final = gridsearch.best_estimator_


classifier_final.fit(X_full_processed, Y)

print("✅ Modèle final entraîné sur toutes les données.")


data_test_submission = pd.read_csv('conversion_data_test.csv') 

X_test_submission = data_test_submission.copy() 


X_submission_processed = preprocessor.transform(X_test_submission) 


Y_predictions_submission = classifier_final.predict(X_submission_processed)

df_submission = pd.DataFrame({'converted': Y_predictions_submission})

submission_file_name = 'conversion_data_test_predictions_chrisgilleron_XGBClassifier.csv'
df_submission.to_csv(submission_file_name, index=False)




print(f"✅ EXPORTATION RÉUSSIE : Fichier de soumission créé : {submission_file_name}")
```

```python
data.shape
```

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Obtenir les prédictions sur l'ensemble de test
best_model = gridsearch.best_estimator_
y_pred = best_model.predict(X_test)

# 2. Calculer la matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print("Matrice de Confusion :")
print(cm)

# 3. Visualisation (Optionnel)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', 
            xticklabels=['Prédit Non-Converti (0)', 'Prédit Converti (1)'],
            yticklabels=['Réel Non-Converti (0)', 'Réel Converti (1)'])
plt.ylabel('Valeur Réelle')
plt.xlabel('Valeur Prédite')
plt.title('Matrice de Confusion sur l\'Ensemble de Test')
plt.show()
```

```python
scores_df
```

```python
# Perform grid search
print("Grid search...")
xgboost = XGBClassifier()

# Grid of values to be tested
params = {
    'max_depth': [4, 6, 8, 10],
    'min_child_weight': [1, 2, 4, 6, 8],
    'n_estimators': [2, 4, 6, 8, 10, 12]
}
print(params)
gridsearch = GridSearchCV(xgboost, param_grid = params, cv = 3, verbose = 1) # cv : the number of folds to be used for CV
gridsearch.fit(X_train, y_train)
print("...Done.")
print("Best hyperparameters : ", gridsearch.best_params_)
print("Best validation accuracy : ", gridsearch.best_score_)
print()
print("Accuracy on training set : ", gridsearch.score(X_train, y_train))
print("Accuracy on test set : ", gridsearch.score(X_test, y_test))

# scores_df = scores_df.append({'model': 'xgboost', 'accuracy': gridsearch.score(X_train, y_train), 'set': 'train'}, ignore_index = True)
# scores_df = scores_df.append({'model': 'xgboost', 'accuracy': gridsearch.score(X_test, y_test), 'set': 'test'}, ignore_index = True)
# scores_df

new_rows = [
    {'model': 'xgboost', 'accuracy': gridsearch.score(X_train, y_train), 'set': 'train'},
    {'model': 'xgboost', 'accuracy': gridsearch.score(X_test, y_test), 'set': 'test'}
]

scores_df = pd.concat([scores_df, pd.DataFrame(new_rows)], ignore_index=True)
scores_df

```
