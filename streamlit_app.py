from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd

import streamlit as st

# Set the title and favicon that appear in the Browser's tab bar.
#st.set_page_config(
#    page_title="AVANI",
#    page_icon=":progress:",  # This is an emoji shortcode. Could be a URL too.
#)
# ✅ Must be the first Streamlit command
st.set_page_config(page_title="Inventory Tracker", page_icon="📦", layout="wide")


import streamlit as st


import streamlit as st
import requests
from streamlit_lottie import st_lottie
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json
import streamlit as st
import requests
from streamlit_lottie import st_lottie




import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Inventory Animation
inventory_lottie = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_ydo1amjm.json")

# Theme Toggle (Light/Dark Mode)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

mode = st.sidebar.radio("🎨 Select Theme", ("Light", "Dark"))
st.session_state.dark_mode = mode == "Dark"

# Background and Text Theme
light_css = """
<style>
body {
    background: linear-gradient(to right, #f9f9f9, #e0eafc);
}
h1, h2, h3, p, label {
    color: #111 !important;
}
</style>
"""

dark_css = """
<style>
body {
    background: linear-gradient(to right, #232526, #414345);
}
h1, h2, h3, p, label {
    color: #eee !important;
}
</style>
"""

st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# Login function
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""

    if not st.session_state.authenticated:
        col1, col2 = st.columns([1, 2])
        with col1:
            st_lottie(inventory_lottie, height=250)
        with col2:
            st.markdown("<h2 style='text-align:center;'>🔐 Admin Login</h2>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    if username == "admin" and password == "Suhas@123":
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful! 🎉")
                    else:
                        st.error("Invalid username or password 🚫")
    return st.session_state.authenticated

# Login gate
if not login():
    st.stop()

# --- Main App Content ---
st.markdown(f"""
    <h1 style='text-align:center; animation: fadeIn 1.5s;'>📦 Inventory Tracker Dashboard</h1>
    <h4 style='text-align:center; margin-bottom:30px;'>Welcome <b>{st.session_state.username}</b>! Track and manage inventory efficiently.</h4>
""", unsafe_allow_html=True)

# Stylish card section
st.markdown("""
<style>
.card {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 15px;
    background-color: rgba(255,255,255,0.1);
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 40px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'><h3>➕ Add Item</h3><p>Enter and manage new inventory items.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'><h3>📊 View Stock</h3><p>See current stock levels and trends.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='card'><h3>🚨 Alerts</h3><p>Get alerts for low or critical stock.</p></div>", unsafe_allow_html=True)

# Optional logout
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", key="logout_button"):
    st.session_state.authenticated = False
   # st.experimental_rerun()  Rerun to show the login page

# Some logic or user interaction
if st.button("Rerun", key="rerun_button"):
    st.experimental_rerun()

# Optional: Add the logout button at the top or sidebar
#if st.sidebar.button("🚪 Logout", key="logout_sidebar"):
   # st.session_state.authenticated = False
   # st.experimental_rerun()
    
# Simulate an authentication state (use this as a flag to track login status)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Sidebar Logout Button
#st.sidebar.markdown("---")
#if st.sidebar.button("🚪 Logout", key="sidebar_logout_button"):
    # Set authentication to False
   # st.session_state.authenticated = False
    # Trigger rerun to redirect to login page
    #st.experimental_rerun()

# Login page logic
if not st.session_state.authenticated:
    # This is the login page (you can customize this as needed)
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Sample credentials check (you can modify this as per your requirements)
    if st.button("Login", key="login_button"):
        if username == "admin" and password == "password":  # Change to your credentials
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# The main app page (accessible only if authenticated)
if st.session_state.authenticated:
    st.title("Welcome to the Admin Dashboard!")
    st.write("This is where your app content goes.")



url = "https://newinventory.streamlit.app/"
st.markdown(f"[Create ]({url})", unsafe_allow_html=True)
    # Add your application logic here

    # Optional: Add the logout button at the top or sidebar
   # st.sidebar.markdown("---")
   # if st.sidebar.button("🚪 Logout", key="logout_final"):
   #     st.session_state.authenticated = False
  #      st.experimental_rerun()


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
    
 #  st.write(f"price: ₹{price:.2f}"

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
('Bisleri Water (500ml)', 50, 115, 15, 20.00, 5, 'Pure mineral water'),  
('Thums Up (300ml)', 40, 93, 8, 35.00, 10, 'Strong carbonated cola drink'),  
('Red Bull (250ml)', 125, 12, 18, 70.00, 8, 'Energy-boosting drink'),  
('Nescafe Coffee (hot, large)', 55, 11, 14, 40.00, 5, 'Freshly brewed instant coffee'),  
('Real Fruit Juice (200ml)', 45, 11, 9, 35.00, 5, 'Healthy mixed fruit juice'),  
('Masala Chai (Cup)', 100, 11, 12, 20.00, 5, 'Authentic Indian spiced tea'),  

-- Snacks  
('Lays Chips (small)', 50, 34, 16, 20.00, 10, 'Crispy salted potato chips'),  
('Dairy Milk Chocolate', 50, 6, 19, 35.00, 5, 'Milk chocolate bar'),  
('Britannia Nutri Bar', 40, 3, 12, 30.00, 8, 'Healthy granola bar with nuts'),  
('Parle-G Biscuits (large pack)', 80, 8, 8, 40.00, 5, 'Classic glucose biscuits'),  
('Haldiram’s Namkeen (small)', 60, 5, 10, 40.00, 8, 'Spicy and crunchy Indian snack'),  

-- Personal Care  
('Colgate Toothpaste (small)', 20, 1, 9, 15.00, 5, 'Fluoride toothpaste for strong teeth'),  
('Dettol Hand Sanitizer (small)', 40, 2, 13, 25.00, 8, 'Antibacterial sanitizer for hygiene'),  
('Crocin Pain Reliever (strip)', 40, 1, 5, 35.00, 3, 'Over-the-counter paracetamol tablet'),  
('Band-Aid Strips (box)', 25, 0, 10, 20.00, 5, 'Adhesive bandages for wounds'),  
('Himalaya Sunscreen (small)', 150, 6, 5, 120.00, 3, 'Herbal sunscreen lotion'),  
('Mediker Anti-Lice Shampoo', 100, 6, 8, 75.00, 5, 'Effective shampoo for lice removal'),  

-- Household  
('Eveready AA Batteries (4-pack)', 100, 1, 5, 70.00, 3, 'Long-lasting alkaline batteries'),  
('Syska LED Bulb (9W, 2-pack)', 200, 3, 3, 150.00, 2, 'Energy-efficient LED bulbs'),  
('Garbage Bags (small, 10-pack)', 70, 5, 10, 50.00, 5, 'Disposable trash bags for home use'),  
('Origami Paper Towels (single roll)', 40, 3, 8, 30.00, 5, 'Absorbent paper towels'),  
('Harpic Toilet Cleaner (500ml)', 105, 2, 5, 95.00, 3, 'Powerful toilet cleaning liquid'),  

-- Others  
('Lottery Tickets', 20, 17, 20, 15.00, 10, 'Government-approved lottery tickets'),  
('The Times of India Newspaper', 12, 22, 20, 10.00, 5, 'Daily national newspaper'),  
('Ball Pens (5-pack)', 70, 1, 8, 50.00, 5, 'Smooth writing ball pens'),  
('Natraj Pencils (10-pack)', 60, 1, 8, 30.00, 5, 'High-quality HB pencils'),  
('Classmate Notebook (200 pages)', 50, 1, 8, 40.00, 5, 'Spiral-bound ruled notebook');       
        """
    )
    conn.commit()




# ---------- Database Connection ----------
#def connect_db():
#    """Connects to the SQLite database (create one if it doesn't exist)."""
#    return sqlite3.connect("inventory.db")


# ---------- Load Data from Database ----------
load_data(conn):
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

# ---------- Update Data in Database ----------
def update_data(df, changes):
    """Updates the inventory data in the database based on changes."""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        if changes.get("edited_rows"):
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

        if changes.get("added_rows"):
            cursor.executemany(
                """
                INSERT INTO inventory
                    (id, item_name, price, units_sold, units_left, cost_price, reorder_point, description)
                VALUES
                    (:id, :item_name, :price, :units_sold, :units_left, :cost_price, :reorder_point, :description)
                """,
                (defaultdict(lambda: None, row) for row in changes["added_rows"]),
            )

        if changes.get("deleted_rows"):
            cursor.executemany(
                "DELETE FROM inventory WHERE id = :id",
                ({"id": int(df.loc[i, "id"])} for i in changes["deleted_rows"]),
            )

        conn.commit()

    except Exception as e:
        st.error(f"Failed to update data: {e}")

    finally:
        conn.close()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.
# **Welcome to KGI-Corner Store's intentory tracker!**
# This page reads and writes directly from/to our inventory database.
# Set the title that appears at the top of the page.
# :shopping_bags:KGI-AVANI  **Welcome to KGI-Corner Store's Intelligent Inventory Tracker!** Powered by AVANI (Advanced Visual Analytics for Networked Insights),
"""

# 🛒 VISSU4-STORES 


 This tool seamlessly connects to our inventory database to provide:

📊 Real-Time Updates
🔍 Advanced Analytics
🚀 Effortless Inventory Management

Optimize your store operations with VISSU4-intelligent solution!


"""
# """
#💎 NIDHI: Next-Generation Intelligent Analytics
#Unlock the treasure of insights from your inventory and supply chain by uploading your data.
#"""
#url = "https://nidhii.streamlit.app/"
#st.markdown(f"[Access NIDHI]({url})", unsafe_allow_html=True)

#"""
#💎 KGI-INDUSTRY 5.0 APPS 
#"""
#url = "https://finacle.streamlit.app/"
#st.markdown(f"[Access Fincal ]({url})", unsafe_allow_html=True)

#url = "https://kgi-financecalculator.streamlit.app/"
#st.markdown(f"[Access CALCULATOR ]({url})", unsafe_allow_html=True)

#url = "https://kgi-manager.streamlit.app/"
#st.markdown(f"[Access TASK MANAGER ]({url})", unsafe_allow_html=True)

#url = "https://kgi-stock-market-tracker.streamlit.app/"
#st.markdown(f"[Access STOCK MARKET ]({url})", unsafe_allow_html=True)

#url = "https://multilocation.streamlit.app/"
#st.markdown(f"[Access MULTILOACTION]({url})", unsafe_allow_html=True)

#url = "https://sankalp.streamlit.app/"
#st.markdown(f"[Access SANKALP]({url})", unsafe_allow_html=True)

#url = "https://sandra.streamlit.app/"
#st.markdown(f"[Access Sandra]({url})", unsafe_allow_html=True)


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
        "price": st.column_config.NumberColumn(format="₹%.2f"),
        "cost_price": st.column_config.NumberColumn(format="₹%.2f"),
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
# --- Search and Checkout ---
# ✅ Search and Checkout
#st.subheader("🔍 Search & Checkout Items")

#df = st.session_state.inventory_data

#search = st.text_input("Search for an item", placeholder="e.g. Mouse")
#filtered_df = df[df["Item"].str.contains(search, case=False)] if search else df

#if not filtered_df.empty:
 #   selected_item = st.selectbox("Select item to checkout", filtered_df["Item"].tolist())
  #  item_row = df[df["Item"] == selected_item].iloc[0]
   # max_qty = int(item_row["Quantity"])
   # checkout_qty = st.number_input("Enter quantity to checkout", min_value=1, max_value=max_qty, value=1)


   # if st.button("✅ Checkout"):
       # idx = df[df["Item"] == selected_item].index[0]
      #  new_qty = max_qty - checkout_qty

        # ✅ Update local data
     #   st.session_state.inventory_data.at[idx, "Quantity"] = new_qty

        # ✅ Update database
    #    cursor = conn.cursor()
   #     cursor.execute("UPDATE inventory SET Quantity = ? WHERE Item = ?", (new_qty, selected_item))
  #      conn.commit()

 #       st.success(f"Checked out {checkout_qty} x {selected_item}")
#else:
#    st.warning("No matching items found.")




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

best_sellers = df.sort_values(by="units_sold", ascending=False).head(10)

st.altair_chart(
    alt.Chart(best_sellers)
    .mark_bar()
    .encode(
        x="units_sold",
        y=alt.Y("item_name", sort="-x"),
        tooltip=["item_name", "units_sold"]
    ),
    use_container_width=True
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

# Filter out rows with negative profit
# Ensure that 'revenue' and 'profit' columns are created before filtering
#df["revenue"] = df["units_sold"] * df["price"]
#df["profit"] = df["units_sold"] * (df["price"] - df["cost_price"])

# Filter out rows with negative profit
#df_filtered = df[df["profit"] >= 0]

# Plot the chart
#st.subheader("Revenue vs Profit", divider="green")
#st.altair_chart(
#    alt.Chart(df_filtered)
#    .mark_bar()
 #   .encode(
  #      y=alt.Y("item_name", title="Product").sort("-x"),
   #     x="revenue",
    #    color=alt.value("steelblue"),
     #   tooltip=["item_name", "revenue", "profit"]
  #  ) + 
  #  alt.Chart(df_filtered)
   # .mark_bar()
   # .encode(
    #    y="item_name",
     #   x="profit",
      #  color=alt.value("orange"),
       # tooltip=["item_name", "revenue", "profit"]
    #),
    #use_container_width=True,
#)










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

