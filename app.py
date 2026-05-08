import sys

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


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <nucleotide_sequence>")
        return

    seq = sys.argv[1].upper()
    seq_type = detect_type(seq)

    if seq_type == "Invalid":
        print("Invalid sequence. Use only A, T, C, G or A, U, C, G.")
        return

    print(f"Sequence Type: {seq_type}")

    if seq_type == "DNA":
        mrna = dna_to_mrna(seq)
        trna = trna_from_mrna(mrna)
        aa3, aa1 = translate(mrna)

        print(f"mRNA: {mrna}")
        print(f"tRNA: {trna}")
        print(f"Amino Acid (3-letter): {'-'.join(aa3)}")
        print(f"Protein (1-letter): {''.join(aa1)}")

    elif seq_type == "RNA":
        comp = complement_rna(seq)
        print(f"Complementary RNA: {comp}")


if __name__ == "__main__":
    main()