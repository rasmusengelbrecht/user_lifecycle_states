#!/bin/bash
# Simple wrapper script for the main orchestrator

echo "🏗️ Starting User Analytics Pipeline..."
uv run python user_analytics/run.py "$@"