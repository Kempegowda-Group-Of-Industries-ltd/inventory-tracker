from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="AVANI",
    page_icon=":progress:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.


def connect_db():
    """Connects to the sqlite database."""

    DB_FILENAME = Path(__file__).parent / "inventory.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    """Initializes the inventory table with some data."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL,
            units_sold INTEGER,
            units_left INTEGER,
            cost_price REAL,
            reorder_point INTEGER,
            description TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO inventory
            (item_name, price, units_sold, units_left, cost_price, reorder_point, description)
        VALUES
            -- Beverages
            ('Bottled Water (500ml)', 1.50, 115, 15, 0.80, 16, 'Hydrating bottled water'),
            ('Soda (355ml)', 2.00, 93, 8, 1.20, 10, 'Carbonated soft drink'),
            ('Energy Drink (250ml)', 2.50, 12, 18, 1.50, 8, 'High-caffeine energy drink'),
            ('Coffee (hot, large)', 2.75, 11, 14, 1.80, 5, 'Freshly brewed hot coffee'),
            ('Juice (200ml)', 2.25, 11, 9, 1.30, 5, 'Fruit juice blend'),

            -- Snacks
            ('Potato Chips (small)', 2.00, 34, 16, 1.00, 10, 'Salted and crispy potato chips'),
            ('Candy Bar', 1.50, 6, 19, 0.80, 15, 'Chocolate and candy bar'),
            ('Granola Bar', 2.25, 3, 12, 1.30, 8, 'Healthy and nutritious granola bar'),
            ('Cookies (pack of 6)', 2.50, 8, 8, 1.50, 5, 'Soft and chewy cookies'),
            ('Fruit Snack Pack', 1.75, 5, 10, 1.00, 8, 'Assortment of dried fruits and nuts'),

            -- Personal Care
            ('Toothpaste', 3.50, 1, 9, 2.00, 5, 'Minty toothpaste for oral hygiene'),
            ('Hand Sanitizer (small)', 2.00, 2, 13, 1.20, 8, 'Small sanitizer bottle for on-the-go'),
            ('Pain Relievers (pack)', 5.00, 1, 5, 3.00, 3, 'Over-the-counter pain relief medication'),
            ('Bandages (box)', 3.00, 0, 10, 2.00, 5, 'Box of adhesive bandages for minor cuts'),
            ('Sunscreen (small)', 5.50, 6, 5, 3.50, 3, 'Small bottle of sunscreen for sun protection'),

            -- Household
            ('Batteries (AA, pack of 4)', 4.00, 1, 5, 2.50, 3, 'Pack of 4 AA batteries'),
            ('Light Bulbs (LED, 2-pack)', 6.00, 3, 3, 4.00, 2, 'Energy-efficient LED light bulbs'),
            ('Trash Bags (small, 10-pack)', 3.00, 5, 10, 2.00, 5, 'Small trash bags for everyday use'),
            ('Paper Towels (single roll)', 2.50, 3, 8, 1.50, 5, 'Single roll of paper towels'),
            ('Multi-Surface Cleaner', 4.50, 2, 5, 3.00, 3, 'All-purpose cleaning spray'),

            -- Others
            ('Lottery Tickets', 2.00, 17, 20, 1.50, 10, 'Assorted lottery tickets'),
            ('Newspaper', 1.50, 22, 20, 1.00, 5, 'Daily newspaper')
        """
    )
    conn.commit()


def load_data(conn):
    """Loads the inventory data from the database."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "id",
            "item_name",
            "price",
            "units_sold",
            "units_left",
            "cost_price",
            "reorder_point",
            "description",
        ],
    )

    return df


