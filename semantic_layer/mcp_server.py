#!/usr/bin/env python3
"""MCP Server for Boring Semantic Layer - User Lifecycle Metrics."""

import os
import sys


def create_mcp_server():
    """Create and configure the MCP server with user lifecycle semantic model."""
    from boring_semantic_layer.mcp import MCPSemanticModel
    from semantic_model import create_user_lifecycle_semantic_model

    # Load semantic model
    user_lifecycle_model = create_user_lifecycle_semantic_model()

    # Create MCP server with the model
    mcp_server = MCPSemanticModel(
        models={
            "user_lifecycle": user_lifecycle_model,
        },
        name="User Lifecycle Semantic Layer"
    )

    return mcp_server


if __name__ == "__main__":
    server = create_mcp_server()
    server.run()
