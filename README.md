# 🧠 UMLS Inconsistency Checker

A Python-based tool to detect hierarchical inconsistencies in the **Unified Medical Language System (UMLS)** ontology structure using the `MRREL.RRF` file.

This tool identifies:
- 🔁 **Parent-Child Cycles** (e.g., A → B → C → A)
- 🔄 **Broader-Than Violations** (e.g., A is broader than B and B is broader than A)
- ♻️ **Self-loops** (e.g., A → A)
- 📊 **Duplicate Relationships**

---

## 📦 Features

- Parses UMLS `MRREL.RRF` relationship files
- Analyzes `CHD`, `PAR`, `RB`, and `RN` relationships
- Detects:
  - Cycles in parent-child hierarchy
  - Broader-than inconsistencies
  - Self-referential loops
  - Duplicate edges
- Generates clean CSV reports and summary statistics
- Logs all actions and errors for traceability

---

## 📊 Dataset

This tool works on the `MRREL.RRF` file found in UMLS releases. If you do not have access to the UMLS license, you can use a sample dataset available here:

📂 **UMLS Sample Dataset on Kaggle**  
🔗 [https://www.kaggle.com/datasets/klilajaafer/umls-2024aa](https://www.kaggle.com/datasets/klilajaafer/umls-2024aa)

> Note: The file `MRREL.RRF` contains relationships between concepts in the UMLS Metathesaurus and is necessary for this tool to function.

---

## 🚀 Usage

### ▶️ Basic Command

```bash
python UMLS_Inconsistency_Checker.py -i path/to/MRREL.RRF -t both
```
## 🔧 Arguments

| Argument         | Description                                                   |
|------------------|---------------------------------------------------------------|
| `--input` / `-i` | Path to the UMLS `MRREL.RRF` file                             |
| `--type` / `-t`  | Type of analysis: `parent-child`, `broader-than`, or `both`   |

---

## 📂 Output Files

Results will be saved in a `res/` folder with timestamped filenames:

| Filename                                      | Description                             |
|----------------------------------------------|-----------------------------------------|
| `parent_child_cycles_<timestamp>.csv`        | Detected parent-child cycles            |
| `broader_than_violations_<timestamp>.csv`    | Detected broader-than violations        |
| `self_loops_<timestamp>.csv`                 | Concepts that point to themselves       |
| `duplicates_<timestamp>.csv`                 | Duplicate relationships found           |
| `analysis_statistics_<timestamp>.csv`        | Summary of all detected stats           |

---

## 🧪 Sample MRREL Format

```txt
C0001|||CHD|C0002|
C0002|||CHD|C0003|
C0003|||CHD|C0001|     ← parent-child cycle

C0010|||RB|C0011|
C0011|||RB|C0012|
C0012|||RB|C0010|      ← broader-than cycle
