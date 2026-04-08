import streamlit as st

from step1_excelreader import load_excel, get_delomrade
from step2_chatbot import (
    get_konstruktiv_mapping,
    get_type_mappings,
    get_model_types,
    get_teknikomrade_mapping,
    ENTREPRENAD_LIST
)


@st.cache_data
def load_all_data():
    data = load_excel("data/naming.xlsx")

    konstruktiv_map = get_konstruktiv_mapping(data)
    dokument_map, ritning_map = get_type_mappings(data)
    modell_map = get_model_types(data)
    delomrade_list = get_delomrade(data)
    teknik_map = get_teknikomrade_mapping(data)

    return konstruktiv_map, dokument_map, ritning_map, modell_map, delomrade_list, teknik_map


def main():
    st.set_page_config(page_title="Filename Generator", layout="centered")

    st.title("Filename Generator")
    st.write("Generate correct filename based on project rules")

    (
        konstruktiv_map,
        dokument_map,
        ritning_map,
        modell_map,
        delomrade_list,
        teknik_map
    ) = load_all_data()

    typ = st.selectbox(
        "Typ av handling",
        ["Dokument", "Ritning", "Modell"]
    )

    entreprenad = st.selectbox(
        "Entreprenadnummer",
        ENTREPRENAD_LIST
    )

    teknik_display = list(teknik_map.keys())
    selected_teknik = st.selectbox("Teknikområde", teknik_display)
    teknik = teknik_map[selected_teknik]

    val = None

    if typ == "Dokument":
        reverse_doc_map = {v: k for k, v in dokument_map.items()}

        dokument_display = [
            f"{code} - {reverse_doc_map[code]}"
            for code in sorted(reverse_doc_map.keys())
        ]

        selected = st.selectbox("Dokumenttyp", dokument_display)

        if selected:
            val = selected.split(" - ")[0]

    elif typ == "Ritning":
        reverse_ritning_map = {v: k for k, v in ritning_map.items()}

        ritning_display = [
            f"{code} - {reverse_ritning_map[code]}"
            for code in sorted(reverse_ritning_map.keys())
        ]

        selected = st.selectbox("Ritningstyp", ritning_display)

        if selected:
            val = selected.split(" - ")[0]

    elif typ == "Modell":
        reverse_model_map = {v: k for k, v in modell_map.items()}

        model_display = [
            f"{code} - {reverse_model_map[code]}"
            for code in sorted(reverse_model_map.keys())
        ]

        selected = st.selectbox("Modelltyp", model_display)

        if selected:
            val = selected.split(" - ")[0]

    delomrade_display = list(delomrade_list.keys())

    selected_delomrade = st.selectbox(
        "Delområde",
        delomrade_display
    )

    delomrade = delomrade_list[selected_delomrade]

    lopnummer = st.text_input("Löpnummer (4 digits)")

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