from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pyppeteer import launch
import uvicorn

app = FastAPI()

class CompteRendu(BaseModel):
    date_cr: str; entite: str; escale: str
    retard: bool; reclam_cie: bool; impact_secu: bool; dysfonc: bool
    compagnie: str; num_vol: str; immat: str; date_evenement: str
    heure_locale: str; lieu: str; jour_nuit: str; meteo: str
    desc_succincte: str; desc_detaillee: str
    sig_redacteur_nom: str; sig_redacteur_box: str
    analyse_encadrement: str; diff_qse: bool; diff_cie: bool; diff_aeroport: bool
    sig_encadre_nom: str; sig_encadre_box: str
    analyse_qse_text: str; cl_ev: bool; cl_inc: bool; cl_inc_g: bool; cl_acc: bool
    st_clos_s: bool; st_ouvert: bool; st_clos_d: bool
    dsac: bool; bea: bool; nav_air: bool; autre: bool
    sig_qse_nom: str; sig_qse_box: str

async def generer_pdf(data: CompteRendu):
    path = f"CRE_{data.escale}.pdf"
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    # On charge la page servie par FastAPI
    await page.goto('http://localhost:10000', {'waitUntil': 'networkidle0'})
    
    await page.evaluate(f"""(d) => {{
        const setV = (id, v) => {{ if(document.getElementById(id)) document.getElementById(id).value = v; }};
        const setC = (id, v) => {{ if(document.getElementById(id)) document.getElementById(id).checked = v; }};
        const setT = (id, v) => {{ if(document.getElementById(id)) document.getElementById(id).innerText = v; }};
        
        // Page 1
        setV('date_cr', d.date_cr); setV('entite', d.entite); setV('escale', d.escale);
        setC('retard', d.retard); setC('reclam_cie', d.reclam_cie); setC('impact_secu', d.impact_secu); setC('dysfonc', d.dysfonc);
        setV('compagnie', d.compagnie); setV('num_vol', d.num_vol); setV('immat', d.immat);
        setV('date_evenement', d.date_evenement); setV('heure_locale', d.heure_locale); setV('lieu', d.lieu);
        setV('jour_nuit', d.jour_nuit); setV('meteo', d.meteo);
        setV('desc_succincte', d.desc_succincte); setV('desc_detaillee', d.desc_detaillee);
        setV('sig_redacteur_nom', d.sig_redacteur_nom); setT('sig_redacteur_box', d.sig_redacteur_box);
        setV('analyse_encadrement', d.analyse_encadrement);
        setC('diff_qse', d.diff_qse); setC('diff_cie', d.diff_cie); setC('diff_aeroport', d.diff_aeroport);
        setV('sig_encadre_nom', d.sig_encadre_nom); setT('sig_encadre_box', d.sig_encadre_box);

        // Page 2
        setV('analyse_qse_text', d.analyse_qse_text);
        setC('cl_ev', d.cl_ev); setC('cl_inc', d.cl_inc); 
        setC('st_clos_s', d.st_clos_s); setC('st_ouvert', d.st_ouvert);
        setV('sig_qse_nom', d.sig_qse_nom); setT('sig_qse_box', d.sig_qse_box);
    }}""", data.model_dump())
    
    await page.pdf({'path': path, 'format': 'A4', 'printBackground': True, 'preferCSSPageSize': True})
    await browser.close()
    return path

@app.post("/submit")
async def submit(data: CompteRendu):
    p = await generer_pdf(data)
    return FileResponse(p)

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)