# User Lifecycle Semantic Layer

A lightweight semantic layer for querying user lifecycle metrics using the [boring-semantic-layer](https://github.com/boringdata/boring-semantic-layer) library. Includes a Streamlit app and MCP server for easy querying without SQL.

## Overview

This semantic layer provides a SQL-free interface to query user lifecycle metrics from your DuckDB database, including:

- **MAU (Monthly Active Users)**: Active user counts and percentages
- **User States**: New, Retained, Reactivated, Resurrected, Churned, Dormant
- **Churn Metrics**: Churn rate calculations
- **Pulse Ratio**: Growth health indicator (acquisitions vs churn)

## Setup

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed
- DuckDB database with user_states_monthly table (created by parent project)

### Installation

All dependencies are managed by UV via the parent project's `pyproject.toml`. Simply run:

```bash
# From the project root (user_lifecycle_states/)
./run.sh semantic
```

Or run directly:

```bash
# From semantic_layer directory
uv run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

**Features:**
- Select from 11 predefined metrics
- Group by user state dimension
- Time grouping (month, quarter, year)
- Date range filtering
- Interactive visualizations
- SQL query preview

### MCP Server

The MCP server exposes metrics via the Model Context Protocol, allowing AI assistants like Claude to query your user lifecycle metrics directly.

**Adding to Claude Desktop:**

Add this to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "user-lifecycle": {
      "command": "/absolute/path/to/user_lifecycle_states/.venv/bin/python",
      "args": ["/absolute/path/to/user_lifecycle_states/semantic_layer/mcp_server.py"]
    }
  }
}
```

Replace `/absolute/path/to` with your actual project path. Restart Claude Desktop after updating the config.

## Architecture

### Files

- `semantic_models.yml`: Metric and dimension definitions
- `semantic_model.py`: DuckDB connection and model loader
- `app.py`: Streamlit application
- `mcp_server.py`: MCP server for AI integration
- `README.md`: This file

### Available Metrics

1. **active_users**: Monthly Active Users (MAU)
2. **mau_percentage**: Percentage of total users who are active
3. **total_users**: Total user count
4. **new_users**: First-time active users
5. **retained_users**: Users active in consecutive months
6. **reactivated_users**: Users returning after 1 month
7. **resurrected_users**: Users returning after 2+ months
8. **churned_users**: Users who became inactive
9. **dormant_users**: Inactive users
10. **churn_rate**: Churned / (Churned + Retained)
11. **pulse_ratio**: (New + Reactivated + Resurrected) / Churned

### Available Dimensions

- **user_state**: User lifecycle state (New, Retained, Reactivated, Resurrected, Churned, Dormant)

## Extending the Semantic Model

### Adding New Metrics

Edit `semantic_models.yml`:

```yaml
user_lifecycle:
  measures:
    your_new_metric:
      expr: _.column_name.sum()
      description: "Description of your metric"
```

### Adding New Dimensions

Edit `semantic_models.yml`:

```yaml
user_lifecycle:
  dimensions:
    your_dimension:
      expr: _.column_name
      description: "Description of your dimension"
```

Then update `app.py` to include the new metric/dimension in the UI.

## Database Connection

The semantic layer connects to the DuckDB database at:
```
../user_lifecycle_states/evidence_dashboard/sources/user_analytics/data.duckdb
```

It reads from the `user_states_monthly` table in read-only mode.

## Example Queries

### MAU Over Time

```python
query = semantic_model.query(
    measures=["active_users"],
    time_grain="TIME_GRAIN_MONTH"
)
result = query.execute()
```

### Churn Rate by User State

```python
query = semantic_model.query(
    measures=["churn_rate"],
    dimensions=["user_state"],
    time_grain="TIME_GRAIN_MONTH"
)
result = query.execute()
```

### Pulse Ratio (Growth Health)

```python
query = semantic_model.query(
    measures=["pulse_ratio"],
    time_grain="TIME_GRAIN_MONTH",
    time_range={"start": "2022-03-01", "end": "2024-12-31"}
)
result = query.execute()
```

## Troubleshooting

### Connection Issues

If you see "Failed to connect to DuckDB":
- Verify the database file exists at the expected path
- Check that you have read permissions
- Ensure the `user_states_monthly` table exists

### Query Errors

If queries fail:
- Check the query details expander for generated SQL
- Verify column names match your database schema
- Review error messages for specific issues

## Future Enhancements

Potential improvements:
- Add more dimensions (user cohorts, segments)
- Add retention cohort analysis
- Add user journey metrics
- Export results to CSV
- Save and share query configurations
- Add more visualizations (cohort heatmaps, funnels)
