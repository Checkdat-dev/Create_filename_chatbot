import streamlit as st

from step1_excelreader import load_excel, get_delomrade
from step2_chatbot import (
    get_konstruktiv_mapping,
    get_type_mappings,
    get_model_types,
    get_teknikomrade_mapping,
    ENTREPRENAD_LIST
)

from step4_pdfchatbot import (
    generate_ritning,
    generate_ritningsmodell,
    generate_textdokument
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


def home_page():
    st.title("Filename Generator")
    st.write("Choose company source to continue")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Excel - 1st Company", use_container_width=True):
            st.session_state.page = "excel"
            st.rerun()

    with col2:
        if st.button("PDF - 2nd Company", use_container_width=True):
            st.session_state.page = "pdf"
            st.rerun()


def excel_page():
    if st.button("← Back", key="excel_back"):
        st.session_state.page = "home"
        st.rerun()

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
        ["Dokument", "Ritning", "Modell"],
        key="excel_typ"
    )

    entreprenad = st.selectbox(
        "Entreprenadnummer",
        ENTREPRENAD_LIST,
        key="excel_entreprenad"
    )

    teknik_display = list(teknik_map.keys())
    selected_teknik = st.selectbox("Teknikområde", teknik_display, key="excel_teknik")
    teknik = teknik_map[selected_teknik]

    val = None

    if typ == "Dokument":
        reverse_doc_map = {v: k for k, v in dokument_map.items()}

        dokument_display = [
            f"{code} - {reverse_doc_map[code]}"
            for code in sorted(reverse_doc_map.keys())
        ]

        selected = st.selectbox("Dokumenttyp", dokument_display, key="excel_dokumenttyp")

        if selected:
            val = selected.split(" - ")[0]

    elif typ == "Ritning":
        reverse_ritning_map = {v: k for k, v in ritning_map.items()}

        ritning_display = [
            f"{code} - {reverse_ritning_map[code]}"
            for code in sorted(reverse_ritning_map.keys())
        ]

        selected = st.selectbox("Ritningstyp", ritning_display, key="excel_ritningstyp")

        if selected:
            val = selected.split(" - ")[0]

    elif typ == "Modell":
        reverse_model_map = {v: k for k, v in modell_map.items()}

        model_display = [
            f"{code} - {reverse_model_map[code]}"
            for code in sorted(reverse_model_map.keys())
        ]

        selected = st.selectbox("Modelltyp", model_display, key="excel_modelltyp")

        if selected:
            val = selected.split(" - ")[0]

    delomrade_display = list(delomrade_list.keys())

    selected_delomrade = st.selectbox(
        "Delområde",
        delomrade_display,
        key="excel_delomrade"
    )

    delomrade = delomrade_list[selected_delomrade]

    lopnummer = st.text_input("Löpnummer (4 digits)", key="excel_lopnummer")

    if st.button("Generate filename", key="excel_generate"):
        if not lopnummer.isdigit() or len(lopnummer) != 4:
            st.error("Löpnummer must be exactly 4 digits")
            return

        if not val:
            st.error("Please select valid type")
            return

        filename = f"{entreprenad}-{teknik}-{val}-{delomrade}-{lopnummer}"

        st.success("Generated filename")
        st.code(filename)


