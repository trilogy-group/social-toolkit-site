---
sidebar_position: 4
---

# API Reference

This document provides detailed information about the Brand Memory API endpoints.

## Base URL

All API endpoints are available at:
```
https://social-toolkit.ti.trilogy.com/
```

## Vector Store

Brand Memory uses OpenSearch as its vector store database to store and manage analyzed source content. The vector store is essential for:
- Storing embeddings of analyzed content
- Enabling semantic search capabilities
- Structuring brand-related information for quick retrieval
- Supporting natural language querying of brand content

Currently, only OpenSearch is supported as the vector store backend. When creating a tenant, you must provide OpenSearch configuration details:

```http
POST /tenant
Content-Type: application/json

{
    "name": "Your Company",
    "description": "Your company description",
    "settings": {
        "vector_store_type": "opensearch",
        "vector_store_config": {
            "host": "your-opensearch-host",
            "port": 443,
            "region": "us-east-1",
            "index_name": "your-index"
        },
        "anthropic_api_key": "your-anthropic-key",
        "openai_api_key": "your-openai-key",
        "google_ai_api_key": "your-google-ai-key"
    },
    "concurrency_limits": {
        "TEXT": 10,
        "IMAGE": 5,
        "VIDEO": 3,
        "AUDIO": 3
    },
}
```

The vector store automatically indexes all source content analysis, making it available for semantic querying and retrieval through your application.

## Model Context Protocol (MCP)

