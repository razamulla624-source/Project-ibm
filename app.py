"""
app.py
------
Streamlit frontend for Supermarket Sales Analytics.
Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import get_clean_dataframe
from analytics import (
    overall_kpis,
    sales_by_category,
    sales_by_branch,
    sales_by_customer_type,
    sales_by_gender,
    sales_by_payment,
    monthly_sales_trend,
    top_products,
    rating_distribution,
    category_branch_heatmap,
    sales_by_day_of_week,
    generate_insights,
)

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Main background */
        .main { background-color: #f8f9fb; }

        /* KPI card */
        .kpi-card {
            background: #ffffff;
            border: 1px solid #e0e4ea;
            border-radius: 10px;
            padding: 18px 20px;
            text-align: center;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }
        .kpi-label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #1e3a5f;
        }
        .kpi-sub {
            font-size: 12px;
            color: #9ca3af;
            margin-top: 4px;
        }

        /* Section header */
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #1e3a5f;
            margin-top: 24px;
            margin-bottom: 4px;
            border-left: 4px solid #3b82f6;
            padding-left: 10px;
        }
        .section-sub {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 16px;
            padding-left: 14px;
        }

        /* Insight card */
        .insight-card {
            background: #ffffff;
            border: 1px solid #e0e4ea;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .insight-title {
            font-size: 15px;
            font-weight: 700;
            color: #1e3a5f;
            margin-bottom: 6px;
        }
        .insight-action {
            margin-top: 8px;
            font-size: 13px;
            color: #2563eb;
            font-weight: 600;
        }

        /* Quality row */
        .quality-ok   { color: #16a34a; font-weight: 600; }
        .quality-warn { color: #d97706; font-weight: 600; }
        .quality-bad  { color: #dc2626; font-weight: 600; }

        /* Sidebar */
        section[data-testid="stSidebar"] { background: #1e3a5f; }
        section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMultiSelect label { color: #cbd5e1 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Load data (cached)
# ──────────────────────────────────────────────
@st.cache_data
def load():
    return get_clean_dataframe()


df_full, quality_report = load()


# ──────────────────────────────────────────────
# Sidebar – Filters
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Supermarket Analytics")
    st.markdown("---")
    st.markdown("### 🔍 Filters")

    all_cities = sorted(df_full["City"].unique().tolist())
    sel_cities = st.multiselect("City / Branch", all_cities, default=all_cities)

    all_cats = sorted(df_full["Category"].unique().tolist())
    sel_cats = st.multiselect("Category", all_cats, default=all_cats)

    all_cust = sorted(df_full["Customer Type"].unique().tolist())
    sel_cust = st.multiselect("Customer Type", all_cust, default=all_cust)

    all_pay = sorted(df_full["Payment"].unique().tolist())
    sel_pay = st.multiselect("Payment Method", all_pay, default=all_pay)

    date_min = df_full["Date"].min().date()
    date_max = df_full["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    st.markdown("---")
    st.caption(f"📅 Data: {date_min} → {date_max}")
    st.caption(f"📊 Total rows: {len(df_full):,}")


# Apply filters
start_date, end_date = (date_range[0], date_range[1]) if len(date_range) == 2 else (date_min, date_max)
df = df_full[
    df_full["City"].isin(sel_cities)
    & df_full["Category"].isin(sel_cats)
    & df_full["Customer Type"].isin(sel_cust)
    & df_full["Payment"].isin(sel_pay)
    & (df_full["Date"].dt.date >= start_date)
    & (df_full["Date"].dt.date <= end_date)
].copy()

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

kpis = overall_kpis(df)


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#1e3a5f;font-size:32px;margin-bottom:0'>🛒 Supermarket Sales Analytics</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='color:#6b7280;font-size:14px;margin-top:2px'>Analysis period: "
    f"<b>{kpis['date_range_start']}</b> to <b>{kpis['date_range_end']}</b> "
    f"— Showing <b>{len(df):,}</b> transactions</p>",
    unsafe_allow_html=True,
)
st.markdown("---")


# ──────────────────────────────────────────────
# Tab Layout
# ──────────────────────────────────────────────
tabs = st.tabs([
    "📊 Overview",
    "📦 Categories",
    "🏪 Branches",
    "👥 Customers",
    "📅 Time Trends",
    "🏅 Products",
    "🔍 Data Quality",
    "💡 Insights",
])


# ════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Aggregated across all filtered transactions</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Total Revenue</div>'
            f'<div class="kpi-value">₹{kpis["total_revenue"]:,.0f}</div>'
            f'<div class="kpi-sub">Gross Sales</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Transactions</div>'
            f'<div class="kpi-value">{kpis["total_transactions"]:,}</div>'
            f'<div class="kpi-sub">Invoices processed</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Avg Order Value</div>'
            f'<div class="kpi-value">₹{kpis["avg_order_value"]:,.2f}</div>'
            f'<div class="kpi-sub">Per invoice</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Avg Rating</div>'
            f'<div class="kpi-value">{kpis["avg_rating"]} ⭐</div>'
            f'<div class="kpi-sub">Customer satisfaction</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Units Sold</div>'
            f'<div class="kpi-value">{kpis["total_units_sold"]:,}</div>'
            f'<div class="kpi-sub">Total quantity</div></div>',
            unsafe_allow_html=True,
        )
    with c6:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Unique Products</div>'
            f'<div class="kpi-value">{kpis["unique_products"]}</div>'
            f'<div class="kpi-sub">SKUs active</div></div>',
            unsafe_allow_html=True,
        )
    with c7:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Cities Covered</div>'
            f'<div class="kpi-value">{df["City"].nunique()}</div>'
            f'<div class="kpi-sub">Active locations</div></div>',
            unsafe_allow_html=True,
        )
    with c8:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Categories</div>'
            f'<div class="kpi-value">{df["Category"].nunique()}</div>'
            f'<div class="kpi-sub">Product lines</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
        cat_df = sales_by_category(df)
        fig = px.pie(
            cat_df, values="Total_Sales", names="Category",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4,
        )
        fig.update_traces(textinfo="percent+label", textfont_size=12)
        fig.update_layout(showlegend=True, margin=dict(t=10, b=10, l=10, r=10), height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Payment Method Breakdown</div>', unsafe_allow_html=True)
        pay_df = sales_by_payment(df)
        fig2 = px.bar(
            pay_df, x="Payment", y="Total_Sales",
            text="Sales_Share_%",
            color="Payment",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"Total_Sales": "Revenue (₹)", "Payment": "Method"},
        )
        fig2.update_traces(texttemplate="%{text}%", textposition="outside")
        fig2.update_layout(showlegend=False, margin=dict(t=10, b=10), height=350, yaxis_title="Revenue (₹)")
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════
# TAB 2 — CATEGORIES
# ════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title">Sales by Product Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ranked by total revenue</div>', unsafe_allow_html=True)

    cat_df = sales_by_category(df)

    fig = px.bar(
        cat_df.sort_values("Total_Sales"),
        x="Total_Sales", y="Category",
        orientation="h",
        color="Total_Sales",
        color_continuous_scale="Blues",
        text="Total_Sales",
        labels={"Total_Sales": "Revenue (₹)", "Category": "Category"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=10, b=10), height=400, xaxis_title="Revenue (₹)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Avg Order Value by Category</div>', unsafe_allow_html=True)
        fig2 = px.bar(
            cat_df.sort_values("Avg_Order", ascending=False),
            x="Category", y="Avg_Order",
            color="Avg_Order",
            color_continuous_scale="Teal",
            text="Avg_Order",
            labels={"Avg_Order": "Avg Order (₹)"},
        )
        fig2.update_traces(texttemplate="₹%{text:,.2f}", textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, height=350, xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Avg Rating by Category</div>', unsafe_allow_html=True)
        fig3 = px.bar(
            cat_df.sort_values("Avg_Rating", ascending=False),
            x="Category", y="Avg_Rating",
            color="Avg_Rating",
            color_continuous_scale="RdYlGn",
            text="Avg_Rating",
            range_y=[0, 5.5],
            labels={"Avg_Rating": "Avg Rating"},
        )
        fig3.update_traces(texttemplate="%{text:.2f} ⭐", textposition="outside")
        fig3.update_layout(coloraxis_showscale=False, height=350, xaxis_tickangle=-30)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Category Summary Table</div>', unsafe_allow_html=True)
    display_cat = cat_df.rename(columns={
        "Category": "Category", "Total_Sales": "Total Revenue (₹)",
        "Transactions": "Transactions", "Avg_Order": "Avg Order (₹)",
        "Avg_Rating": "Avg Rating", "Units_Sold": "Units Sold",
        "Sales_Share_%": "Revenue Share (%)",
    })
    st.dataframe(display_cat.style.format({
        "Total Revenue (₹)": "₹{:,.2f}",
        "Avg Order (₹)": "₹{:,.2f}",
        "Avg Rating": "{:.2f}",
        "Revenue Share (%)": "{:.2f}%",
    }), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════
# TAB 3 — BRANCHES
# ════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">Branch & City Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Revenue, transactions, and satisfaction by location</div>', unsafe_allow_html=True)

    branch_df = sales_by_branch(df)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            branch_df, x="City", y="Total_Sales",
            color="Branch",
            text="Total_Sales",
            barmode="group",
            labels={"Total_Sales": "Revenue (₹)", "City": "City"},
            title="Total Revenue by City",
        )
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(height=380, xaxis_tickangle=-15)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            branch_df, x="Transactions", y="Avg_Order",
            size="Total_Sales", color="City",
            hover_name="City",
            text="Branch",
            title="Avg Order vs Transactions (bubble = revenue)",
            labels={"Transactions": "No. of Transactions", "Avg_Order": "Avg Order (₹)"},
        )
        fig2.update_traces(textposition="top center")
        fig2.update_layout(height=380)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Category vs City Heatmap</div>', unsafe_allow_html=True)
    heatmap_df = category_branch_heatmap(df)
    cities = [c for c in heatmap_df.columns if c != "Category"]
    fig3 = go.Figure(data=go.Heatmap(
        z=heatmap_df[cities].values,
        x=cities,
        y=heatmap_df["Category"].tolist(),
        colorscale="Blues",
        text=[[f"₹{v:,.0f}" for v in row] for row in heatmap_df[cities].values],
        texttemplate="%{text}",
        showscale=True,
    ))
    fig3.update_layout(
        height=400,
        xaxis_title="City", yaxis_title="Category",
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Branch Summary Table</div>', unsafe_allow_html=True)
    st.dataframe(branch_df.rename(columns={
        "Branch": "Branch", "City": "City",
        "Total_Sales": "Total Revenue (₹)", "Transactions": "Transactions",
        "Avg_Order": "Avg Order (₹)", "Avg_Rating": "Avg Rating",
    }).style.format({
        "Total Revenue (₹)": "₹{:,.2f}",
        "Avg Order (₹)": "₹{:,.2f}",
        "Avg Rating": "{:.2f}",
    }), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════
# TAB 4 — CUSTOMERS
# ════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">Customer Segmentation</div>', unsafe_allow_html=True)

    cust_df = sales_by_customer_type(df)
    gender_df = sales_by_gender(df)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Member vs Normal — Revenue Share**")
        fig = px.pie(
            cust_df, values="Total_Sales", names="Customer Type",
            color_discrete_sequence=["#3b82f6", "#f59e0b"],
            hole=0.45,
        )
        fig.update_traces(textinfo="percent+label+value", textfont_size=12)
        fig.update_layout(height=320, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Gender — Revenue Share**")
        fig2 = px.pie(
            gender_df, values="Total_Sales", names="Gender",
            color_discrete_sequence=["#8b5cf6", "#ec4899"],
            hole=0.45,
        )
        fig2.update_traces(textinfo="percent+label+value", textfont_size=12)
        fig2.update_layout(height=320, margin=dict(t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Avg Order Value Comparison</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.bar(
            cust_df, x="Customer Type", y="Avg_Order",
            color="Customer Type",
            text="Avg_Order",
            color_discrete_sequence=["#3b82f6", "#f59e0b"],
            labels={"Avg_Order": "Avg Order (₹)"},
        )
        fig3.update_traces(texttemplate="₹%{text:,.2f}", textposition="outside")
        fig3.update_layout(showlegend=False, height=300, yaxis_title="Avg Order (₹)")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.bar(
            gender_df, x="Gender", y="Avg_Order",
            color="Gender",
            text="Avg_Order",
            color_discrete_sequence=["#8b5cf6", "#ec4899"],
            labels={"Avg_Order": "Avg Order (₹)"},
        )
        fig4.update_traces(texttemplate="₹%{text:,.2f}", textposition="outside")
        fig4.update_layout(showlegend=False, height=300, yaxis_title="Avg Order (₹)")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-title">Customer × Category Spend</div>', unsafe_allow_html=True)
    cust_cat = (
        df.groupby(["Customer Type", "Category"])["Sales"]
        .sum()
        .round(2)
        .reset_index()
    )
    fig5 = px.bar(
        cust_cat, x="Category", y="Sales",
        color="Customer Type",
        barmode="group",
        color_discrete_sequence=["#3b82f6", "#f59e0b"],
        labels={"Sales": "Revenue (₹)"},
    )
    fig5.update_layout(height=380, xaxis_tickangle=-20, yaxis_title="Revenue (₹)")
    st.plotly_chart(fig5, use_container_width=True)

    # Rating distribution
    st.markdown('<div class="section-title">Rating Distribution</div>', unsafe_allow_html=True)
    rat_df = rating_distribution(df)
    fig6 = px.bar(
        rat_df, x="Rating_Band", y="Count",
        color="Count",
        color_continuous_scale="YlGn",
        text="Count",
        labels={"Rating_Band": "Rating Band", "Count": "No. of Transactions"},
    )
    fig6.update_traces(textposition="outside")
    fig6.update_layout(coloraxis_showscale=False, height=320, xaxis_title="Rating Band", yaxis_title="Transactions")
    st.plotly_chart(fig6, use_container_width=True)


# ════════════════════════════════════════════════
# TAB 5 — TIME TRENDS
# ════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">Monthly Revenue Trend</div>', unsafe_allow_html=True)

    monthly = monthly_sales_trend(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month_Label"], y=monthly["Total_Sales"],
        mode="lines+markers+text",
        name="Revenue",
        text=[f"₹{v:,.0f}" for v in monthly["Total_Sales"]],
        textposition="top center",
        line=dict(color="#3b82f6", width=2.5),
        marker=dict(size=8),
    ))
    fig.add_trace(go.Bar(
        x=monthly["Month_Label"], y=monthly["Transactions"],
        name="Transactions",
        yaxis="y2",
        marker_color="rgba(99,179,237,0.35)",
    ))
    fig.update_layout(
        height=420,
        yaxis=dict(title=dict(text="Revenue (₹)", font=dict(color="#3b82f6"))),
        yaxis2=dict(title=dict(text="Transactions", font=dict(color="#63b3ed")), overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=20, b=20),
        xaxis_title="Month",
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Day-of-Week Pattern</div>', unsafe_allow_html=True)
        dow = sales_by_day_of_week(df)
        fig2 = px.bar(
            dow, x="Day_of_Week", y="Total_Sales",
            color="Total_Sales",
            color_continuous_scale="Purples",
            text="Total_Sales",
            labels={"Day_of_Week": "Day", "Total_Sales": "Revenue (₹)"},
        )
        fig2.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig2.update_layout(coloraxis_showscale=False, height=360, yaxis_title="Revenue (₹)")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Monthly Avg Order Value</div>', unsafe_allow_html=True)
        fig3 = px.line(
            monthly, x="Month_Label", y="Avg_Order",
            markers=True,
            text="Avg_Order",
            labels={"Month_Label": "Month", "Avg_Order": "Avg Order (₹)"},
            line_shape="spline",
            color_discrete_sequence=["#10b981"],
        )
        fig3.update_traces(texttemplate="₹%{text:,.2f}", textposition="top center")
        fig3.update_layout(height=360, yaxis_title="Avg Order (₹)")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Category Revenue — Monthly Breakdown</div>', unsafe_allow_html=True)
    cat_monthly = (
        df.groupby(["Month_Label", "Category"])["Sales"]
        .sum()
        .round(2)
        .reset_index()
        .sort_values("Month_Label")
    )
    fig4 = px.area(
        cat_monthly, x="Month_Label", y="Sales",
        color="Category",
        labels={"Month_Label": "Month", "Sales": "Revenue (₹)"},
        line_group="Category",
        groupnorm=None,
    )
    fig4.update_layout(height=400, yaxis_title="Revenue (₹)", xaxis_title="Month")
    st.plotly_chart(fig4, use_container_width=True)


# ════════════════════════════════════════════════
# TAB 6 — PRODUCTS
# ════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)

    n_top = st.slider("Show top N products", min_value=5, max_value=20, value=10, step=1)
    prod_df = top_products(df, n=n_top)

    fig = px.bar(
        prod_df.sort_values("Total_Sales"),
        x="Total_Sales", y="Product",
        orientation="h",
        color="Category",
        text="Total_Sales",
        labels={"Total_Sales": "Revenue (₹)", "Product": "Product"},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_layout(height=450, xaxis_title="Revenue (₹)", margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Units Sold — Top Products</div>', unsafe_allow_html=True)
        fig2 = px.bar(
            prod_df.sort_values("Units_Sold", ascending=False),
            x="Product", y="Units_Sold",
            color="Category",
            text="Units_Sold",
            labels={"Units_Sold": "Units Sold", "Product": "Product"},
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=370, xaxis_tickangle=-30)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Avg Rating — Top Products</div>', unsafe_allow_html=True)
        fig3 = px.scatter(
            prod_df, x="Avg_Rating", y="Total_Sales",
            size="Units_Sold", color="Category",
            hover_name="Product",
            text="Product",
            labels={"Avg_Rating": "Avg Rating", "Total_Sales": "Revenue (₹)"},
        )
        fig3.update_traces(textposition="top center")
        fig3.update_layout(height=370)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">Product Detail Table</div>', unsafe_allow_html=True)
    st.dataframe(prod_df.rename(columns={
        "Product": "Product", "Category": "Category",
        "Total_Sales": "Revenue (₹)", "Transactions": "Transactions",
        "Units_Sold": "Units Sold", "Avg_Rating": "Avg Rating",
    }).style.format({
        "Revenue (₹)": "₹{:,.2f}",
        "Avg Rating": "{:.2f}",
    }), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════
# TAB 7 — DATA QUALITY
# ════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-title">Data Quality Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Results from Step 1 & 2: Load and validate the dataset</div>', unsafe_allow_html=True)

    def status_badge(val: int, warn_threshold: int = 1) -> str:
        if val == 0:
            return f'<span class="quality-ok">✅ {val}</span>'
        elif val <= warn_threshold:
            return f'<span class="quality-warn">⚠️ {val}</span>'
        else:
            return f'<span class="quality-bad">❌ {val}</span>'

    checks = [
        ("Total Missing Values", quality_report["total_missing"], 0),
        ("Duplicate Invoice IDs", quality_report["duplicate_invoice_ids"], 0),
        ("Negative Quantity Rows", quality_report["negative_quantity"], 0),
        ("Negative Unit Price Rows", quality_report["negative_unit_price"], 0),
        ("Negative Sales Rows", quality_report["negative_sales"], 0),
        ("Sales Mismatch Rows (stored ≠ Qty×Price)", quality_report["sales_mismatch_rows"], 5),
    ]

    col1, col2 = st.columns([1, 1])
    with col1:
        for label, val, warn in checks:
            badge = status_badge(val, warn)
            st.markdown(
                f"<div style='padding:8px 0;border-bottom:1px solid #e5e7eb;font-size:14px'>"
                f"<b>{label}:</b> &nbsp; {badge}</div>",
                unsafe_allow_html=True,
            )

    with col2:
        missing = quality_report.get("missing_values", {})
        if missing:
            st.warning(f"Columns with missing data: {missing}")
        else:
            st.success("✅ No missing values found in any column.")
        st.info(
            f"📋 **Dataset Summary**\n\n"
            f"- Total rows loaded: **{len(df_full):,}**\n"
            f"- Columns: **{', '.join(df_full.columns.tolist())}**\n"
            f"- Date range: **{df_full['Date'].min().date()}** → **{df_full['Date'].max().date()}**\n"
            f"- Branches: **{df_full['Branch'].nunique()}** | Cities: **{df_full['City'].nunique()}**\n"
            f"- Categories: **{df_full['Category'].nunique()}** | Products: **{df_full['Product'].nunique()}**"
        )

    st.markdown('<div class="section-title">Sales Calculation Verification</div>', unsafe_allow_html=True)
    st.markdown(
        """
        **Step 3 — Sales = Quantity × Unit Price**

        The `Sales` column is recalculated on load using:
        ```
        df["Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)
        ```
        This ensures all downstream analysis is consistent regardless of any pre-existing values
        in the original CSV.
        """,
    )
    sample = df[["Invoice ID", "Date", "Product", "Quantity", "Unit Price", "Sales"]].head(10)
    st.dataframe(sample.style.format({
        "Unit Price": "₹{:,.2f}",
        "Sales": "₹{:,.2f}",
    }), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Full Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.drop(columns=["Month", "Month_Label", "Quarter", "Day_of_Week"], errors="ignore").head(50).style.format({
        "Unit Price": "₹{:,.2f}",
        "Sales": "₹{:,.2f}",
    }), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════
# TAB 8 — INSIGHTS
# ════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-title">Business Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Data-driven recommendations derived from Step 4–6 analysis</div>',
        unsafe_allow_html=True,
    )

    insights = generate_insights(df, kpis)
    for ins in insights:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">{ins['icon']} &nbsp; {ins['title']}</div>
                <div style="font-size:14px;color:#374151;">{ins['detail']}</div>
                <div class="insight-action">🎯 Action: {ins['action']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Summary Statistics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Numeric Column Statistics**")
        num_cols = ["Quantity", "Unit Price", "Sales", "Rating"]
        desc = df[num_cols].describe().T.round(2)
        st.dataframe(desc.style.format("{:.2f}"), use_container_width=True)
    with col2:
        st.markdown("**Revenue by Gender × Customer Type**")
        cross = (
            df.groupby(["Gender", "Customer Type"])["Sales"]
            .agg(["sum", "count", "mean"])
            .round(2)
            .rename(columns={"sum": "Total (₹)", "count": "Txns", "mean": "Avg (₹)"})
            .reset_index()
        )
        st.dataframe(cross.style.format({
            "Total (₹)": "₹{:,.2f}",
            "Avg (₹)": "₹{:,.2f}",
        }), use_container_width=True, hide_index=True)

    # Final comparison bar chart
    st.markdown('<div class="section-title">Category Comparison — Revenue vs Avg Rating</div>', unsafe_allow_html=True)
    cat_df2 = sales_by_category(df)
    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(
        x=cat_df2["Category"], y=cat_df2["Total_Sales"],
        name="Total Revenue (₹)", marker_color="#3b82f6",
        yaxis="y",
    ))
    fig_cmp.add_trace(go.Scatter(
        x=cat_df2["Category"], y=cat_df2["Avg_Rating"],
        name="Avg Rating", mode="lines+markers",
        marker=dict(color="#f59e0b", size=9),
        line=dict(color="#f59e0b", width=2),
        yaxis="y2",
    ))
    fig_cmp.update_layout(
        height=400,
        yaxis=dict(title=dict(text="Total Revenue (₹)", font=dict(color="#3b82f6"))),
        yaxis2=dict(title=dict(text="Avg Rating (0–5)", font=dict(color="#f59e0b")),
                    overlaying="y", side="right", range=[0, 5.5]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_tickangle=-20,
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig_cmp, use_container_width=True)


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:12px;color:#9ca3af;'>"
    "🛒 Supermarket Sales Analytics Dashboard &nbsp;|&nbsp; Built with Streamlit &amp; Plotly"
    "</p>",
    unsafe_allow_html=True,
)
