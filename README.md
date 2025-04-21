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
python umls_inconsistency_checker.py -i path/to/MRREL.RRF -t both
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

The actual UMLS `MRREL.RRF` file includes **many fields** beyond just concept IDs and relationships. Here's an example of a **realistic entry**:
```txt
C0000005|A13433185|SCUI|RB|C0036775|A7466261|SCUI||R86000559||MSHFRE|MSHFRE|||N||
```

This line contains information like:
- Source and target CUIs (e.g., `C0000005`, `C0036775`)
- Relationship type (e.g., `RB` for *broader-than*)
- Source vocabularies (`MSHFRE`, `MSH`)
- And other identifiers like AUIs, ATNs, RELA, etc.