All API endpoints described below are also available as [MCP](https://github.com/trilogy-group/social-toolkit/tree/main/mcp) operations. MCP ([Model Context Protocol](https://modelcontextprotocol.io/introduction)) is a standardized way to interact with AI models and manage their context. Using MCP allows for better interoperability and standardization across different AI services.

**Note:** Currently MCP only supports local connections, so it doesn't support remote use of these tools.

### Benefits of MCP

- **Standardized Interactions**: MCP provides a consistent interface for working with different AI models and services
- **Context Management**: Better handling of context windows and model memory
- **Interoperability**: Seamlessly switch between different AI providers while maintaining the same interface
- **Enhanced Control**: Fine-grained control over model parameters and context handling

### MCP Operations

All API endpoints can be accessed through MCP operations. For example:

```python
# Creating a tenant via MCP
tenant = session.call_tool("create_tenant", {
    "name": "Social Savvy",
    "description": "AI Podcast Studio",
    "settings": {
        "vector_store_type": "opensearch",
        # ... other settings ...
    }
})
```

[Example Client](https://github.com/trilogy-group/social-toolkit/tree/main/mcp/client.py)

### Setting up MCP

To use the MCP client:

1. Run the setup script:
```bash
./setup.sh
```

2. Start the MCP client:
```bash
./run.sh
```

## Tenant Management

### Create Tenant

```http
POST /tenant
Content-Type: application/json

{
    "name": "Your Company or Application",
    "description": "Your company or application description",
    "settings": {
        "vector_store_type": "opensearch",
        "vector_store_config": {
            "host": "your-opensearch-host",
            "port": 443,
            "region": "us-east-1",
            "index_name": "your-index"
        },
        "anthropic_api_key": "your-anthropic-key",
        "openai_api_key": "your-openai-key",
        "google_ai_api_key": "your-google-ai-key"
    },
    "concurrency_limits": {
        "TEXT": 10,
        "IMAGE": 5,
        "VIDEO": 3,
        "AUDIO": 3
    },
}
```

### Get Tenant

```http
GET /tenant/{tenant_id}
```

### List Tenants

```http
GET /tenant
```

### Update Tenant

```http
PUT /tenant/{tenant_id}
Content-Type: application/json

{
    "name": "Updated Name",
    "description": "Updated description",
    "settings": {
        // Updated settings
    }
}
```

### Delete Tenant

```http
DELETE /tenant/{tenant_id}
```

## Brand Management

### Create Brand

```http
POST /tenant/{tenant_id}/brand
Content-Type: application/json

{
    "name": "Your Brand",
    "description": "Your brand description",
    "settings": {
        // Optional brand-specific settings
    }
}
```

### Get Brand

```http
GET /tenant/{tenant_id}/brand/{brand_id}
```

### List Brands

```http
GET /tenant/{tenant_id}/brand
```

### Update Brand

```http
PUT /tenant/{tenant_id}/brand/{brand_id}
Content-Type: application/json

{
    "name": "Updated Brand",
    "description": "Updated description",
    "settings": {
        // Updated settings
    }
}
```

### Delete Brand

```http
DELETE /tenant/{tenant_id}/brand/{brand_id}
```

### Trigger Brand Compass

```http
POST /tenant/{tenant_id}/brand/{brand_id}/compass/trigger
```

### Get Brand Compass

```http
GET /tenant/{tenant_id}/brand/{brand_id}/compass
```

Response:
```json
{
    "status": "PROCESSING",
    "generations": [...],
    "triggered_at": "2024-01-08T12:00:00Z",
    "completed_at": null,
    "progress": {
        "total_workers": 5,
        "completed_workers": 2,
        "percent_complete": 40
    }
}
```

## Source Management

### Add Source

```http
POST /tenant/{tenant_id}/brand/{brand_id}/source
Content-Type: multipart/form-data

{
    "name": "Sample Content",
    "description": "Content description",
    "source_type": "SAMPLE", // SAMPLE, GUIDELINES, or KNOWLEDGE
    "content_type": "TEXT", // TEXT, IMAGE, AUDIO, or VIDEO
    "file": <file-data>
    // OR
    "url": "https://example.com/content",
    // OR
    "text": "Direct text content..."
}
```

### Get Source

```http
GET /tenant/{tenant_id}/brand/{brand_id}/source/{source_id}
```

### List Sources

```http
GET /tenant/{tenant_id}/brand/{brand_id}/source
```

Query parameters:
- `source_type`: Filter by source type
- `status`: Filter by status

### Delete Source

```http
DELETE /tenant/{tenant_id}/brand/{brand_id}/source/{source_id}
```

### Reprocess Source

```http
POST /tenant/{tenant_id}/brand/{brand_id}/source/{source_id}/reprocess
```

## Prompt Management

### Create Prompt

```http
POST /tenant/{tenant_id}/prompt
Content-Type: application/json

{
    "name": "Voice Analysis",
    "description": "Analyze content tone and voice",
    "content_type": "TEXT",
    "prompt_text": "Analyze this content and describe how it reflects our brand voice",
    "settings": {
        // Optional prompt-specific settings
    }
}
```

### Get Prompt

```http
GET /tenant/{tenant_id}/prompt/{prompt_id}
```

### List Prompts

```http
GET /tenant/{tenant_id}/prompt
```

Query parameters:
- `content_type`: Filter by content type

### Update Prompt

```http
PUT /tenant/{tenant_id}/prompt/{prompt_id}
Content-Type: application/json

{
    "name": "Updated Name",
    "description": "Updated description",
    "prompt_text": "Updated prompt text"
}
```

### Delete Prompt

```http
DELETE /tenant/{tenant_id}/prompt/{prompt_id}
```

## Worker Management

### Create Worker

```http
POST /tenant/{tenant_id}/worker
Content-Type: application/json

{
    "name": "Social Media Generator",
    "description": "Generate social media posts",
    "output_type": "TEXT",
    "prompt": "Create a social media post that matches our brand voice"
}
```

### Get Worker

```http
GET /tenant/{tenant_id}/worker/{worker_id}
```

### List Workers

```http
GET /tenant/{tenant_id}/worker
```

Query parameters:
- `output_type`: Filter by output type

### Update Worker

```http
PUT /tenant/{tenant_id}/worker/{worker_id}
Content-Type: application/json

{
    "name": "Updated Name",
    "description": "Updated description",
    "prompt": "Updated prompt"
}
```

### Delete Worker

```http
DELETE /tenant/{tenant_id}/worker/{worker_id}
```

## Generation Management

### Create Generation

```http
POST /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation
Content-Type: application/json

{
    "context": "Optional context for generation"
}
```

### Get Generation

```http
GET /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}
```

### List Generations

```http
GET /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation
```
