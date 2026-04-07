import streamlit as st

from step1_excelreader import load_excel, get_delomrade
from step2_chatbot import (
    get_konstruktiv_mapping,
    get_type_mappings,
    get_model_types
)

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


@st.cache_data
def load_all_data():
    data = load_excel("data/naming.xlsx")

    konstruktiv_map = get_konstruktiv_mapping(data)
    dokument_map, ritning_map = get_type_mappings(data)
    modell_map = get_model_types(data)
    delomrade_list = get_delomrade(data)

    return konstruktiv_map, dokument_map, ritning_map, modell_map, delomrade_list


def main():
    st.set_page_config(page_title="Filename Generator", layout="centered")

    st.title("Filename Generator")
    st.write("Generate correct filename based on project rules")

    (
        konstruktiv_map,
        dokument_map,
        ritning_map,
        modell_map,
        delomrade_list
    ) = load_all_data()

    typ = st.selectbox(
        "Typ av handling",
        ["document", "drawing", "model"]
    )

    entreprenad = st.selectbox(
        "Entreprenadnummer",
        ENTREPRENAD_LIST
    )

    teknik = st.selectbox(
        "Teknikområde",
        VALID_TEKNIKOMRADEN
    )

    delomrade = st.selectbox(
        "Delområde",
        delomrade_list
    )

    lopnummer = st.text_input("Löpnummer (4 digits)")

    val = None

    if typ == "document":
        dokument_keys = sorted(dokument_map.keys())

        selected = st.selectbox(
            "Dokumenttyp",
            dokument_keys
        )

        if selected:
            val = dokument_map[selected]

    elif typ == "drawing":
        ritning_keys = sorted(ritning_map.keys())

        selected = st.selectbox(
            "Ritningstyp",
            ritning_keys
        )

        if selected:
            val = ritning_map[selected]

    elif typ == "model":
        model_keys = sorted(set(modell_map.keys()))

        selected = st.selectbox(
            "Modelltyp",
            model_keys
        )

        if selected:
            val = modell_map[selected]

    if st.button("Generate filename"):
        if not lopnummer.isdigit() or len(lopnummer) != 4:
            st.error("Löpnummer must be exactly 4 digits")
            return

        if not val:
            st.error("Please select valid type")
            return

        filename = f"{entreprenad}-{teknik}-{val}-{delomrade}-{lopnummer}"

        st.success("Generated filename")
        st.code(filename)


if __name__ == "__main__":
    main()