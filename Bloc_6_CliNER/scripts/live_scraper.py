import os
from playwright.sync_api import sync_playwright
import time

"""
Module de collecte et téléchargement des protocoles d'essais cliniques (ClinicalTrials.gov).
Fournit deux stratégies d'acquisition :
1. Extraction automatisée via navigateur headless (Playwright) pour les recherches exploratoires.
2. Téléchargement direct par requête HTTP sur le CDN ClinicalTrials pour les identifiants NCT connus.
"""

def run_scraper(condition: str, max_results: int = 5) -> str:
    """
    Télécharge les protocoles PDF associés à une condition médicale donnée.
    
    Args:
        condition: Pathologie ou terme de recherche clinique (ex: 'Diabetes').
        max_results: Nombre maximal d'essais à traiter.
        
    Returns:
        Chemin du répertoire local contenant les fichiers téléchargés.
    """
    output_dir = os.path.abspath(f"data/live_pdfs_{condition.replace(' ', '_')}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Isolation de l'exécution Playwright dans un sous-processus si invoqué hors du thread principal
    import threading
    if threading.current_thread() != threading.main_thread():
        print(f"Lancement de Playwright via subprocess pour '{condition}'...")
        import subprocess, sys
        subprocess.run([sys.executable, __file__, condition, str(max_results)])
        return output_dir

    print(f"Lancement de Playwright pour scrapper {max_results} essais sur '{condition}'...")
    
    import requests
    downloaded_count = 0
    page_token = None
    
    try:
        # Lancement d'un navigateur Chrome invisible (headless=True)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # API REST V2 de ClinicalTrials.gov
            url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={condition}&pageSize=100&fields=NCTId,DocumentSection"
            
            while downloaded_count < max_results:
                current_url = url
                if page_token:
                    current_url += f"&pageToken={page_token}"
                    
                print("Recherche de protocoles avec PDF via l'API...")
                try:
                    response = requests.get(current_url, timeout=10)
                    data = response.json()
                except Exception as e:
                    print(f"Erreur API: {e}")
                    break
                    
                studies = data.get("studies", [])
                if not studies:
                    break
                    
                # On parcourt chaque étude médicale remontée par l'API
                for study in studies:
                    nct_id = study.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
                    
                    # On vérifie si l'étude a bien un fichier PDF attaché (DocumentSection)
                    docs = study.get("documentSection", {}).get("largeDocumentModule", {}).get("largeDocs", [])
                    
                    has_pdf = False
                    for doc in docs:
                        filename = doc.get("filename", "")
                        if filename.lower().endswith(".pdf"):
                            has_pdf = True
                            break
                            
                    if not has_pdf:
                        continue # Si pas de PDF, on passe au patient suivant !
                        
                    study_url = f"https://clinicaltrials.gov/study/{nct_id}"
                    print(f"[{downloaded_count+1}/{max_results}] Téléchargement du PDF pour l'essai {nct_id}...")
                    
                    # 🤖 AUTOMATISATION WEB (RPA)
                    try:
                        page.goto(study_url, wait_until="networkidle", timeout=30000)
                        links = page.locator("a")
                        count = links.count()
                        
                        pdf_downloaded = False
                        # On scanne tous les liens de la page à la recherche d'un lien ".pdf"
                        for i in range(count):
                            href = links.nth(i).get_attribute("href")
                            if href and (".pdf" in href.lower() or "large-docs" in href.lower()):
                                try:
                                    # Clic automatique et interception du téléchargement
                                    with page.expect_download(timeout=15000) as download_info:
                                        links.nth(i).click(force=True)
                                    download = download_info.value
                                    
                                    safe_name = download.suggested_filename
                                    if not safe_name.endswith(".pdf"):
                                        safe_name += ".pdf"
                                        
                                    filepath = os.path.join(output_dir, f"{nct_id}_{safe_name}")
                                    download.save_as(filepath)
                                    
                                    pdf_downloaded = True
                                    downloaded_count += 1
                                    break 
                                except Exception:
                                    pass 
                                    
                        if downloaded_count >= max_results:
                            break
                            
                    except Exception as e:
                        print(f"Erreur chargement page {nct_id}: {e}")
                        
                if downloaded_count >= max_results:
                    break
                    
                # Gestion de la pagination de l'API
                page_token = data.get("nextPageToken")
                if not page_token:
                    break
        
            browser.close()
    except Exception as e:
        print(f"Erreur globale scraping : {e}")

    return output_dir

def download_pdf_for_nctid(nct_id: str, output_dir: str) -> str:
    """
    Télécharge le PDF pour un identifiant NCT spécifique via l'API v2 et le CDN ClinicalTrials.
    
    Args:
        nct_id: Identifiant de l'essai clinique (ex: 'NCT01849835').
        output_dir: Répertoire de destination du fichier téléchargé.
        
    Returns:
        Chemin local du fichier téléchargé ou None si aucun PDF n'est disponible.
    """
    import requests
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    try:
        # 1. On interroge l'API pour récupérer le vrai nom du fichier PDF
        res = requests.get(f"https://clinicaltrials.gov/api/v2/studies/{nct_id}?fields=DocumentSection", timeout=10)
        data = res.json()
        docs = data.get("documentSection", {}).get("largeDocumentModule", {}).get("largeDocs", [])
        
        pdf_filename = None
        for doc in docs:
            if str(doc.get("filename", "")).lower().endswith(".pdf"):
                pdf_filename = doc.get("filename")
                break
                
        if not pdf_filename:
            print(f"Aucun PDF attaché trouvé pour {nct_id} sur ClinicalTrials.gov")
            return None
            
        # 2. ⚡ REVERSE ENGINEERING DU CDN ⚡
        # Le CDN stocke les fichiers dans un dossier basé sur les 2 derniers chiffres du NCT_ID
        last_two = nct_id[-2:]
        pdf_url = f"https://cdn.clinicaltrials.gov/large-docs/{last_two}/{nct_id}/{pdf_filename}"
        
        print(f"Téléchargement du PDF via CDN: {pdf_url}")
        pdf_res = requests.get(pdf_url, stream=True, timeout=20)
        
        if pdf_res.status_code == 200:
            # Sauvegarde en mode Binaire (wb = write binary)
            filepath = os.path.join(output_dir, f"{nct_id}_{pdf_filename}")
            with open(filepath, "wb") as f:
                for chunk in pdf_res.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"DOWNLOADED:{filepath}")
            return filepath
        else:
            print(f"Erreur téléchargement CDN ({pdf_res.status_code}): {pdf_url}")
            
    except Exception as e:
        print(f"Erreur téléchargement API pour {nct_id}: {e}")
        
    return None

if __name__ == "__main__":
    # Point d'entrée pour le sous-processus système (évite le crash thread Streamlit)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "FETCH_ID":
        nct_id = sys.argv[2]
        out_dir = sys.argv[3]
        download_pdf_for_nctid(nct_id, out_dir)
    else:
        cond = sys.argv[1] if len(sys.argv) > 1 else "Breast Cancer"
        m_res = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        run_scraper(cond, m_res)
