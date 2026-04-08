import re
import pandas as pd

from step1_excelreader import load_excel, get_delomrade


ENTREPRENAD_LIST = [
    "E00","E01","E02","E03","E04","E05","E06","E06A","E06B",
    "E08","E09","E10","E11","E12","E13","E14","E15",
    "EB02","EB03","EB04","EB05","EB06","EB07","EB08",
    "FA36","FA37","FU.E06","IBTL01","JPSHFU01","JPSHFU02",
    "SE02","SE03","SE05","SE08","SE16","SE17","SE18","SE19",
    "SE20","SE21","SE22","SPD","TRV","TSB01","UM02","UM03",
    "JPSHFU03","SE23","SE24","SE25","BUP08","BUP09","SE26","SE27",
    "A001","BBP01","BBP03","BBP04","BBP05","BBS01","BBT01",
    "BEF01","BIK01","BIK02","BPU01","BTH01","BTH02","BTH03",
    "BTH04","BTH05","BTH06","BU01","BU02","BU03","BUA01",
    "BUB01","BUF02","BUU01","BUK02","BUP01","BUP03","BUP04","BUP06",
    "FA28.1","FA28.2","FA14.2"
]


def normalize_text(text):
    return re.sub(r"\s+", " ", str(text).strip().lower())


def is_real_value(x):
    return pd.notna(x) and str(x).strip() != "" and str(x).strip().lower() != "nan"


def is_valid_type_code(code):
    code = str(code).strip()
    return bool(re.fullmatch(r"\d+[A-Za-z]?", code))


# Teknikområde mapping (NR + BENÄMNING)
def get_teknikomrade_mapping(data):
    df = data["Gruppnummer"]

    mapping = {}
    started = False

    for _, row in df.iterrows():
        nr = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
        ben = str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else ""

        nr = nr.replace("\xa0", "").strip()
        ben = ben.replace("\xa0", "").strip()

        if not started:
            if nr == "NR" and ben == "BENÄMNING":
                started = True
            continue

        if not nr or not ben:
            continue

        if nr.lower() == "nr":
            continue

        mapping[f"{nr} - {ben}"] = nr

    return mapping


def get_konstruktiv_mapping(data):
    df = data["Mappning BSAB-Konstruktions kod"]

    mapping = {}

    for _, row in df.iterrows():
        left = str(row.iloc[0]).strip() if is_real_value(row.iloc[0]) else ""
        right = str(row.iloc[1]).strip() if len(row) > 1 and is_real_value(row.iloc[1]) else ""

        if not left or not right:
            continue

        if left.lower() == "konstruktiv teknik kod":
            continue

        mapping[left] = right

        if " - " in left:
            short_key = left.split(" - ")[0].strip()
            mapping[short_key] = right

    return mapping


def get_type_mappings(data):
    df = data["Databas-Text-Ritningsnummer"]

    document_map = {}
    drawing_map = {}

    current_section = None

    for _, row in df.iterrows():
        col1 = str(row.iloc[1]).strip() if len(row) > 1 and is_real_value(row.iloc[1]) else ""
        col2 = str(row.iloc[2]).strip() if len(row) > 2 and is_real_value(row.iloc[2]) else ""

        col1_norm = normalize_text(col1)

        # START: Textdokument
        if col1_norm == "textdokument":
            current_section = "Dokument"
            continue

        # START: Ritningar
        if col1_norm == "ritningar":
            current_section = "Ritning"
            continue

        if not col1 or not col2:
            continue

        if not is_valid_type_code(col2):
            continue

        key = normalize_text(col1)

        if current_section == "Dokument":
            document_map[key] = col2

        elif current_section == "Ritning":
            drawing_map[key] = col2

    return document_map, drawing_map

def get_model_types(data):
    df = data["Redovisningssätt (modeller)"]

    mapping = {}
    started = False

    for _, row in df.iterrows():
        code = str(row.iloc[2]).strip() if len(row) > 2 and is_real_value(row.iloc[2]) else ""
        text = str(row.iloc[3]).strip() if len(row) > 3 and is_real_value(row.iloc[3]) else ""

        if not started:
            if code.lower() == "värde" and text.lower() == "beskrivningstext":
                started = True
            continue

        if not code or not text:
            continue

       
        mapping[normalize_text(text)] = code

    return mapping