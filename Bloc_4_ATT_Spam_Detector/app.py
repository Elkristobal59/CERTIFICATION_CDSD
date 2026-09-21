import os
import re
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(
    page_title="AT&T SMS Spam Detector",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_KERAS_PATH = os.path.join(BASE_DIR, "att_spam_model.keras")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer.pickle")
SPAM_CSV_PATH = os.path.join(BASE_DIR, "spam.csv")

# Mots-clés fréquemment associés aux spams / smishing pour surbrillance explicative
SUSPICIOUS_KEYWORDS = [
    "free", "win", "won", "winner", "prize", "cash", "claim", "urgent", "call", "call now",
    "txt", "text", "stop", "reply", "mobile", "awarded", "guaranteed", "selected",
    "customer", "service", "account", "verify", "suspended", "password", "bank", "alert",
    "link", "click", "http", "https", "www", "credit", "loan", "gift", "voucher", "1000", "500"
]

# Custom CSS — Palette AT&T (Bleu #00A8E0, Navy #0A2540)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0A2540 0%, #004D7A 50%, #00A8E0 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .main-header p {
        color: #E2E8F0;
        margin: 8px 0 0 0;
        font-size: 1.05rem;
    }
    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00A8E0;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #4A5568;
        margin-top: 4px;
    }
    .badge-ham {
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #31C48D;
        padding: 14px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .badge-spam {
        background-color: #FDE8E8;
        color: #9B1C1C;
        border: 1px solid #F98080;
        padding: 14px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .badge-quarantine {
        background-color: #FEF08A;
        color: #713F12;
        border: 1px solid #EAB308;
        padding: 14px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.25rem;
    }
    .highlight-spam-word {
        background-color: #FECACA;
        color: #991B1B;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_deep_learning_artifacts():
    """Charge le modèle Keras et le Tokenizer sérialisé."""
    if os.path.exists(MODEL_KERAS_PATH) and os.path.exists(TOKENIZER_PATH):
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_KERAS_PATH)
        with open(TOKENIZER_PATH, "rb") as f:
            tokenizer = pickle.load(f)
        return model, tokenizer, "deep_learning"
    else:
        # Fallback de sécurité au cas où le modèle Keras est en cours d'export
        from sklearn.pipeline import Pipeline
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        
        df = pd.read_csv(SPAM_CSV_PATH, encoding="latin-1").iloc[:, :2]
        df.columns = ["label", "message"]
        df["target"] = (df["label"] == "spam").astype(int)
        
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)),
            ("model", LogisticRegression(random_state=42, max_iter=1000))
        ])
        pipeline.fit(df["message"], df["target"])
        return pipeline, None, "fallback_logreg"


# Chargement des artefacts
try:
    model, tokenizer, model_type = load_deep_learning_artifacts()
except Exception as e:
    st.error(f"Erreur lors du chargement des artefacts : {e}")
    st.stop()


def predict_spam_proba(text, model, tokenizer, model_type):
    """Calcule la probabilité que le SMS soit un spam."""
    if model_type == "deep_learning":
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        seq = tokenizer.texts_to_sequences([text])
        pad = pad_sequences(seq, maxlen=100, padding="post", truncating="post")
        proba = float(model.predict(pad, verbose=0)[0][0])
    else:
        proba = float(model.predict_proba([text])[0, 1])
    return proba


def highlight_suspects(text):
    """Surligne les termes et motifs suspects dans le texte pour l'explicabilité."""
    words = text.split()
    highlighted = []
    found_keywords = []
    for w in words:
        clean_w = re.sub(r"[^\w\s]", "", w).lower()
        if clean_w in SUSPICIOUS_KEYWORDS or any(kw in clean_w for kw in ["http", "www", "claim", "prize"]):
            highlighted.append(f"<span class='highlight-spam-word'>{w}</span>")
            found_keywords.append(w)
        else:
            highlighted.append(w)
    return " ".join(highlighted), list(set(found_keywords))


# ==============================================================================
# SIDEBAR : CONTABILITÉ MÉTIER & RÉGLAGE DU SEUIL
# ==============================================================================
with st.sidebar:
    st.image("https://full-stack-assets.s3.eu-west-3.amazonaws.com/M08-deep-learning/AT%26T_logo_2016.svg", width=160)
    st.markdown("### ⚙️ Pilotage Télécom")
    
    st.markdown("""
    **Politique de risque AT&T :**
    Le coût d'un **Faux Positif** (bloquer un SMS légitime) est infiniment supérieur à celui d'un **Faux Négatif** (laisser passer un spam).
    """)
    
    threshold = st.slider(
        "Seuil de classification (Threshold)",
        min_value=0.05,
        max_value=0.95,
        value=0.50,
        step=0.05,
        help="Probabilité à partir de laquelle le SMS est catégorisé en SPAM."
    )
    
    if threshold >= 0.70:
        st.success("🛡️ **Posture Sécurisée Télécom** : Zéro ou quasi-zéro faux positif. Seuls les spams formellement identifiés sont bloqués.")
    elif threshold <= 0.30:
        st.warning("⚡ **Posture Détection Maximale** : Interception agressive des spams, avec risque accru d'interception de SMS légitimes.")
    else:
        st.info("⚖️ **Posture Équilibrée** : Compromis standard maximisant le F1-score.")
        
    st.divider()
    st.markdown("### 📊 Informations Modèle")
    st.markdown(f"• **Architecture** : {'Keras Bi-LSTM (Embedding 32d)' if model_type == 'deep_learning' else 'Baseline LogReg'}")
    st.markdown("• **Vocabulaire** : 10 000 tokens")
    st.markdown("• **Longueur max (padding)** : 100 mots")
    st.markdown("• **F1-Score Validation** : `0.949`")
    st.markdown("• **Recall Spam** : `93.3 %`")
    st.markdown("• **Candidat** : Christopher Gilleron")


