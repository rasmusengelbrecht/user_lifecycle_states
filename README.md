# User Lifecycle Analytics Dashboard

An end-to-end user lifecycle analytics platform featuring synthetic data generation, advanced user state modeling, and interactive dashboards for understanding user behavior patterns.

## 🏗️ Architecture

- **Python**: Generates synthetic user and transaction data
- **DuckDB**: Local analytical database for data storage  
- **dbt**: Transforms raw data into staging and mart layers
- **Evidence.dev**: Interactive dashboards and visualizations
- **UV**: Python package management and virtual environments

## 📁 Project Structure

```
user_lifecycle_states/
├── pyproject.toml              # UV project configuration
├── run.sh                      # Pipeline execution script
├── user_analytics/
│   └── run.py                  # Main orchestration script
├── data_generation/
│   └── generate_data.py        # Synthetic user behavior data generation
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── data.duckdb             # DuckDB database file
│   └── models/
│       ├── staging/            # Clean source data (stg_users, stg_transactions)
│       └── marts/              # User dimensions, transaction facts, lifecycle states
└── evidence_dashboard/
    ├── package.json
    ├── pages/                  # Interactive dashboard pages
    └── sources/                # SQL queries and data connections
```

## 🚀 Quick Start

### Prerequisites

- [UV](https://docs.astral.sh/uv/) installed
- [Node.js](https://nodejs.org/) (for Evidence.dev)

### Run Everything

```bash
# Clone and navigate to project
cd user_lifecycle_states

# Run the complete pipeline (generate → transform → dashboard)
./run.sh
```

This single command will:
1. Install all dependencies
2. Generate synthetic user and transaction data
3. Transform data using dbt
4. Start the Evidence dashboard at http://localhost:3000

### Individual Steps

You can also run individual parts of the pipeline:

```bash
# Setup only
./run.sh --setup

# Generate data only
./run.sh --generate

# Transform data only  
./run.sh --transform

# Start dashboard only
./run.sh --dashboard

# Skip setup (if already done)
./run.sh --skip-setup
```

## 📊 Data Models

### Staging Layer
- `stg_users`: Clean user data with signup dates and basic attributes
- `stg_transactions`: Clean transaction data with user relationships

### Marts Layer
- `dim_users`: User dimension with lifecycle metrics and behavioral attributes
- `fct_transactions`: Transaction facts with user context and timing analysis
- `mart_user_state_monthly`: **Advanced user lifecycle states** (New, Retained, Churned, Reactivated, Resurrected, Dormant, Never Activated) by month

## 🎯 Dashboard Features

The Evidence dashboard provides comprehensive user lifecycle analytics:

### 📈 Key Visualizations
- **Monthly Active Users (MAU)**: Bar chart with percentage of total users active each month
- **Monthly User Dynamics**: Stacked bar chart showing user state transitions (New, Retained, Reactivated, Resurrected vs. Churned)
- **Monthly Churn Rate**: Line chart showing `Churned / (Churned + Retained)` percentage
- **Pulse Ratio**: Health metric showing `(New + Reactivated + Resurrected) / Churned`

### 🎨 Advanced Features
- **Dual-axis charts** with bars and lines for comprehensive metrics
- **Negative visualization** for churned users (red, below zero)
- **Custom color palettes** for intuitive user state understanding
- **Interactive data tables** for detailed exploration of underlying data

### 📊 User Lifecycle States
- **New**: First-time active users
- **Retained**: Users active in consecutive months  
- **Churned**: Users who became inactive after being active
- **Reactivated**: Users who returned after 1 month of inactivity
- **Resurrected**: Users who returned after 2+ months of inactivity
- **Dormant**: Users who remain inactive after churning
- **Never Activated**: Users who never had any transactions

## 🔧 Development

### Manual Data Generation
```bash
cd data_generation
uv run python generate_data.py
```

### Manual dbt Runs
```bash
cd dbt_project
uv run dbt run
uv run dbt test
```

### Evidence Development
```bash
cd evidence_dashboard
npm run dev
```

## 🧪 Testing

```bash
# Test dbt models
cd dbt_project
uv run dbt test

# Check data quality
uv run dbt run --full-refresh
```

## 📝 Configuration

### Data Generation
- Generates **1000 synthetic users** with realistic lifecycle behaviors:
  - **Never Activated** (10%): Users who never transact
  - **Retained** (40%): Users who remain consistently active
  - **Churned** (20%): Users who stop transacting after some activity
  - **Sporadic** (20%): Users with irregular transaction patterns
  - **Resurrected** (10%): Users who return after periods of inactivity
- Creates **3,952 transactions** spanning 2022 with proper temporal constraints
- Ensures **data integrity**: All transactions occur on/after user signup dates
- Output: Raw data in DuckDB `raw_data` schema

### dbt Configuration  
- Database: DuckDB at `data.duckdb`
- Target: `dev` environment
- Materializations:
  - Staging: `view`
  - Marts: `table`

### Evidence Configuration
- Database: DuckDB connection to transformed data
- **Custom chart height**: 280px globally configured
- **Advanced visualizations**: Combo charts, dual-axis, custom color palettes
- **Interactive features**: Hover details, data tables, responsive design

## 🛠️ Troubleshooting

### Common Issues

1. **UV not found**: Install UV using the instructions at https://docs.astral.sh/uv/
2. **Node.js missing**: Install Node.js from https://nodejs.org/
3. **Database locked**: Stop any running processes and retry
4. **API connection issues**: Check internet connectivity

### Clean Restart

```bash
# Remove database and start fresh
rm -f dbt_project/data.duckdb
./run.sh
```

## 🎨 Customization

### Data Generation
- **User behaviors**: Edit `data_generation/generate_data.py` to modify behavioral patterns and probabilities
- **Data volume**: Adjust `n_users` parameter to generate more/fewer synthetic users
- **Time period**: Modify `start_date` and `end_date` for different analysis windows

### Analytics Models
- **New lifecycle states**: Extend `mart_user_state_monthly.sql` with custom business logic
- **Additional metrics**: Create new dbt models in `dbt_project/models/marts/`
- **Custom aggregations**: Build specialized views for specific analysis needs

### Dashboard Customization
- **New visualizations**: Add charts to `evidence_dashboard/pages/index.md`
- **Custom color schemes**: Modify color palettes in chart configurations
- **Chart types**: Experiment with different Evidence chart components (ScatterPlot, Heatmap, etc.)
- **Interactive filters**: Add date ranges, user segments, or other filtering capabilities

## 📚 Learn More

- [dbt Documentation](https://docs.getdbt.com/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Evidence Documentation](https://evidence.dev/docs)
- [UV Documentation](https://docs.astral.sh/uv/)
- [pandas Documentation](https://pandas.pydata.org/docs/)