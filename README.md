# 🛒 Supermarket Sales Analytics

A complete end-to-end data analytics project for a multi-city supermarket chain — from raw CSV to an interactive Streamlit dashboard and a Jupyter Notebook walkthrough.

---

## 📁 Project Structure

```
supermarket_analysis/
│
├── data/
│   └── supermarket_data.csv          # Source dataset (500 rows × 13 columns)
│
├── Supermarket_Sales_Analysis.ipynb  # Jupyter Notebook — full step-by-step analysis
├── app.py                            # Streamlit dashboard (Steps 5 & 6)
├── analytics.py                      # Aggregation functions (Step 4)
├── data_loader.py                    # Load, validate & clean pipeline (Steps 1–3)
│
├── Supermarket_Sales_Analytics.pptx  # PowerPoint presentation (13 slides)
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 🗂️ Dataset

| Field | Description |
|-------|-------------|
| **Invoice ID** | Unique transaction identifier |
| **Date** | Transaction date |
| **Branch** | Store branch code (A / B / C / D) |
| **City** | City name (Mumbai · Delhi · Bengaluru · Jaipur) |
| **Customer Type** | Member or Normal |
| **Gender** | Male / Female |
| **Product** | Product name (20 unique SKUs) |
| **Category** | Product category (8 lines) |
| **Quantity** | Units purchased |
| **Unit Price** | Price per unit (₹) |
| **Payment** | Payment method (UPI · Card · Cash · Net Banking) |
| **Rating** | Customer satisfaction score (1–5) |
| **Sales** | Transaction total (₹) |

**Period:** January 1, 2026 → July 1, 2026 · **500 transactions** · **4 cities**

---

## 🔢 Analysis Pipeline

| Step | Task | File |
|------|------|------|
| **1** | Collect and load the CSV dataset | `data_loader.py` |
| **2** | Check for missing/incorrect values | `data_loader.py` |
| **3** | Calculate `Sales = Quantity × Unit Price` | `data_loader.py` |
| **4** | Group & summarise (totals, counts, averages) | `analytics.py` |
| **5** | Create charts to compare results | `app.py` / Notebook |
| **6** | Data-driven business recommendations | `app.py` / Notebook |

---

## 🚀 Quick Start

### 1. Clone / open the project

```bash
cd supermarket_analysis
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4a. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

Opens automatically at **http://localhost:8501**

### 4b. Open the Jupyter Notebook

```bash
jupyter notebook Supermarket_Sales_Analysis.ipynb
```

or in VS Code: open the `.ipynb` file and select the Python kernel.

---

## 📊 Dashboard Tabs

| Tab | Contents |
|-----|----------|
| 📊 **Overview** | 8 KPI cards · Revenue by category (donut) · Payment bar chart |
| 📦 **Categories** | Revenue, avg order, avg rating charts + sortable table |
| 🏪 **Branches** | City revenue, scatter bubble, category × city heatmap |
| 👥 **Customers** | Member vs Normal, gender split, rating distribution |
| 📅 **Time Trends** | Monthly dual-axis trend, day-of-week, stacked area |
| 🏅 **Products** | Top-N slider, units sold, rating scatter |
| 🔍 **Data Quality** | Missing values, duplicates, Sales verification, dataset preview |
| 💡 **Insights** | 7 actionable business recommendation cards |

---

## 📓 Notebook Sections

| Section | Description |
|---------|-------------|
| **Step 1** | Load CSV, inspect shape, dtypes, and summary statistics |
| **Step 2** | Missing values, duplicates, negative fields, sales mismatch check |
| **Step 3** | Recalculate `Sales = Qty × Unit Price`, add derived time columns |
| **Step 4** | 10 aggregation tables — KPIs, category, branch, customer, payment, monthly, top products, rating distribution, day-of-week, heatmap |
| **Step 5** | 11 charts — bar, pie, donut, heatmap, dual-axis line, scatter, correlation matrix |
| **Step 6** | 7 business insights with data-backed reasoning and action items |

---

## 📈 Key Findings

| Finding | Value |
|---------|-------|
| **Total Revenue** | ₹2,44,411 |
| **Best Category** | Beverages (23% of revenue) |
| **Top Branch** | Mumbai — Branch C (₹72,469) |
| **Peak Month** | April 2026 (₹52,570 · highest avg order ₹584) |
| **Top Product** | Cheese (₹27,906) |
| **Preferred Payment** | UPI (27.8% · avg order ₹534.73) |
| **Digital Payments** | 77.9% of total revenue |
| **Avg Rating** | 3.99 / 5.0 |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| **Python** | 3.13 | Core language |
| **Pandas** | ≥ 2.0 | Data loading, cleaning, aggregation |
| **Matplotlib** | ≥ 3.7 | Static charts (Notebook) |
| **Seaborn** | ≥ 0.12 | Statistical visualisations (Notebook) |
| **Plotly** | ≥ 5.20 | Interactive charts (Dashboard) |
| **Streamlit** | ≥ 1.35 | Web dashboard frontend |

---

## 📂 Output Files

| File | Description |
|------|-------------|
| `Supermarket_Sales_Analysis.ipynb` | Full analysis notebook with code + outputs |
| `Supermarket_Sales_Analytics.pptx` | 13-slide presentation |
| `app.py` | Streamlit interactive dashboard |

---

*Built with Python · Pandas · Matplotlib · Seaborn · Plotly · Streamlit*
