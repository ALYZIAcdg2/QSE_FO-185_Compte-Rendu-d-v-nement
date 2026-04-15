function showAlert(m) {
    const al = document.getElementById('custom-alert');
    document.getElementById('alert-message').textContent = m;
    al.style.display = 'flex';
}
function closeAlert() { document.getElementById('custom-alert').style.display = 'none'; }

function calculerScore() {
    ['entite', 'escale', 'compagnie', 'lieu'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = el.value.toUpperCase();
    });
}

function getFormData() {
    const getV = (id) => document.getElementById(id)?.value || "";
    const getC = (id) => document.getElementById(id)?.checked || false;
    const getT = (id) => document.getElementById(id)?.innerText || "";

    return {
        date_cr: getV('date_cr'), entite: getV('entite'), escale: getV('escale'),
        retard: getC('retard'), reclam_cie: getC('reclam_cie'), impact_secu: getC('impact_secu'), dysfonc: getC('dysfonc'),
        compagnie: getV('compagnie'), num_vol: getV('num_vol'), immat: getV('immat'),
        date_evenement: getV('date_evenement'), heure_locale: getV('heure_locale'), lieu: getV('lieu'),
        jour_nuit: getV('jour_nuit'), meteo: getV('meteo'),
        desc_succincte: getV('desc_succincte'), desc_detaillee: getV('desc_detaillee'),
        sig_redacteur_nom: getV('sig_redacteur_nom'), sig_redacteur_box: getT('sig_redacteur_box'),
        analyse_encadrement: getV('analyse_encadrement'),
        diff_qse: getC('diff_qse'), diff_cie: getC('diff_cie'), diff_aeroport: getC('diff_aeroport'),
        sig_encadre_nom: getV('sig_encadre_nom'), sig_encadre_box: getT('sig_encadre_box'),
        analyse_qse_text: getV('analyse_qse_text'),
        cl_ev: getC('cl_ev'), cl_inc: getC('cl_inc'), cl_inc_g: false, cl_acc: false,
        st_clos_s: getC('st_clos_s'), st_ouvert: getC('st_ouvert'), st_clos_d: false,
        dsac: false, bea: false, nav_air: false, autre: false,
        sig_qse_nom: getV('sig_qse_nom'), sig_qse_box: getT('sig_qse_box')
    };
}

async function genererPDF() {
    calculerScore();
    const data = getFormData();
    showAlert("Génération du PDF...");
    try {
        const res = await fetch('/submit?action=pdf', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (res.ok) {
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `CRE_${data.escale || 'DOC'}.pdf`;
            a.click();
            showAlert("✅ Terminé !");
        }
    } catch (e) { showAlert("❌ Erreur serveur"); }
}

async function envoyerEmail() {
    calculerScore();
    const data = getFormData();
    showAlert("📤 Envoi silencieux via SendGrid...");

    try {
        const response = await fetch('/submit?action=email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showAlert("✅ Email envoyé avec succès");
        } else {
            showAlert("❌ Erreur lors de l'envoi SendGrid.");
        }
    } catch (error) {
        showAlert("❌ Impossible de joindre le serveur.");
    }
}