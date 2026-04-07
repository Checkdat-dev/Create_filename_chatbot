import re
import pandas as pd

from step1_excelreader import load_excel, get_delomrade


VALID_TEKNIKOMRADEN = ["c", "a", "A"]

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

        if col1_norm in [
            "databasdokument",
            "databasdokument kopplade till enskild bsab-grupp",
            "textdokument",
            "textdokument kopplade till enskild bsab-grupp"
        ]:
            current_section = "document"
            continue

        if "ritning" in col1_norm:
            current_section = "drawing"
            continue

        if not col1 or not col2:
            continue

        if not is_valid_type_code(col2):
            continue

        key = normalize_text(col1)

        if current_section == "document":
            document_map[key] = col2

        elif current_section == "drawing":
            drawing_map[key] = col2

    return document_map, drawing_map



def get_model_types(data):
    df = data["Redovisningssätt (modeller)"]

    mapping = {}

    for _, row in df.iterrows():
        code = str(row.iloc[2]).strip() if len(row) > 2 and is_real_value(row.iloc[2]) else ""
        text = str(row.iloc[3]).strip() if len(row) > 3 and is_real_value(row.iloc[3]) else ""

        if not code or not text:
            continue

        mapping[normalize_text(text)] = code
        mapping[normalize_text(code)] = code

    return mapping



def strict_match(user_input, mapping):
    user = normalize_text(user_input)

    if user in mapping:
        return mapping[user]

    print("Invalid value. Must match exactly.")
    return None


def controlled_match(user_input, mapping):
    user = normalize_text(user_input)

    if user in mapping:
        return mapping[user]

    matches = [k for k in mapping if k.startswith(user)]

    if len(matches) == 1:
        print(f"Matched with: {matches[0]}")
        return mapping[matches[0]]

    elif len(matches) > 1:
        print("Multiple matches found. Be more specific:")
        print(matches[:5])
        return None

    print("Invalid value.")
    return None



# INPUT VALIDATION

def get_valid_entreprenad():
    while True:
        e = input("Bot: Entreprenadnummer: ").strip().upper()
        if e in ENTREPRENAD_LIST:
            return e
        print("Invalid entreprenadnummer")


def get_valid_teknikomrade():
    while True:
        t = input("Bot: Teknikområde (c / a / A): ").strip()
        if t in VALID_TEKNIKOMRADEN:
            return t
        print("Invalid teknikområde")


def get_valid_delomrade(delomrade_list):
    while True:
        d = input("Bot: Delområde: ").strip()
        if d in delomrade_list:
            return d
        print("Invalid delområde")


def get_valid_lopnummer():
    while True:
        l = input("Bot: Löpnummer (4 digits): ").strip()
        if l.isdigit() and len(l) == 4:
            return l
        print("Invalid löpnummer")



# CHATBOT

def run_chatbot(konstruktiv_map, dokument_map, ritning_map, modell_map, delomrade_list):
    print("\nChatbot started\n")

    while True:
        input("\nUser: ")

        typ = input("Bot: Typ av handling? (document/drawing/model): ").strip().lower()

        entreprenad = get_valid_entreprenad()
        teknik = get_valid_teknikomrade()
        delomrade = get_valid_delomrade(delomrade_list)
        lopnummer = get_valid_lopnummer()

        if typ == "document":
            user_input = input("Bot: Dokumenttyp: ")
            val = strict_match(user_input, dokument_map)

        elif typ == "drawing":
            user_input = input("Bot: Ritningstyp: ")
            val = controlled_match(user_input, ritning_map)

        elif typ == "model":
            user_input = input("Bot: Modelltyp: ")
            val = controlled_match(user_input, modell_map)

        else:
            print("Invalid type")
            continue

        if not val:
            continue

        filename = f"{entreprenad}-{teknik}-{val}-{delomrade}-{lopnummer}"

        print("\nGenerated filename:")
        print(filename)
        print("--------------------------")

# RUN

if __name__ == "__main__":
    data = load_excel("data/naming.xlsx")

    konstruktiv_map = get_konstruktiv_mapping(data)
    dokument_map, ritning_map = get_type_mappings(data)
    modell_map = get_model_types(data)
    delomrade_list = get_delomrade(data)

    run_chatbot(
        konstruktiv_map,
        dokument_map,
        ritning_map,
        modell_map,
        delomrade_list
    )