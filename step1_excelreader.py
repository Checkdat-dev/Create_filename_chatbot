import pandas as pd

def load_excel(file_path):
    data = pd.read_excel(file_path, sheet_name=None, header=None)
    print(f"Loaded {len(data)} sheets")
    return data


def convert_to_chunks(data):
    chunks = []

    for sheet_name, df in data.items():
        text = df.fillna("").astype(str).to_string(index=False)
        chunk = f"Sheet: {sheet_name}\n{text}"

        if sheet_name.lower() in ["inledning", "syfte"]:
            chunks.insert(0, chunk)
        else:
            chunks.append(chunk)

    return chunks


def get_delomrade(data):
    df = data["Delområde byggskede"]

    mapping = {}

    for _, row in df.iterrows():
        if len(row) > 3:
            code = row.iloc[2]
            text = row.iloc[3]

            if pd.notna(code) and pd.notna(text):
                code = str(code).strip()
                text = str(text).strip()

                if code.isdigit() and len(code) == 4:
                    mapping[f"{code} - {text}"] = code

    return mapping