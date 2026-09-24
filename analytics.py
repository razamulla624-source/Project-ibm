"""
analytics.py
------------
Step 4: Group and summarize data — totals, counts, and averages.
All functions accept a clean DataFrame and return a DataFrame or scalar.
"""

import pandas as pd


# ─────────────────────────────────────────────
# 1. Overall KPIs
# ─────────────────────────────────────────────

def overall_kpis(df: pd.DataFrame) -> dict:
    """Top-level business metrics."""
    return {
        "total_revenue": round(df["Sales"].sum(), 2),
        "total_transactions": len(df),
        "avg_order_value": round(df["Sales"].mean(), 2),
        "total_units_sold": int(df["Quantity"].sum()),
        "avg_rating": round(df["Rating"].mean(), 2),
        "unique_products": df["Product"].nunique(),
        "unique_customers": df["Invoice ID"].nunique(),
        "date_range_start": str(df["Date"].min().date()),
        "date_range_end": str(df["Date"].max().date()),
    }


# ─────────────────────────────────────────────
# 2. Sales by Category
# ─────────────────────────────────────────────

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Total sales, transaction count, and average order per category."""
    grp = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
            Units_Sold=("Quantity", "sum"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .reset_index()
    )
    grp["Sales_Share_%"] = (grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(2)
    return grp


# ─────────────────────────────────────────────
# 3. Sales by Branch / City
# ─────────────────────────────────────────────

def sales_by_branch(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby(["Branch", "City"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .reset_index()
    )
    return grp


# ─────────────────────────────────────────────
# 4. Sales by Customer Type
# ─────────────────────────────────────────────

def sales_by_customer_type(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Customer Type")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
        )
        .round(2)
        .reset_index()
    )
    grp["Sales_Share_%"] = (grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(2)
    return grp


# ─────────────────────────────────────────────
# 5. Sales by Gender
# ─────────────────────────────────────────────

def sales_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Gender")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
        )
        .round(2)
        .reset_index()
    )
    grp["Sales_Share_%"] = (grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(2)
    return grp


# ─────────────────────────────────────────────
# 6. Sales by Payment Method
# ─────────────────────────────────────────────

def sales_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Payment")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .reset_index()
    )
    grp["Sales_Share_%"] = (grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(2)
    return grp


# ─────────────────────────────────────────────
# 7. Monthly Sales Trend
# ─────────────────────────────────────────────

def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby("Month_Label")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("Month_Label")
    )
    return grp


# ─────────────────────────────────────────────
# 8. Top Products
# ─────────────────────────────────────────────

def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    grp = (
        df.groupby(["Product", "Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Units_Sold=("Quantity", "sum"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .head(n)
        .reset_index()
    )
    return grp


# ─────────────────────────────────────────────
# 9. Rating Distribution
# ─────────────────────────────────────────────

def rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Bin ratings 1–5 and count."""
    bins = [1, 2, 3, 4, 5, 5.1]
    labels = ["1–2", "2–3", "3–4", "4–5", "5"]
    df = df.copy()
    df["Rating_Band"] = pd.cut(df["Rating"], bins=bins, labels=labels, right=False, include_lowest=True)
    return df.groupby("Rating_Band", observed=True).size().reset_index(name="Count")


# ─────────────────────────────────────────────
# 10. Category × Branch heatmap data
# ─────────────────────────────────────────────

def category_branch_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    pivot = (
        df.groupby(["Category", "City"])["Sales"]
        .sum()
        .round(2)
        .unstack(fill_value=0)
        .reset_index()
    )
    return pivot


# ─────────────────────────────────────────────
# 11. Day-of-Week Pattern
# ─────────────────────────────────────────────

def sales_by_day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grp = (
        df.groupby("Day_of_Week")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
        )
        .round(2)
        .reindex(order)
        .reset_index()
    )
    return grp


# ─────────────────────────────────────────────
# 12. Business Recommendations
# ─────────────────────────────────────────────

