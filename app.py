import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Blinkit Business Analytics",
    page_icon="📊",
    layout="wide"
)

# Aggregate results from the project notebook.
# This is a Blinkit-themed practice dataset, not official Blinkit data.
marketing = pd.DataFrame({
    "Channel": ["Email", "SMS", "Social Media", "App"],
    "Impressions": [7275694, 7367010, 7281244, 7563662],
    "Clicks": [756057, 744274, 738839, 734975],
    "Conversions": [74671, 73235, 74940, 75192],
    "Spend": [3997488.04, 3998607.54, 4110363.91, 4213378.75],
    "Revenue": [8189331.58, 7938649.32, 7990415.98, 8075010.49],
    "CTR": [10.39, 10.10, 10.15, 9.72],
    "Conversion Rate": [9.88, 9.84, 10.14, 10.23],
    "ROAS": [2.05, 1.99, 1.94, 1.92]
})

sentiment = pd.DataFrame({
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Feedback Count": [1620, 1738, 1642],
    "Average Rating": [4.50, 3.52, 2.01]
})

delivery = pd.DataFrame({
    "Delivery Status": ["On time", "Slightly delayed", "Significantly delayed"],
    "Orders": [3470, 1037, 493]
})

inventory = pd.DataFrame({
    "Metric": ["Units received", "Damaged units"],
    "Units": [18485, 1022]
})

st.title("📊 Blinkit Business Analytics")
st.caption(
    "Exploratory analysis of a Blinkit-themed practice dataset. "
    "Figures are from the project notebook and are not official company metrics."
)

# KPI cards
total_spend = marketing["Spend"].sum()
total_revenue = marketing["Revenue"].sum()
total_conversions = marketing["Conversions"].sum()
on_time_rate = 3470 / 5000 * 100
damage_rate = 1022 / 18485 * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Campaign Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Campaign Spend", f"₹{total_spend:,.0f}")
k3.metric("Conversions", f"{total_conversions:,.0f}")
k4.metric("On-time Deliveries", f"{on_time_rate:.1f}%")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "Marketing", "Delivery", "Customer Feedback", "Inventory"
])

with tab1:
    st.subheader("Marketing Campaign Performance")

    selected_channels = st.multiselect(
        "Choose marketing channels",
        options=marketing["Channel"].tolist(),
        default=marketing["Channel"].tolist()
    )
    filtered_marketing = marketing[
        marketing["Channel"].isin(selected_channels)
    ]

    if not filtered_marketing.empty:
        left, right = st.columns(2)

        with left:
            fig = px.bar(
                filtered_marketing,
                x="Channel",
                y="Revenue",
                title="Revenue by Channel",
                labels={"Revenue": "Revenue (₹)"}
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.bar(
                filtered_marketing,
                x="Channel",
                y="ROAS",
                title="Return on Ad Spend (ROAS)",
                labels={"ROAS": "Revenue / Spend"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            filtered_marketing[
                ["Channel", "Impressions", "Clicks", "Conversions",
                 "Spend", "Revenue", "CTR", "Conversion Rate", "ROAS"]
            ],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Select at least one channel to view results.")

with tab2:
    st.subheader("Delivery Performance")

    left, right = st.columns(2)

    with left:
        fig = px.pie(
            delivery,
            names="Delivery Status",
            values="Orders",
            title="Order Delivery Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            delivery,
            x="Delivery Status",
            y="Orders",
            title="Orders by Delivery Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.metric("Average deviation from promised time", "4.44 minutes")
    st.caption(
        "The notebook's delivery_time_minutes field is the difference "
        "between actual and promised delivery time, not total delivery duration."
    )

with tab3:
    st.subheader("Customer Feedback and Sentiment")

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            sentiment,
            x="Sentiment",
            y="Feedback Count",
            title="Feedback Volume by Sentiment"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            sentiment,
            x="Sentiment",
            y="Average Rating",
            title="Average Rating by Sentiment",
            range_y=[0, 5]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(sentiment, hide_index=True, use_container_width=True)

with tab4:
    st.subheader("Inventory Quality")

    left, right = st.columns(2)

    with left:
        st.metric("Units Received", f"{18485:,}")
        st.metric("Damaged Units", f"{1022:,}")
        st.metric("Damage Rate", f"{damage_rate:.2f}%")

    with right:
        fig = px.pie(
            inventory,
            names="Metric",
            values="Units",
            title="Received vs Damaged Units"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Damage rate is calculated as damaged units divided by units received."
    )

st.divider()
st.caption("Built with Python, Streamlit, Pandas, and Plotly.")