def pdf_page():
    if st.button("← Back", key="pdf_back"):
        st.session_state.page = "home"
        st.rerun()

    st.title("PDF Filename Generator")
    st.write("Generate correct filename based on PDF rules")

    DELOMRADE = [str(i) for i in range(10)]

    # RANGE BASED (FROM PDF)
    ANLAGGNINGSDEL_RANGES = {
        (0, 0): "Gemensamt",
        (1, 9): "Väg/tunnel",
        (10, 19): "Ramper",
        (20, 29): "Tvärtunnlar",
        (30, 39): "Anslutningsvägar",
        (40, 49): "Broar",
        (50, 59): "Utrymningsvägar",
        (60, 69): "Driftutrymmen el",
        (70, 79): "Ventilation",
        (80, 89): "VA",
        (90, 99): "Övrigt"
    }

    ANLAGGNINGSDEL_MAP = {}
    for (start, end), text in ANLAGGNINGSDEL_RANGES.items():
        for i in range(start, end + 1):
            code = f"{i:02d}"
            ANLAGGNINGSDEL_MAP[code] = text

    TEKNIKOMRADE = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    TEKNISKT_SYSTEM = {
        "00": {"name": "VÄG OCH TRAFIK", "sub": {"01": "Trafikflöden","02": "Planer","03": "Profiler","04": "Sektioner","05": "Utformning","08": "Trafikföring","09": "Tvärsektion"}},
        "10": {"name": "MARK", "sub": {"11": "Geoteknik","12": "Tolkad geoteknik","13": "Grundvatten","14": "Tunnlar","15": "Underbyggnad","16": "Skydd byggnad","17": "Skydd natur","18": "Uppfyllning","19": "Plantering"}},
        "20": {"name": "ANLÄGGNINGSBYGGDELAR", "sub": {"21": "Grundkonstruktion","22": "Stödkonstruktion","23": "Bärverk","24": "Tunnelförstärkning","25": "Vägöverbyggnad","26": "VA-magasin","27": "Betongkylning","28": "Bärverk horisontellt","29": "Bärverk övrigt","2A": "Frostsäkring"}},
        "30": {"name": "HUSBYGGDELAR", "sub": {"32": "Husunderbyggnad","33": "Husstomme","34": "Yttertak","35": "Yttervägg","36": "Rum","37": "Invändig","38": "Brand","39": "Övrigt"}},
        "40": {"name": "VÄGANORDNINGAR", "sub": {"41": "Trafikanordning","42": "Motorvägssystem","43": "Information","44": "Tunnelinredning","45": "Innertak","46": "Barriär","47": "Ytväg","48": "Signaler"}},
        "50": {"name": "RÖR- OCH VENTILATIONSSYSTEM", "sub": {"51": "VA","53": "Sprinkler","54": "Gas","55": "Kyla","56": "Värme","57": "Ventilation","58": "Tunnelventilation"}},
        "60": {"name": "ELANLÄGGNINGAR", "sub": {"62": "Kraft","63": "Belysning","64": "Vägbelysning","65": "Elvärme","66": "Spänning","67": "Kabel"}},
        "70": {"name": "TRANSPORTANLÄGGNINGAR", "sub": {"71": "Hiss","73": "Persontransport","75": "Varutransport","77": "Portar"}},
        "80": {"name": "STYRSYSTEM", "sub": {"81": "Styr","82": "Styr väg","84": "Övervakning","85": "Ledning","86": "Kommunikation","87": "Tele","88": "Avgift"}},
        "90": {"name": "SAMMANSATT", "sub": {"91": "Sammansatt bygg","92": "Sammansatt inst","93": "Gränser","94": "Befintligt","95": "Ritningsinfo","96": "Provisorier","97": "Kartor","98": "Övrigt"}},
    }

    # OMBINED SYSTEM DROPDOWN
    system_display = []
    system_lookup = {}

    for main_code, main_data in TEKNISKT_SYSTEM.items():
        for sub_code, sub_name in main_data["sub"].items():
            label = f"{main_code} - {main_data['name']} → {sub_code} - {sub_name}"
            system_display.append(label)
            system_lookup[label] = sub_code

    DOKUMENTBETECKNING_DISPLAY = {k: v for k, v in {
        "A1": "3D Trafik","A2": "3D Plan","A3": "3D Profil","A4": "3D Sektion","A5": "3D Utformning","A8": "3D Trafikföring","A9": "3D Tvärsektion",
        "B1": "3D Geoteknik","B2": "3D Tolkning","B3": "3D Grundvatten","B4": "3D Tunnel","B5": "3D Underbyggnad","B6": "3D Skydd bygg","B7": "3D Skydd natur","B8": "3D Uppfyllning","B9": "3D Plantering",
        "C1": "3D Grund","C2": "3D Stöd","C3": "3D Bärverk","C4": "3D Tunnelstöd","C5": "3D Väg","C6": "3D VA","C7": "3D Betong","C8": "3D Horisontell","C9": "3D Övrigt","CA": "3D Frost",
        "D2": "3D Husgrund","D3": "3D Stomme","D4": "3D Tak","D5": "3D Vägg","D6": "3D Rum","D7": "3D Invändigt","D8": "3D Brand","D9": "3D Övrigt"
    }.items()}

    typ = st.selectbox("Typ av handling", ["Ritning", "Ritningsmodell", "Textdokument"], key="pdf_typ")

    # ================= RITNING =================
    if typ == "Ritning":
        delomrade = st.selectbox("Delområde", DELOMRADE, key="pdf_r_del")

        anl_display = [f"{k} - {v}" for k, v in ANLAGGNINGSDEL_MAP.items()]
        selected_anl = st.selectbox("Anläggningsdel", anl_display, key="pdf_r_anl")
        anlaggningsdel = selected_anl.split(" - ")[0]

        teknik = st.selectbox("Teknikområde", TEKNIKOMRADE, key="pdf_r_teknik")

        selected_system = st.selectbox("Tekniskt system", system_display, key="pdf_r_sys")
        system = system_lookup[selected_system]

        lopnummer = st.text_input("Löpnummer (2 characters)", key="pdf_r_lop")

        if st.button("Generate PDF filename", key="pdf_r_btn"):
            if len(lopnummer) != 2:
                st.error("Löpnummer must be exactly 2 characters")
                return

            filename = generate_ritning(delomrade, anlaggningsdel, teknik, system, lopnummer)
            st.success("Generated filename")
            st.code(filename)

    # ================= RITNINGSMODELL =================
    elif typ == "Ritningsmodell":
        teknik = st.selectbox("Teknikområde", TEKNIKOMRADE, key="pdf_m_teknik")
        delomrade = st.selectbox("Delområde", DELOMRADE, key="pdf_m_del")

        anl_display = [f"{k} - {v}" for k, v in ANLAGGNINGSDEL_MAP.items()]
        selected_anl = st.selectbox("Anläggningsdel", anl_display, key="pdf_m_anl")
        anlaggningsdel = selected_anl.split(" - ")[0]

        selected_system = st.selectbox("Tekniskt system", system_display, key="pdf_m_sys")
        system = system_lookup[selected_system]

        lopnummer = st.text_input("Löpnummer (2 characters)", key="pdf_m_lop")

        if st.button("Generate PDF filename", key="pdf_m_btn"):
            if len(lopnummer) != 2:
                st.error("Löpnummer must be exactly 2 characters")
                return

            filename = generate_ritningsmodell(teknik, delomrade, anlaggningsdel, system, lopnummer)
            st.success("Generated filename")
            st.code(filename)

    # ================= TEXT =================
    elif typ == "Textdokument":
        delomrade = st.selectbox("Delområde", DELOMRADE, key="pdf_t_del")
        teknik = st.selectbox("Teknikområde", TEKNIKOMRADE, key="pdf_t_teknik")

        doc_display = [f"{k} - {v}" for k, v in DOKUMENTBETECKNING_DISPLAY.items()]
        selected_doc = st.selectbox("Dokumentbeteckning", doc_display, key="pdf_t_doc")
        dokumentbeteckning = selected_doc.split(" - ")[0]

        lopnummer = st.text_input("Löpnummer (4 characters)", key="pdf_t_lop")

        if st.button("Generate PDF filename", key="pdf_t_btn"):
            if len(lopnummer) != 4:
                st.error("Löpnummer must be exactly 4 characters")
                return

            filename = generate_textdokument(delomrade, teknik, dokumentbeteckning, lopnummer)
            st.success("Generated filename")
            st.code(filename)
def main():
    st.set_page_config(page_title="Filename Generator", layout="centered")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "excel":
        excel_page()
    elif st.session_state.page == "pdf":
        pdf_page()


if __name__ == "__main__":
    main()