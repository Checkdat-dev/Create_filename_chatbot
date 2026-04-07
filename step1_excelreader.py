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

    values = []

    for _, row in df.iterrows():
        if len(row) > 2:
            val = row.iloc[2]

            if pd.notna(val):
                val = str(val).strip()

                if val.isdigit() and len(val) == 4:
                    values.append(val)

    return sorted(set(values))