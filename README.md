# A/B Testing Analysis — Landing Page Conversion

End-to-end A/B test analysis evaluating whether a redesigned landing page (`new_page`) produces higher conversion rates than the original (`old_page`). The pipeline covers data cleaning, SQL-based aggregation, three statistical tests, visualizations, and a power analysis.

---

## Dataset

`ab_data.csv` — 294,478 rows with the following fields:

| Column | Description |
|---|---|
| `user_id` | Unique visitor identifier |
| `timestamp` | Time of visit |
| `group` | `control` or `treatment` |
| `landing_page` | `old_page` (control) or `new_page` (treatment) |
| `converted` | `1` = converted, `0` = did not convert |

---

## Project Structure

```
ab-testing-analysis/
├── data/
│   └── ab_data.csv
├── db/
│   └── abtest.db           # Auto-generated SQLite database
├── charts/
│   ├── conversion_rates.png
│   ├── distribution_plot.png
│   └── power_analysis.png
├── outputs/
│   └── ab_report.xlsx      # Test results summary
├── clean_data.py
├── load_to_db.py
├── run_tests.py
└── create_charts.py
```

---

## Pipeline

### 1. `clean_data.py`
- Loads the raw CSV
- Removes duplicate records (excluding timestamp)
- Deduplicates by `user_id`, keeping the first occurrence
- Validates group/page alignment via a crosstab

### 2. `load_to_db.py`
- Loads the cleaned dataframe into a local SQLite database (`db/abtest.db`)
- Creates/replaces the `ab_test` table on each run

### 3. `run_tests.py`
Runs three statistical tests against the database and exports results to Excel.

| Test | Purpose |
|---|---|
| **Chi-Square** | Tests independence between group and conversion outcome |
| **T-Test** (two-sided) | Compares mean conversion rates between groups |
| **Mann-Whitney U** | Non-parametric alternative; no normality assumption required |

All tests use α = 0.05. Results are saved to `outputs/ab_report.xlsx`.

### 4. `create_charts.py`
Generates three charts saved to `charts/`:

- **Conversion Rate Bar Chart** — side-by-side conversion rates (%) for control vs. treatment
- **Distribution Plot** — converted vs. not-converted counts for each group
- **Power Analysis** — statistical power as a function of sample size, with the 0.8 power threshold and the actual sample size marked

---

## Requirements

```
pandas
scipy
statsmodels
matplotlib
numpy
openpyxl
```

Install with:

```bash
pip install pandas scipy statsmodels matplotlib numpy openpyxl
```

---

## Usage

Run the full pipeline in order:

```bash
python clean_data.py
python load_to_db.py
python run_tests.py
python create_charts.py
```

Or trigger everything at once by running `run_tests.py` and `create_charts.py` directly — both scripts invoke the earlier steps automatically via `subprocess`.

---

## Output

- **`outputs/ab_report.xlsx`** — summary table with the test statistic, p-value, hypothesis decision, and plain-language conclusion for each of the three tests
- **`charts/`** — three publication-ready PNG charts

---

## Notes

- The dataset is sourced from [Kaggle: A/B Testing](https://www.kaggle.com/datasets/zhangluyuan/ab-testing)
- Mismatched rows (e.g. control group assigned to `new_page`) are handled during deduplication in `clean_data.py`
- The power analysis uses raw conversion rate difference as the effect size
