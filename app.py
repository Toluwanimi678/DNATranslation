from flask import Flask, request, render_template_string

app = Flask(__name__)

# Genetic code (RNA codons → amino acids)
CODON_TABLE = {
    "UUU": ("Phe", "F"), "UUC": ("Phe", "F"),
    "UUA": ("Leu", "L"), "UUG": ("Leu", "L"),
    "CUU": ("Leu", "L"), "CUC": ("Leu", "L"),
    "CUA": ("Leu", "L"), "CUG": ("Leu", "L"),
    "AUU": ("Ile", "I"), "AUC": ("Ile", "I"),
    "AUA": ("Ile", "I"), "AUG": ("Met", "M"),
    "GUU": ("Val", "V"), "GUC": ("Val", "V"),
    "GUA": ("Val", "V"), "GUG": ("Val", "V"),

    "UCU": ("Ser", "S"), "UCC": ("Ser", "S"),
    "UCA": ("Ser", "S"), "UCG": ("Ser", "S"),
    "CCU": ("Pro", "P"), "CCC": ("Pro", "P"),
    "CCA": ("Pro", "P"), "CCG": ("Pro", "P"),
    "ACU": ("Thr", "T"), "ACC": ("Thr", "T"),
    "ACA": ("Thr", "T"), "ACG": ("Thr", "T"),
    "GCU": ("Ala", "A"), "GCC": ("Ala", "A"),
    "GCA": ("Ala", "A"), "GCG": ("Ala", "A"),

    "UAU": ("Tyr", "Y"), "UAC": ("Tyr", "Y"),
    "UAA": ("Stop", "*"), "UAG": ("Stop", "*"),
    "CAU": ("His", "H"), "CAC": ("His", "H"),
    "CAA": ("Gln", "Q"), "CAG": ("Gln", "Q"),
    "AAU": ("Asn", "N"), "AAC": ("Asn", "N"),
    "AAA": ("Lys", "K"), "AAG": ("Lys", "K"),
    "GAU": ("Asp", "D"), "GAC": ("Asp", "D"),
    "GAA": ("Glu", "E"), "GAG": ("Glu", "E"),

    "UGU": ("Cys", "C"), "UGC": ("Cys", "C"),
    "UGA": ("Stop", "*"), "UGG": ("Trp", "W"),
    "CGU": ("Arg", "R"), "CGC": ("Arg", "R"),
    "CGA": ("Arg", "R"), "CGG": ("Arg", "R"),
    "AGU": ("Ser", "S"), "AGC": ("Ser", "S"),
    "AGA": ("Arg", "R"), "AGG": ("Arg", "R"),
    "GGU": ("Gly", "G"), "GGC": ("Gly", "G"),
    "GGA": ("Gly", "G"), "GGG": ("Gly", "G")
}


def detect_type(seq):
    if "U" in seq and "T" not in seq:
        return "RNA"
    elif "T" in seq and "U" not in seq:
        return "DNA"
    else:
        return "Invalid"


def dna_to_mrna(dna):
    return dna.replace("T", "U")


def complement_rna(rna):
    comp = {"A": "U", "U": "A", "C": "G", "G": "C"}
    return "".join(comp.get(base, base) for base in rna)


def trna_from_mrna(mrna):
    comp = {"A": "U", "U": "A", "C": "G", "G": "C"}
    return "".join(comp.get(base, base) for base in mrna)


def translate(mrna):
    amino_acids_3 = []
    amino_acids_1 = []

    for i in range(0, len(mrna) - 2, 3):
        codon = mrna[i:i+3]

        if codon in CODON_TABLE:
            aa3, aa1 = CODON_TABLE[codon]

            if aa3 == "Stop":
                break

            amino_acids_3.append(aa3)
            amino_acids_1.append(aa1)

    return amino_acids_3, amino_acids_1


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Nucleotide Analyzer</title>

    <style>
        body{
            font-family: Arial;
            background:#f4f4f4;
            padding:40px;
        }

        .container{
            max-width:700px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:10px;
        }

        textarea{
            width:100%;
            padding:10px;
            font-size:16px;
        }

        button{
            margin-top:20px;
            padding:12px 20px;
            background:#2563eb;
            color:white;
            border:none;
            border-radius:8px;
            cursor:pointer;
        }

        .result{
            margin-top:25px;
            padding:20px;
            background:#eef2ff;
            border-radius:8px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🧬 Nucleotide Analyzer</h1>

    <form method="POST">

        <textarea
            name="sequence"
            rows="5"
            placeholder="Enter DNA or RNA sequence"
            required
        ></textarea>

        <button type="submit">
            Analyze Sequence
        </button>

    </form>

    {% if result %}
    <div class="result">

        <h2>Sequence Type: {{ result.type }}</h2>

        {% if result.type == "DNA" %}

            <p><strong>mRNA:</strong> {{ result.mrna }}</p>

            <p><strong>tRNA:</strong> {{ result.trna }}</p>

            <p><strong>3-Letter Amino Acids:</strong>
            {{ result.aa3 }}</p>

            <p><strong>Protein Sequence:</strong>
            {{ result.aa1 }}</p>

        {% elif result.type == "RNA" %}

            <p><strong>Complementary RNA:</strong>
            {{ result.complement }}</p>

        {% else %}

            <p>Invalid sequence entered.</p>

        {% endif %}

    </div>
    {% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        seq = request.form["sequence"].upper().strip()

        seq_type = detect_type(seq)

        result = {"type": seq_type}

        if seq_type == "DNA":

            mrna = dna_to_mrna(seq)
            trna = trna_from_mrna(mrna)

            aa3, aa1 = translate(mrna)

            result.update({
                "mrna": mrna,
                "trna": trna,
                "aa3": "-".join(aa3),
                "aa1": "".join(aa1)
            })

        elif seq_type == "RNA":

            result["complement"] = complement_rna(seq)

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(debug=True)