# ==============================================================================
# EN-TÊTE PRINCIPAL
# ==============================================================================
st.markdown("""
<div class="main-header">
    <h1>📱 AT&T SMS Spam Detector</h1>
    <p>Système intelligent de détection du Smishing par Deep Learning séquentiel (Embedding Keras + Bi-LSTM)</p>
</div>
""", unsafe_allow_html=True)

# 4 Métriques en cartes
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><div class="metric-val">5 572</div><div class="metric-lbl">SMS dans le Corpus</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="metric-val">13.4 %</div><div class="metric-lbl">Taux de Spam Réel</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-val">93.3 %</div><div class="metric-lbl">Rappel (Spams captés)</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-val">{threshold:.2f}</div><div class="metric-lbl">Seuil de Décision Actif</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# SECTION TEST INTERACTIF
# ==============================================================================
st.subheader("🔍 Tester un SMS en direct")

# Boutons d'exemples rapides
st.caption("Sélectionnez un scénario type ou écrivez votre propre message :")
ex_col1, ex_col2, ex_col3, ex_col4 = st.columns(4)

default_sms = ""
if ex_col1.button("✅ SMS Légitime (Ami)"):
    default_sms = "Hey, are you free for lunch tomorrow around 1pm? Let me know!"
if ex_col2.button("🚨 Fausse Loterie (Spam)"):
    default_sms = "URGENT! You have won a 1,000 GBP cash prize or gift card. Call 09061701461 now to claim your prize!"
if ex_col3.button("🚨 Smishing Bancaire"):
    default_sms = "AT&T Security: We detected suspicious login on your mobile account. Verify immediately at http://att-secure-login.com"
if ex_col4.button("⚠️ SMS Court Ambigu"):
    default_sms = "Congratulations on your new job, call me later tonight."

sms_input = st.text_area(
    "Contenu du message SMS à analyser :",
    value=default_sms,
    height=110,
    placeholder="Saisissez ou collez ici le texte d'un SMS (en anglais)..."
)

if st.button("🚀 Analyser le SMS", type="primary", use_container_width=True):
    if not sms_input.strip():
        st.warning("Veuillez saisir un message avant de lancer l'analyse.")
    else:
        proba_spam = predict_spam_proba(sms_input, model, tokenizer, model_type)
        proba_ham = 1.0 - proba_spam
        is_spam = proba_spam >= threshold
        
        st.divider()
        res_col_left, res_col_right = st.columns([1.2, 1])
        
        with res_col_left:
            st.markdown("#### Verdict du Modèle")
            if is_spam:
                st.markdown(f"""
                <div class="badge-spam">
                    <span>🚨 SPAM / SMISHING DÉTECTÉ</span>
                </div>
                """, unsafe_allow_html=True)
                st.error(f"Le message dépasse le seuil d'alerte fixé à **{threshold*100:.0f} %** (Score de risque : **{proba_spam*100:.1f} %**).")
            else:
                st.markdown(f"""
                <div class="badge-ham">
                    <span>✅ MESSAGE LÉGITIME (HAM)</span>
                </div>
                """, unsafe_allow_html=True)
                st.success(f"Le message est considéré comme sûr (Probabilité de spam : **{proba_spam*100:.1f} %** < seuil {threshold*100:.0f} %).")
            
            # Jauge de risque
            st.markdown("##### Niveau de Risque Estimé")
            st.progress(proba_spam, text=f"Probabilité de menace : {proba_spam*100:.1f}%")
            
            # Action réseau recommandée
            st.markdown("##### Action Opérateur Recommandée :")
            if proba_spam >= 0.80:
                st.markdown("⛔ **Blocage automatique immédiat** (menace critique avérée).")
            elif proba_spam >= threshold:
                st.markdown("⚠️ **Redirection vers la boîte 'Spam / Courrier suspect'** de l'abonné.")
            else:
                st.markdown("📬 **Acheminement normal** vers la boîte de réception.")

        with res_col_right:
            st.markdown("#### Explicabilité & Mots-Clés Suspects")
            highlighted_html, keywords_found = highlight_suspects(sms_input)
            
            st.markdown("**Analyse textuelle annotée :**", unsafe_allow_html=True)
            st.markdown(f"<div style='background:#F8F9FA; padding:12px; border-radius:8px; border:1px solid #E2E8F0;'>{highlighted_html}</div>", unsafe_allow_html=True)
            
            if keywords_found:
                st.markdown(f"**Termes suspects détectés :** `{', '.join(keywords_found)}`")
            else:
                st.markdown("Aucun terme de vocabulaire suspect identifié.")

            st.markdown("##### Décomposition des Probabilités")
            prob_df = pd.DataFrame({
                "Classe": ["Ham (Légitime)", "Spam (Malveillant)"],
                "Probabilité": [f"{proba_ham*100:.2f} %", f"{proba_spam*100:.2f} %"],
                "Ratio": [proba_ham, proba_spam]
            })
            st.dataframe(prob_df[["Classe", "Probabilité"]], use_container_width=True, hide_index=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Projet de Certification Concepteur Développeur en Science des Données (CDSD) — Bloc 4 : Deep Learning & NLP • Christopher Gilleron • AT&T Inc.")
