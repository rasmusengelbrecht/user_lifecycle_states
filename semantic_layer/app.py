"""Streamlit app for querying user lifecycle data using semantic layer.

This app allows users to query predefined metrics without writing SQL,
using the boring-semantic-layer library.
"""

import streamlit as st
import pandas as pd
from semantic_model import create_user_lifecycle_semantic_model

st.set_page_config(
    layout="wide",
    page_title="User Lifecycle Analytics",
    page_icon="📊",
)

st.title("📊 User Lifecycle Analytics")

st.markdown(
    """
    Query user lifecycle metrics without writing SQL. Select metrics and dimensions below,
    then click "Run Query" to see results.
    """
)

# Initialize semantic model
@st.cache_resource
def get_semantic_model():
    """Load and cache the semantic model."""
    return create_user_lifecycle_semantic_model()


try:
    semantic_model = get_semantic_model()
    st.success("✅ Connected to DuckDB")
except Exception as e:
    st.error(f"❌ Failed to connect to DuckDB: {e}")
    st.stop()

# Sidebar for query configuration
st.sidebar.header("Query Configuration")

# Add cache clear button
if st.sidebar.button("🔄 Refresh Semantic Model", help="Clear cache and reload semantic model"):
    st.cache_resource.clear()
    st.rerun()

# Define metrics and dimensions
available_metrics = [
    "active_users",
    "mau_percentage",
    "total_users",
    "new_users",
    "retained_users",
    "reactivated_users",
    "resurrected_users",
    "churned_users",
    "dormant_users",
    "churn_rate",
    "pulse_ratio",
]

dimension_options = {
    "User State": "user_state",
}

# Metric selection
st.sidebar.subheader("Metrics")
selected_metrics = st.sidebar.multiselect(
    "Select metrics to query",
    options=available_metrics,
    default=["active_users"],
    help="Choose one or more metrics to calculate",
)

# Dimension selection
st.sidebar.subheader("Dimensions")
selected_dimensions = st.sidebar.multiselect(
    "Select dimensions to group by",
    options=list(dimension_options.keys()),
    help="Choose dimensions to break down your metrics",
)

# Time grain selection
st.sidebar.subheader("Time Dimension")
time_grain_options = {
    "None": None,
    "Month": "TIME_GRAIN_MONTH",
    "Quarter": "TIME_GRAIN_QUARTER",
    "Year": "TIME_GRAIN_YEAR",
}

selected_time_grain = st.sidebar.selectbox(
    "Group by time",
    options=list(time_grain_options.keys()),
    index=1,  # Default to Month
    help="Choose a time granularity to group by",
)

# Date range filter
st.sidebar.subheader("Filters")
use_date_filter = st.sidebar.checkbox("Filter by date range", value=False)

date_from = None
date_to = None

if use_date_filter:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        date_from = st.date_input("From")
    with col2:
        date_to = st.date_input("To")

# Query button
run_query = st.sidebar.button("🚀 Run Query", type="primary", use_container_width=True)

# Main content area
if run_query:
    if not selected_metrics:
        st.warning("⚠️ Please select at least one metric")
    else:
        try:
            with st.spinner("Executing query..."):
                # Build dimension list
                dimensions = [dimension_options[d] for d in selected_dimensions]

                # Get time grain
                time_grain = time_grain_options[selected_time_grain]

                # Build query parameters
                query_params = {
                    "dimensions": dimensions if dimensions else [],
                    "measures": selected_metrics,
                }

                # Add time grain if selected
                if time_grain:
                    query_params["time_grain"] = time_grain

                # Add time range if date filter is specified
                if use_date_filter and date_from and date_to:
                    query_params["time_range"] = {
                        "start": str(date_from),
                        "end": str(date_to),
                    }

                # Query the semantic model
                query = semantic_model.query(**query_params)

                # Show query info for debugging
                with st.expander("🔍 Query Details"):
                    st.write("**Query Parameters:**")
                    st.json(query_params)
                    st.write("**Generated SQL:**")
                    st.code(query.sql(), language="sql")

                # Execute query
                result_df = query.execute()

                # Visualization if time grain is selected
                if time_grain and len(result_df) > 0:
                    st.subheader("Visualization")
                    time_col = "month"

                    if time_col in result_df.columns:
                        # Check if we have dimensions (non-time, non-measure columns)
                        dimension_cols = [col for col in result_df.columns
                                        if col not in [time_col] + selected_metrics]

                        if dimension_cols:
                            # Multiple dimensions - pivot to show one line per dimension value
                            import plotly.express as px

                            # Sort by dimension(s) first, then by time to ensure proper line connections
                            sort_cols = dimension_cols + [time_col]
                            result_df_sorted = result_df.sort_values(sort_cols)

                            # Create a combined dimension column for better labeling
                            if len(dimension_cols) == 1:
                                color_col = dimension_cols[0]
                            else:
                                # Combine multiple dimensions into one label
                                result_df_sorted['dimension_label'] = result_df_sorted[dimension_cols].astype(str).agg(' - '.join, axis=1)
                                color_col = 'dimension_label'

                            # Create line chart with plotly for better control
                            fig = px.line(
                                result_df_sorted,
                                x=time_col,
                                y=selected_metrics[0],  # Use first metric
                                color=color_col,
                                title=f"{selected_metrics[0]} over time by {', '.join(dimension_cols)}",
                                markers=True
                            )

                            # Update layout for better readability
                            fig.update_layout(
                                xaxis_title="Time",
                                yaxis_title=selected_metrics[0],
                                hovermode='x unified'
                            )

                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            # No dimensions - simple time series
                            chart_data = result_df.set_index(time_col)
                            st.line_chart(chart_data[selected_metrics])
                    else:
                        st.info("Time-based visualization not available for this query")

                # Display the dataframe
                with st.expander("See raw data table"):
                    st.dataframe(result_df, use_container_width=True, height=400)

        except Exception as e:
            st.error(f"❌ Query failed: {e}")
            st.exception(e)
else:
    st.info("👈 Configure your query in the sidebar and click 'Run Query' to see results")

# Footer
st.markdown("---")
st.markdown(
    """
    **About this tool:** This application uses the [boring-semantic-layer](https://github.com/boringdata/boring-semantic-layer)
    to provide a SQL-free interface for querying user lifecycle data.
    """
)
