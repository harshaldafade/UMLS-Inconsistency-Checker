# 🧠 UMLS Inconsistency Checker

A Python-based tool for detecting logical inconsistencies in the **UMLS (Unified Medical Language System)** ontology structure. Specifically, it identifies:

- 🔁 **Parent-Child Loops** (e.g., Concept A → B → A)
- 🔄 **Broader-Than Cycles** (e.g., A is broader than B, and B is broader than A)
- ♻️ **Self-loops** (e.g., A → A)
- 📊 **Duplicate relationships**

---

## 📦 Features

- Parses `MRREL.RRF` files used in UMLS
- Analyzes `CHD`, `PAR`, `RB`, `RN` relationships
- Detects graph cycles and logical conflicts
- Outputs structured CSV reports with detailed issues
- Generates runtime stats and logs for debugging

---

## 🚀 Usage

### ✅ Command Line Arguments

| Argument | Description |
|----------|-------------|
| `--input` / `-i` | Path to the `MRREL.RRF` file |
| `--type` / `-t`  | Type of analysis: `parent-child`, `broader-than`, or `both` |

### 🧪 Example

```bash
python UMLS_Inconsistency_Checker.py -i Dataset/MRREL.RRF -t both
