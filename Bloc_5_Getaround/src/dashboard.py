"""
Dashboard d'aide à la décision et d'estimation tarifaire GetAround.
Projet : GetAround Delay & Pricing Optimization - Certification CDSD Bloc 5
Auteur : Christopher Gilleron
"""

import os
import requests
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="GetAround Decision & Pricing Hub",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pour une interface soignée et moderne
st.markdown("""
<style>
    .main {
        background-color: #F8F9FA;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #00C2B2;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #1B2A4A;
    }
    .metric-label {
        font-size: 14px;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-sub {
        font-size: 13px;
        color: #28A745;
        font-weight: 500;
    }
    .reco-box {
        background: linear-gradient(135deg, #1B2A4A 0%, #2A3F6D 100%);
        color: white;
        padding: 22px;
        border-radius: 12px;
        margin-top: 20px;
        border: 1px solid #00C2B2;
    }
    .price-box {
        background: linear-gradient(135deg, #00C2B2 0%, #009E91 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)


# --- CHARGEMENT DES DONNÉES EN CACHE ---

@st.cache_data
def load_datasets():
    """Charge les datasets de retards et de tarification."""
    delay_candidates = [
        "get_around_delay_analysis.xlsx",
        "data/get_around_delay_analysis.xlsx",
        os.path.join(os.path.dirname(__file__), "get_around_delay_analysis.xlsx"),
        os.path.join(os.path.dirname(__file__), "..", "get_around_delay_analysis.xlsx"),
        os.path.join(os.path.dirname(__file__), "..", "data", "get_around_delay_analysis.xlsx")
    ]
    pricing_candidates = [
        "get_around_pricing_project.csv",
        "data/get_around_pricing_project.csv",
        os.path.join(os.path.dirname(__file__), "get_around_pricing_project.csv"),
        os.path.join(os.path.dirname(__file__), "..", "get_around_pricing_project.csv"),
        os.path.join(os.path.dirname(__file__), "..", "data", "get_around_pricing_project.csv")
    ]
    
    delay_path = next((p for p in delay_candidates if os.path.exists(p)), "get_around_delay_analysis.xlsx")
    pricing_path = next((p for p in pricing_candidates if os.path.exists(p)), "get_around_pricing_project.csv")

    df_delay = pd.read_excel(delay_path, sheet_name="rentals_data")
    df_pricing = pd.read_csv(pricing_path)
    if "Unnamed: 0" in df_pricing.columns:
        df_pricing = df_pricing.drop(columns=["Unnamed: 0"])
        
    return df_delay, df_pricing


@st.cache_resource
def load_ml_model():
    """Charge la pipeline de tarification entraînée."""
    model_candidates = [
        "model.joblib",
        "models/model.joblib",
        os.path.join(os.path.dirname(__file__), "model.joblib"),
        os.path.join(os.path.dirname(__file__), "..", "model.joblib"),
        os.path.join(os.path.dirname(__file__), "..", "models", "model.joblib")
    ]
    model_path = next((p for p in model_candidates if os.path.exists(p)), None)
    if model_path and os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except Exception:
            return None
    return None


df_delay, df_pricing = load_datasets()
pipeline_model = load_ml_model()


# --- SIDEBAR NAVIGATION ---

st.sidebar.title("🚗 GetAround")
st.sidebar.caption("Plateforme d'Aide à la Décision")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 1. Analyse Retards & Seuil de Sécurité",
        "💶 2. Simulateur de Prix Dynamique"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("🔗 **API FastAPI :** [Documentation Swagger](https://elkristobal59-getaround-pricing-api.hf.space/docs)")
st.sidebar.caption("Getaround Fleet Management v1.0")


# ==============================================================================
# PAGE 1 : ANALYSE DES RETARDS ET SIMULATION DE SEUIL
# ==============================================================================

if page == "📊 1. Analyse Retards & Seuil de Sécurité":
    st.title("🚗 Analyse des Retards & Optimisation du Seuil de Battement")
    st.markdown("""
    Lorsqu'un locataire restitue son véhicule en retard, cela pénalise le conducteur suivant (attente, mécontentement, annulation).
    **Le défi métier :** Imposer un délai minimum de battement entre 2 locations supprime les litiges mais bloque des créneaux de réservation, réduisant potentiellement les revenus du propriétaire.
    """)

    # Préparation des données pour analyse
    df_ended = df_delay[df_delay["state"] == "ended"].copy()
    late_mask = df_ended["delay_at_checkout_in_minutes"] > 0
    late_rentals = df_ended[late_mask]
    
    # Locations consécutives
    df_delay_sub = df_ended[["rental_id", "delay_at_checkout_in_minutes"]].rename(
        columns={"rental_id": "previous_ended_rental_id", "delay_at_checkout_in_minutes": "previous_delay"}
    )
    df_consecutive = df_delay.merge(df_delay_sub, on="previous_ended_rental_id", how="inner")
    df_consecutive["is_conflict"] = df_consecutive["previous_delay"] > df_consecutive["time_delta_with_previous_rental_in_minutes"]

    total_rentals = len(df_delay)
    ended_count = len(df_ended)
    late_pct = (len(late_rentals) / ended_count) * 100
    median_delay = late_rentals["delay_at_checkout_in_minutes"].median()
    consecutive_count = len(df_consecutive)
    consecutive_pct = (consecutive_count / total_rentals) * 100
    conflict_count = df_consecutive["is_conflict"].sum()

    # --- LIGNE DE KPIS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Volume de locations</div>
            <div class="metric-value">{total_rentals:,}</div>
            <div class="metric-sub">{ended_count:,} terminées avec état</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Taux de retard global</div>
            <div class="metric-value">{late_pct:.1f} %</div>
            <div class="metric-sub">Médiane des retards : {median_delay:.0f} min</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Locations enchaînées</div>
            <div class="metric-value">{consecutive_count:,}</div>
            <div class="metric-sub">{consecutive_pct:.1f} % du volume global</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Litiges réels constatés</div>
            <div class="metric-value" style="color: #E74C3C;">{conflict_count}</div>
            <div class="metric-sub">{conflict_count/consecutive_count*100:.1f} % des enchaînements</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- GRAPHIQUES EXPLORATOIRES ---
    c_graph1, c_graph2 = st.columns(2)

    with c_graph1:
        st.subheader("📈 Distribution des retards au checkout")
        plot_data = df_ended["delay_at_checkout_in_minutes"].dropna().clip(-60, 360)
        fig_hist = px.histogram(
            plot_data, 
            nbins=70,
            title="Répartition des minutes de retard (tronqué à [-60, 360] min)",
            labels={"value": "Retard (minutes)", "count": "Nombre de locations"},
            color_discrete_sequence=["#1B2A4A"]
        )
        fig_hist.add_vline(x=0, line_dash="dash", line_color="#E74C3C", annotation_text="À l'heure (0 min)")
        fig_hist.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=380)
        st.plotly_chart(fig_hist, use_container_width=True)

    with c_graph2:
        st.subheader("📱 Connect vs 🤝 Mobile (Remise clé)")
        type_stats = df_ended.groupby("checkin_type")["delay_at_checkout_in_minutes"].apply(
            lambda s: (s > 0).mean() * 100
        ).reset_index(name="late_rate")
        type_stats["checkin_type"] = type_stats["checkin_type"].replace({
            "connect": "GetAround Connect (43%)",
            "mobile": "Mobile avec RDV (61%)"
        })
        
        fig_bar = px.bar(
            type_stats,
            x="checkin_type",
            y="late_rate",
            color="checkin_type",
            color_discrete_sequence=["#00C2B2", "#E74C3C"],
            text_auto=".1f",
            title="Taux de retard selon le mode de check-in (%)",
            labels={"late_rate": "% de retards", "checkin_type": "Mode de restitution"}
        )
        fig_bar.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), height=380)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- SIMULATEUR DÉCISIONNEL DE SEUIL ---
    st.subheader("🎛️ Simulateur Décisionnel d'Impact de Seuil (Threshold Simulator)")
    st.markdown("""
    Ajustez le seuil de battement minimal imposé entre deux réservations consécutives pour observer en direct
    l'arbitrage (**trade-off**) entre **litiges évités** et **créneaux de réservation potentiellement perdus**.
    """)

    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        threshold_val = st.slider("Seuil minimum de battement (minutes)", 0, 360, 60, step=15)
    with col_s2:
        scope_choice = st.selectbox(
            "Périmètre d'application",
            ["Toutes les voitures", "GetAround Connect uniquement", "Mobile (remise physique) uniquement"]
        )

    # Filtrage du périmètre
    if scope_choice == "GetAround Connect uniquement":
        scope_consecutive = df_consecutive[df_consecutive["checkin_type"] == "connect"].copy()
        total_scope_volume = len(df_delay[df_delay["checkin_type"] == "connect"])
    elif scope_choice == "Mobile (remise physique) uniquement":
        scope_consecutive = df_consecutive[df_consecutive["checkin_type"] == "mobile"].copy()
        total_scope_volume = len(df_delay[df_delay["checkin_type"] == "mobile"])
    else:
        scope_consecutive = df_consecutive.copy()
        total_scope_volume = total_rentals

    total_conflicts_scope = scope_consecutive["is_conflict"].sum()
    blocked_rentals = (scope_consecutive["time_delta_with_previous_rental_in_minutes"] < threshold_val).sum()
    solved_conflicts = ((scope_consecutive["is_conflict"]) & 
                        (scope_consecutive["time_delta_with_previous_rental_in_minutes"] < threshold_val)).sum()
    remaining_conflicts = total_conflicts_scope - solved_conflicts

    res1, res2, res3 = st.columns(3)
    with res1:
        st.metric(
            "Locations bloquées / décalées",
            f"{blocked_rentals:,}",
            f"{blocked_rentals / total_scope_volume * 100:.2f} % du volume total"
        )
    with res2:
        st.metric(
            "Conflits & annulations évités",
            f"{solved_conflicts:,}",
            f"{solved_conflicts / total_conflicts_scope * 100:.1f} % des litiges résolus" if total_conflicts_scope > 0 else "0%"
        )
    with res3:
        st.metric(
            "Litiges résiduels",
            f"{remaining_conflicts:,}",
            f"-{solved_conflicts} litiges"
        )

    # Courbe de Trade-Off
    thresholds_range = list(range(0, 361, 15))
    list_blocked, list_solved = [], []
    for t in thresholds_range:
        blk = (scope_consecutive["time_delta_with_previous_rental_in_minutes"] < t).sum()
        slv = ((scope_consecutive["is_conflict"]) & 
               (scope_consecutive["time_delta_with_previous_rental_in_minutes"] < t)).sum()
        list_blocked.append((blk / total_scope_volume) * 100)
        list_solved.append((slv / total_conflicts_scope) * 100 if total_conflicts_scope > 0 else 0)

    fig_tradeoff = go.Figure()
    fig_tradeoff.add_trace(go.Scatter(
        x=thresholds_range, y=list_solved,
        mode='lines+markers',
        name='% Litiges résolus (Bénéfice UX)',
        line=dict(color='#00C2B2', width=3)
    ))
    fig_tradeoff.add_trace(go.Scatter(
        x=thresholds_range, y=list_blocked,
        mode='lines+markers',
        name='% Locations bloquées (Risque Revenu)',
        line=dict(color='#E74C3C', width=3)
    ))
    fig_tradeoff.add_vline(x=threshold_val, line_dash="dash", line_color="#F39C12", 
                           annotation_text=f"Seuil choisi : {threshold_val} min")
    fig_tradeoff.update_layout(
        title="Courbes d'arbitrage : % Litiges résolus vs % Chiffre d'affaires exposé",
        xaxis_title="Seuil de battement minimum (minutes)",
        yaxis_title="Pourcentage (%)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
        height=400
    )
    st.plotly_chart(fig_tradeoff, use_container_width=True)

    # Recommandation Business
    st.markdown("""
    <div class="reco-box">
        <h3>💡 Recommandation Stratégique pour le Product Manager</h3>
        <p>
        1. <b>Seuil optimal recommandé : 60 minutes.</b> À ce palier, nous résolvons <b>67 % des litiges</b> (146 conflits évités) pour seulement <b>1,9 % du volume global de locations bloqué</b>.
        <br>
        2. <b>Déploiement prioritaire sur GetAround Connect :</b> Bien que les utilisateurs Connect soient plus ponctuels (43 % de retard vs 61 % en Mobile), le parcours 100 % autonome rend l'attente du locataire suivant particulièrement frustrante.
        <br>
        3. <b>Rendement décroissant au-delà :</b> Passer de 60 à 180 min n'apporte que 23 points de résolution supplémentaires mais multiplie par plus de 2,5 le nombre de réservations bloquées.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 2 : SIMULATEUR DE PRIX DYNAMIQUE
# ==============================================================================

else:
    st.title("💶 Simulateur d'Estimation du Prix de Location")
    st.markdown("""
    Aidez les propriétaires partenaires à positionner leur véhicule au prix optimal du marché.
    Ce simulateur exploite notre **Random Forest Regressor (R² = 0.729, MAE = 10.78 €)** déployé en production.
    """)

    if pipeline_model is None:
        st.error("⚠️ Modèle de machine learning non trouvé dans `models/model.joblib`. Veuillez exécuter `python src/train.py`.")
        st.stop()

    brands = sorted(df_pricing["model_key"].dropna().unique())
    fuels = sorted(df_pricing["fuel"].dropna().unique())
    car_types = sorted(df_pricing["car_type"].dropna().unique())
    colors = sorted(df_pricing["paint_color"].dropna().unique())

    col_c1, col_c2, col_c3 = st.columns(3)

    with col_c1:
        st.subheader("🚘 Profil du véhicule")
        sel_brand = st.selectbox("Marque", brands, index=brands.index("Peugeot") if "Peugeot" in brands else 0)
        sel_type = st.selectbox("Carrosserie", car_types, index=car_types.index("sedan") if "sedan" in car_types else 0)
        sel_fuel = st.selectbox("Carburant", fuels, index=fuels.index("diesel") if "diesel" in fuels else 0)
        sel_color = st.selectbox("Couleur", colors, index=colors.index("black") if "black" in colors else 0)

    with col_c2:
        st.subheader("⚙️ Spécifications techniques")
        sel_mileage = st.slider("Kilométrage (km)", 0, 300000, 75000, step=5000)
        sel_power = st.slider("Puissance moteur (cv)", 50, 450, 130, step=5)

    with col_c3:
        st.subheader("✨ Options & Équipements")
        has_connect = st.checkbox("GetAround Connect (déverrouillage mobile)", value=True)
        has_gps = st.checkbox("GPS embarqué", value=True)
        has_ac = st.checkbox("Climatisation", value=True)
        is_auto = st.checkbox("Boîte automatique", value=False)
        has_parking = st.checkbox("Parking privé pour restitution", value=True)
        has_regulator = st.checkbox("Régulateur de vitesse", value=True)
        has_winter_tires = st.checkbox("Pneus neige / hiver", value=False)

    predict_btn = st.button("🚀 Calculer le prix recommandé", type="primary", use_container_width=True)

    if predict_btn:
        input_dict = {
            "model_key": sel_brand,
            "mileage": int(sel_mileage),
            "engine_power": int(sel_power),
            "fuel": sel_fuel,
            "paint_color": sel_color,
            "car_type": sel_type,
            "private_parking_available": bool(has_parking),
            "has_gps": bool(has_gps),
            "has_air_conditioning": bool(has_ac),
            "automatic_car": bool(is_auto),
            "has_getaround_connect": bool(has_connect),
            "has_speed_regulator": bool(has_regulator),
            "winter_tires": bool(has_winter_tires)
        }
        
        # 1. Tentative d'appel en temps réel à l'API FastAPI
        api_url = os.getenv("API_URL", "https://elkristobal59-getaround-pricing-api.hf.space")
        pred_price = None
        rounded_price = None
        min_price = None
        max_price = None
        prediction_source = "Modèle Pipeline local"

        try:
            res = requests.post(f"{api_url}/predict", json=input_dict, timeout=10.0)
            if res.status_code == 200:
                data = res.json()
                pred_price = data["predicted_price_per_day"]
                rounded_price = data["rounded_price"]
                min_price = data["recommended_range"]["min_price"]
                max_price = data["recommended_range"]["max_price"]
                prediction_source = f"⚡ Inférence en direct via API FastAPI ({api_url})"
        except Exception:
            pass

        # 2. Fallback direct sur le modèle local si l'API est indisponible
        if pred_price is None and pipeline_model is not None:
            df_input = pd.DataFrame([input_dict])
            for col in ['private_parking_available', 'has_gps', 'has_air_conditioning',
                        'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires']:
                df_input[col] = df_input[col].astype(int)
            pred_price = float(pipeline_model.predict(df_input)[0])
            rounded_price = int(round(pred_price))
            min_price = max(10, rounded_price - 11)
            max_price = rounded_price + 11
            prediction_source = "📦 Modèle Pipeline embarqué (secours local)"

        # Référence marché
        similar_cars = df_pricing[
            (df_pricing["car_type"] == sel_type) & (df_pricing["fuel"] == sel_fuel)
        ]
        market_median = similar_cars["rental_price_per_day"].median() if len(similar_cars) > 0 else df_pricing["rental_price_per_day"].median()

        st.markdown(f"""
        <div class="price-box">
            <h2>Prix recommandé : {rounded_price} € / jour</h2>
            <p style="font-size: 16px;">Fourchette conseillée au propriétaire : <b>{min_price} € – {max_price} € / jour</b></p>
            <p style="font-size: 14px; opacity: 0.9;">Médiane du marché pour ce segment ({sel_type} + {sel_fuel}) : <b>{market_median:.0f} € / jour</b></p>
            <p style="font-size: 12px; margin-top: 10px; background: rgba(255,255,255,0.2); border-radius: 6px; padding: 4px;">{prediction_source}</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("""
        ℹ️ **Remarque méthodologique :** La puissance fiscale et le kilométrage constituent plus de 70 % de la valeur locative du véhicule.
        Les options (Connect, GPS, Régulateur) favorisent le taux de conversion et l'attractivité de l'annonce mais ne justifient qu'une surcote modérée (+2 à +5 €/jour).
        """)