def generate_insights(df: pd.DataFrame, kpis: dict) -> list[dict]:
    """Return a list of actionable business insights derived from data."""
    insights = []

    # Top category
    cat = sales_by_category(df)
    top_cat = cat.iloc[0]
    low_cat = cat.iloc[-1]
    insights.append({
        "icon": "🏆",
        "title": f"Best-Selling Category: {top_cat['Category']}",
        "detail": (
            f"**{top_cat['Category']}** generates ₹{top_cat['Total_Sales']:,.2f} in revenue "
            f"({top_cat['Sales_Share_%']}% of total). "
            f"Stock priority and promotional budgets should favour this category."
        ),
        "action": "Increase stock, run loyalty discounts.",
    })

    insights.append({
        "icon": "⚠️",
        "title": f"Under-Performing Category: {low_cat['Category']}",
        "detail": (
            f"**{low_cat['Category']}** accounts for only ₹{low_cat['Total_Sales']:,.2f} "
            f"({low_cat['Sales_Share_%']}% of total). "
            f"Review pricing, shelf placement, or promotional strategy."
        ),
        "action": "Run targeted promotions or reconsider product mix.",
    })

    # Top branch
    branch = sales_by_branch(df)
    top_branch = branch.iloc[0]
    insights.append({
        "icon": "📍",
        "title": f"Top Branch: {top_branch['City']} (Branch {top_branch['Branch']})",
        "detail": (
            f"Branch **{top_branch['Branch']} – {top_branch['City']}** leads with "
            f"₹{top_branch['Total_Sales']:,.2f} revenue and avg rating "
            f"{top_branch['Avg_Rating']}. Replicate its best practices across other branches."
        ),
        "action": "Share successful practices; assign top performers here.",
    })

    # Payment preference
    pay = sales_by_payment(df)
    top_pay = pay.iloc[0]
    insights.append({
        "icon": "💳",
        "title": f"Preferred Payment: {top_pay['Payment']}",
        "detail": (
            f"**{top_pay['Payment']}** is the most used payment method "
            f"({top_pay['Sales_Share_%']}% of revenue). "
            f"Ensure seamless checkout and consider exclusive offers for this method."
        ),
        "action": "Partner with payment provider for cashback offers.",
    })

    # Customer type
    cust = sales_by_customer_type(df)
    if len(cust) == 2:
        member_row = cust[cust["Customer Type"] == "Member"].iloc[0]
        normal_row = cust[cust["Customer Type"] == "Normal"].iloc[0]
        diff = member_row["Avg_Order"] - normal_row["Avg_Order"]
        direction = "higher" if diff > 0 else "lower"
        insights.append({
            "icon": "👥",
            "title": "Member vs Normal Customer Spend",
            "detail": (
                f"Members spend on average ₹{abs(diff):.2f} **{direction}** per order than normal customers. "
                f"{'Growing the membership base can directly boost revenue.' if diff > 0 else 'Consider enhancing membership benefits to increase member spend.'}"
            ),
            "action": "Expand loyalty programme with tiered rewards.",
        })

    # Rating health
    avg_rating = kpis["avg_rating"]
    rating_status = "healthy" if avg_rating >= 4.0 else "needs attention"
    insights.append({
        "icon": "⭐",
        "title": f"Customer Satisfaction: {avg_rating} / 5.0",
        "detail": (
            f"Overall average rating is **{avg_rating}**, which is {rating_status}. "
            f"{'Maintain quality and staff training to sustain this.' if avg_rating >= 4.0 else 'Identify low-rated product lines and address root causes.'}"
        ),
        "action": "Introduce post-purchase feedback loop for low-rated products.",
    })

    # Monthly trend
    trend = monthly_sales_trend(df)
    if len(trend) >= 2:
        best_month = trend.loc[trend["Total_Sales"].idxmax(), "Month_Label"]
        worst_month = trend.loc[trend["Total_Sales"].idxmin(), "Month_Label"]
        insights.append({
            "icon": "📈",
            "title": "Seasonal Revenue Pattern",
            "detail": (
                f"Highest revenue recorded in **{best_month}**; lowest in **{worst_month}**. "
                f"Plan inventory build-up and marketing campaigns ahead of peak months."
            ),
            "action": "Pre-stock peak-demand items before high-sales months.",
        })

    return insights
