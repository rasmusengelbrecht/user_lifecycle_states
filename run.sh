#!/bin/bash
# Simple wrapper script for the main orchestrator

# Check if user wants to run the semantic layer app
if [ "$1" = "semantic" ]; then
    echo "📊 Starting Semantic Layer App..."
    cd semantic_layer && uv run streamlit run app.py
    exit 0
fi

echo "🏗️ Starting User Analytics Pipeline..."
uv run python user_analytics/run.py "$@"