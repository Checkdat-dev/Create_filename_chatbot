# pdf_naming.py

from step3_pdfreader import load_pdf_data


# ==========================================
# LOAD DATA FROM PDF
# ==========================================
pdf_data = load_pdf_data("data/naming.pdf")

DELOMRADE = pdf_data["delomrade"]
ANLAGGNINGSDEL = pdf_data["anlaggningsdel"]
TEKNIKOMRADE = pdf_data["teknikomrade"]
TEKNISKT_SYSTEM = pdf_data["tekniskt_system"]
DOKUMENTBETECKNING = pdf_data["dokumentbeteckning"]


def get_valid_systems():
    valid = []

    for main in TEKNISKT_SYSTEM.values():
        sub = main.get("sub", {})

        if isinstance(sub, dict):
            valid.extend(sub.keys())   # "62", "63"
        elif isinstance(sub, list):
            valid.extend(sub)

    return valid


VALID_SYSTEMS = get_valid_systems()


# ==========================================
# VALIDATION
# ==========================================

def validate_common(delomrade, teknik):
    if delomrade not in DELOMRADE:
        raise ValueError("Invalid Delområde")

    if teknik not in TEKNIKOMRADE:
        raise ValueError("Invalid Teknikområde")


def validate_ritning(anl, system):

    if not (isinstance(anl, str) and anl.isdigit() and 0 <= int(anl) <= 99):
        raise ValueError("Invalid Anläggningsdel")

    if system not in VALID_SYSTEMS:
        raise ValueError("Invalid Tekniskt system")


def validate_text(doc):
    if doc not in DOKUMENTBETECKNING:
        raise ValueError("Invalid Dokumentbeteckning")


def validate_lopnummer(lopnummer, length):
    if len(lopnummer) != length:
        raise ValueError(f"Löpnummer must be {length} characters")


# ==========================================
# GENERATION FUNCTIONS
# ==========================================

# -------- 1. RITNING --------
def generate_ritning(delomrade, anlaggning, teknik, system, lopnummer):
    validate_common(delomrade, teknik)
    validate_ritning(anlaggning, system)
    validate_lopnummer(lopnummer, 2)

    return f"{delomrade}{anlaggning}{teknik}{system}{lopnummer}"


# -------- 2. RITNINGSMODELL --------
def generate_ritningsmodell(teknik, delomrade, anlaggning, system, lopnummer):
    validate_common(delomrade, teknik)
    validate_ritning(anlaggning, system)
    validate_lopnummer(lopnummer, 2)

    return f"{teknik}{delomrade}{anlaggning}{system}{lopnummer}"


# -------- 3. TEXTDOKUMENT --------
def generate_textdokument(delomrade, teknik, dokumentbeteckning, lopnummer):
    validate_common(delomrade, teknik)
    validate_text(dokumentbeteckning)
    validate_lopnummer(lopnummer, 4)

    return f"{delomrade}{teknik}{dokumentbeteckning}{lopnummer}"