def update_data(conn, df, changes):
    """Updates the inventory data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        deltas = st.session_state.inventory_table["edited_rows"]
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            """
            UPDATE inventory
            SET
                item_name = :item_name,
                price = :price,
                units_sold = :units_sold,
                units_left = :units_left,
                cost_price = :cost_price,
                reorder_point = :reorder_point,
                description = :description
            WHERE id = :id
            """,
            rows,
        )

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO inventory
                (id, item_name, price, units_sold, units_left, cost_price, reorder_point, description)
            VALUES
                (:id, :item_name, :price, :units_sold, :units_left, :cost_price, :reorder_point, :description)
            """,
            (defaultdict(lambda: None, row) for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        cursor.executemany(
            "DELETE FROM inventory WHERE id = :id",
            ({"id": int(df.loc[i, "id"])} for i in changes["deleted_rows"]),
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.
# **Welcome to KGI-Corner Store's intentory tracker!**
# This page reads and writes directly from/to our inventory database.
# Set the title that appears at the top of the page.
"""
# :shopping_bags:KGI - AVANI 



**Welcome to KGI-Corner Store's Intelligent Inventory Tracker!**
Powered by AVANI (Advanced Visual Analytics for Networked Insights), this tool seamlessly connects to our inventory database to provide:

📊 Real-Time Updates
🔍 Advanced Analytics
🚀 Effortless Inventory Management

Optimize your store operations with AVANI's intelligent solutions!


"""

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast("Database initialized with some sample data.")

# Load data from database
df = load_data(conn)

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    column_config={
        # Show dollar sign before price columns.
        "price": st.column_config.NumberColumn(format="$%.2f"),
        "cost_price": st.column_config.NumberColumn(format="$%.2f"),
    },
    key="inventory_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.inventory_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.inventory_table),
)


# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Units left", divider="red")

need_to_reorder = df[df["units_left"] < df["reorder_point"]].loc[:, "item_name"]

if len(need_to_reorder) > 0:
    items = "\n".join(f"* {name}" for name in need_to_reorder)

    st.error(f"We're running dangerously low on the items below:\n {items}")

""
""

st.altair_chart(
    # Layer 1: Bar chart.
    alt.Chart(df)
    .mark_bar(
        orient="horizontal",
    )
    .encode(
        x="units_left",
        y="item_name",
    )
    # Layer 2: Chart showing the reorder point.
    + alt.Chart(df)
    .mark_point(
        shape="diamond",
        filled=True,
        size=50,
        color="salmon",
        opacity=1,
    )
    .encode(
        x="reorder_point",
        y="item_name",
    ),
    use_container_width=True,
)

st.caption("NOTE: The :diamonds: location shows the reorder point.")

""
""
""

# -----------------------------------------------------------------------------

st.subheader("Best sellers", divider="orange")

""
""

st.altair_chart(
    alt.Chart(df)
    .mark_bar(orient="horizontal")
    .encode(
        x="units_sold",
        y=alt.Y("item_name").sort("-x"),
    ),
    use_container_width=True,
)


# -----------------------------------------------------------------------------
# Additional visualizations for inventory data

st.subheader("Item Category Insights", divider="blue")

# PIE CHART: Proportion of Units Sold
st.write("### Proportion of Units Sold")
pie_chart = (
    alt.Chart(df)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("units_sold:Q", title="Units Sold"),
        color=alt.Color("item_name:N", legend=None),
        tooltip=["item_name", "units_sold"]
    )
)
st.altair_chart(pie_chart, use_container_width=True)

# LINE CHART: Price vs Units Sold
st.write("### Price vs Units Sold")
line_chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x=alt.X("price:Q", title="Item Price"),
        y=alt.Y("units_sold:Q", title="Units Sold"),
        tooltip=["item_name", "price", "units_sold"]
    )
)
st.altair_chart(line_chart, use_container_width=True)

# SCATTER PLOT: Price vs Cost Price with Units Sold
st.write("### Price vs Cost Price with Units Sold")
scatter_plot = (
    alt.Chart(df)
    .mark_circle(size=100)
    .encode(
        x="cost_price:Q",
        y="price:Q",
        size="units_sold:Q",
        color="item_name:N",
        tooltip=["item_name", "price", "cost_price", "units_sold"]
    )
)
st.altair_chart(scatter_plot, use_container_width=True)



