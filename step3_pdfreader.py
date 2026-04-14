
import pdfplumber


def load_pdf_data(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # ==============================
    # VALUES (UNCHANGED)
    # ==============================

    delomrade = [str(i) for i in range(0, 10)]

    anlaggningsdel = [f"{i:02d}" for i in range(0, 100)]

    teknikomrade = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    dokumentbeteckning = [
        "A1","A2","A3","A4","A5","A8","A9",
        "B1","B2","B3","B4","B5","B6","B7","B8","B9",
        "C1","C2","C3","C4","C5","C6","C7","C8","C9","CA",
        "D2","D3","D4","D5","D6","D7","D8","D9",
        "E1","E2","E3","E4","E5","E6","E7","E8",
        "F1","F3","F4","F5","F6","F7","F8",
        "G2","G3","G4","G5","G6","G7",
        "H1","H3","H5","H7",
        "J1","J2","J4","J5",
        "K1","K2","K3","K4"
    ]

    # ==============================
    #  STRUCTURED TEKNISKT SYSTEM
    # ==============================

    tekniskt_system = {
        "00": {
            "name": "Väg och trafik",
            "sub": ["01","02","03","04","05","08","09"]
        },
        "10": {
            "name": "Mark",
            "sub": ["11","12","13","14","15","16","17","18","19"]
        },
        "20": {
            "name": "Anläggningsbyggdelar",
            "sub": ["21","22","23","24","25","26","27","28","29","2A"]
        },
        "30": {
            "name": "Husbyggdelar",
            "sub": ["32","33","34","35","36","37","38","39"]
        },
        "40": {
            "name": "Väganordningar",
            "sub": ["41","42","43","44","45","46","47","48"]
        },
        "50": {
            "name": "Rör- och ventilationssystem",
            "sub": ["51","53","54","55","56","57","58"]
        },
        "60": {
            "name": "Elanläggningar",
            "sub": ["62","63","64","65","66","67"]
        },
        "70": {
            "name": "Transportanläggningar",
            "sub": ["71","73","75","77"]
        },
        "80": {
            "name": "Styrsystem",
            "sub": ["81","82","84","85","86"]
        },
        "90": {
            "name": "Sammansatt",
            "sub": ["91","92","93","94","95","96","97","98"]
        }
    }

    return {
        "delomrade": delomrade,
        "anlaggningsdel": anlaggningsdel,
        "teknikomrade": teknikomrade,
        "tekniskt_system": tekniskt_system,
        "dokumentbeteckning": dokumentbeteckning
    }