# BOX PLOT: Distribution of Units Left
st.write("### Units Left Distribution")
box_plot = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        x=alt.X("item_name:N", title="Item Name"),
        y=alt.Y("units_left:Q", title="Units Left"),
        color=alt.Color("item_name:N", legend=None)
    )
)
st.altair_chart(box_plot, use_container_width=True)

# TREEMAP: Units Sold Contribution
st.write("### Units Sold Contribution")
treemap_data = df[["item_name", "units_sold"]].copy()
treemap_data["units_sold_size"] = treemap_data["units_sold"]
treemap_chart = (
    alt.Chart(treemap_data)
    .mark_rect()
    .encode(
        x="item_name:N",
        y="units_sold_size:Q",
        color="item_name:N",
        tooltip=["item_name", "units_sold"]
    )
)
st.altair_chart(treemap_chart, use_container_width=True)

# STACKED BAR CHART: Units Sold vs Units Left
st.write("### Units Sold vs Units Left")
stacked_chart = (
    alt.Chart(df.melt(id_vars=["item_name"], value_vars=["units_sold", "units_left"]))
    .mark_bar()
    .encode(
        x="value:Q",
        y=alt.Y("item_name:N", title="Item Name").sort("-x"),
        color="variable:N",
        tooltip=["item_name", "variable", "value"]
    )
)
st.altair_chart(stacked_chart, use_container_width=True)

# Calculate revenue and profit for each item
df["revenue"] = df["units_sold"] * df["price"]
df["profit"] = df["units_sold"] * (df["price"] - df["cost_price"])

st.subheader("Revenue vs Profit", divider="green")
st.altair_chart(
    alt.Chart(df)
    .mark_bar()
    .encode(
        y=alt.Y("item_name", title="Product").sort("-x"),
        x="revenue",
        color=alt.value("steelblue"),
        tooltip=["item_name", "revenue", "profit"]
    ) + 
    alt.Chart(df)
    .mark_bar()
    .encode(
        y="item_name",
        x="profit",
        color=alt.value("orange"),
        tooltip=["item_name", "revenue", "profit"]
    ),
    use_container_width=True,
)


st.subheader("Inventory Balance: Units Sold vs Units Left", divider="blue")

chart = (
    alt.Chart(df)
    .transform_fold(
        ["units_sold", "units_left"],
        as_=["Type", "Count"]
    )
    .mark_bar()
    .encode(
        x="Count:Q",
        y=alt.Y("item_name:N", title="Product").sort("-x"),
        color="Type:N",
        tooltip=["item_name", "units_sold", "units_left"]
    )
)

st.altair_chart(chart, use_container_width=True)




df["stock_status"] = df.apply(
    lambda row: "Low Stock" if row["units_left"] < row["reorder_point"] else "Sufficient",
    axis=1
)

st.subheader("Reorder Status of Inventory", divider="red")

st.altair_chart(
    alt.Chart(df)
    .mark_bar()
    .encode(
        y=alt.Y("item_name", title="Product").sort("-x"),
        x="units_left",
        color=alt.Color("stock_status", scale=alt.Scale(domain=["Low Stock", "Sufficient"], range=["red", "green"])),
        tooltip=["item_name", "units_left", "stock_status"]
    ),
    use_container_width=True,
)

import plotly.express as px

st.subheader("Sales Distribution by Product", divider="orange")

fig = px.pie(
    df,
    values="units_sold",
    names="item_name",
    title="Share of Total Sales by Product",
    hole=0.4,  # Creates a donut chart
)
st.plotly_chart(fig, use_container_width=True)



#ALTER TABLE inventory ADD COLUMN date TEXT DEFAULT CURRENT_DATE;

#st.subheader("Daily Sales Trend", divider="green")

# Assume 'date' column contains sales dates
#daily_sales = df.groupby("date").sum().reset_index()

#st.line_chart(daily_sales, x="date", y="units_sold", use_container_width=True)

