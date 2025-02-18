---
sidebar_position: 4
---

# API Reference

This document provides detailed information about the Brand Memory API endpoints.

## Authorization

The API uses two types of authorization:

1. **Public Endpoints** - No authorization required
   - Creating a tenant (`POST /tenant`)

2. **Admin Endpoints** - Requires admin authorization
   - Listing all tenants (`GET /tenant`)
   - Contact vinayak.sachdeva@codenation.co.in for admin access

3. **Tenant-Specific Endpoints** - Requires tenant API key
   - All other endpoints
   - Use the API key received during tenant creation as a Bearer token

### Using the API Key

For all tenant-specific endpoints, include the API key in the Authorization header:

```http
Authorization: Bearer <your-tenant-api-key>
```

## Base URL

All API endpoints are available at:
```
https://social-toolkit.ti.trilogy.com/
```

## Vector Store

Brand Memory uses vector storage to store and manage analyzed source content. By default, it uses an internal vector store, but you can optionally configure OpenSearch as your vector store backend.

The vector store is essential for:
- Storing embeddings of analyzed content
- Enabling semantic search capabilities
- Structuring brand-related information for quick retrieval
- Supporting natural language querying of brand content

When creating a tenant, you can optionally provide OpenSearch configuration details:

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

If OpenSearch configuration is not provided, the system will automatically use the default internal vector store.

## Model Context Protocol (MCP)

All API endpoints described below are also available as MCP tools. MCP ([Model Context Protocol](https://modelcontextprotocol.io/introduction)) is a standardized way to interact with AI models and manage their context. Using MCP allows for better interoperability and standardization across different AI services.

For detailed MCP documentation, see [mcp/README.md](https://github.com/trilogy-group/social-toolkit-site/blob/main/mcp/README.md).

**Note:** Currently MCP only supports local connections, so it doesn't support remote use of these tools.

### Setting up MCP

Clone the [repo](https://github.com/trilogy-group/social-toolkit-site) and follow this setup

#### Docker Setup
Build the MCP Docker image:
```bash
cd mcp && docker build -t social-toolkit/mcp .
```

#### Using the Inspector
You can use the MCP Inspector for debugging:
```bash
./inspector.sh
```

#### Integration with Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "social-toolkit": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "social-toolkit/mcp"
      ]
    }
  }
}
```

Now you can use the added mcp tools from server.py in claude desktop

### MCP Client Sample (Without Claude Desktop)
To try out the Social Toolkit using natural language locally:

1. Setup:
```bash
./setup.sh
```

2. Run:
```bash
./run.sh
```

This will run both MCP server and client, connected to each other. The terminal will prompt for natural language queries from the user, which then will be translated into MCP tool calls to answer the user query.

## Tenant Management

### Create Tenant
This is a public endpoint that doesn't require authorization.

```http
POST /tenant
Content-Type: application/json

{
    "name": "Your Company or Application",
    "description": "Your company or application description",
    "parent_tenant_id": "t-parent123",
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
    }
}
```

#### Request Fields

**Required Fields:**
- `name` (string): The name of your tenant. This should be a human-readable identifier for your organization or application.
- `description` (string): A brief description of your tenant's purpose or use case.

**Optional Fields:**
- `parent_tenant_id` (string): The ID of the parent tenant if this tenant is part of a hierarchical organization. Must be a valid tenant ID. The child tenant will have access to workers and prompts from parent tenant.

**Settings Object:**
- `vector_store_type` (string, optional): The type of vector store to use. Options:
  - `"opensearch"`: Use OpenSearch as the vector store
  - If not specified, uses the default internal vector store

- `vector_store_config` (object, required if vector_store_type is "opensearch"):
  - `host` (string): OpenSearch host URL
  - `port` (number): OpenSearch port number
  - `region` (string): AWS region for OpenSearch
  - `index_name` (string): Name of the OpenSearch index to use

- `anthropic_api_key` (string, required): Your Anthropic API key for Claude 3.5 Sonnet model access
- `openai_api_key` (string, required): Your OpenAI API key for text embeddings
- `google_ai_api_key` (string, required): Your Google AI API key for Gemini 1.5 Pro model access

**Concurrency Limits Object (optional):**
Controls the maximum number of parallel operations per content type. If not specified, uses system defaults.
- `TEXT` (number): Maximum parallel text operations (default: 10)
- `IMAGE` (number): Maximum parallel image operations (default: 5)
- `VIDEO` (number): Maximum parallel video operations (default: 3)
- `AUDIO` (number): Maximum parallel audio operations (default: 3)

#### Response Fields

- `tenant_id` (string): Unique identifier for the tenant in the format "t-*"
- `api_key` (string): API key for authenticating tenant-specific requests in the format "sk-tenant-*"
- `name` (string): The tenant name as provided in the request
- `description` (string): The tenant description as provided in the request
- `parent_tenant_id` (string, optional): The ID of the parent tenant if specified
- `settings` (object): The tenant settings as configured in the request
- `concurrency_limits` (object): The configured or default concurrency limits

#### Example Response
```json
{
    "tenant_id": "t-123456",
    "api_key": "sk-tenant-abcdef123456",
    "name": "Your Company or Application",
    "description": "Your company or application description",
    "parent_tenant_id": "t-parent123",
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
    }
}
```

### Get Tenant
Requires tenant authorization.

```http
GET /tenant/{tenant_id}
Authorization: Bearer <tenant-api-key>
```

Returns the same fields as the tenant creation response.

### List Tenants
Requires admin authorization. Contact vinayak.sachdeva@codenation.co.in for admin access.

```http
GET /tenant
Authorization: Bearer <admin-api-key>
```

Returns an array of tenant objects, each containing the same fields as the tenant creation response.

### Update Tenant
Requires tenant authorization.

```http
PUT /tenant/{tenant_id}
Authorization: Bearer <tenant-api-key>
Content-Type: application/json

{
    "name": "Updated Name",             // Optional: New tenant name
    "description": "Updated description", // Optional: New description
    "settings": {                       // Optional: Updated settings
        "anthropic_api_key": "new-key",
        "openai_api_key": "new-key",
        "google_ai_api_key": "new-key",
        "vector_store_type": "opensearch",
        "vector_store_config": {
            "host": "new-host",
            "port": 443,
            "region": "new-region",
            "index_name": "new-index"
        }
    },
    "concurrency_limits": {            // Optional: Updated limits
        "TEXT": 20,
        "IMAGE": 10,
        "VIDEO": 5,
        "AUDIO": 5
    }
}
```

All fields in the update request are optional. Only the fields that need to be updated should be included.
The response will contain the complete updated tenant object with all fields.

### Delete Tenant
Requires tenant authorization.

```http
DELETE /tenant/{tenant_id}
Authorization: Bearer <tenant-api-key>
```

Returns a 204 No Content response on successful deletion.

**Note**: Deleting a tenant will also delete all associated brands, sources, prompts, workers, and generations. This action cannot be undone.

## Brand Management

### Create Brand
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/brand
Authorization: Bearer <tenant-api-key>
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
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand/{brand_id}
Authorization: Bearer <tenant-api-key>
```

### List Brands
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand
Authorization: Bearer <tenant-api-key>
```

### Update Brand
Requires tenant authorization.

```http
PUT /tenant/{tenant_id}/brand/{brand_id}
Authorization: Bearer <tenant-api-key>
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
Requires tenant authorization.

```http
DELETE /tenant/{tenant_id}/brand/{brand_id}
Authorization: Bearer <tenant-api-key>
```

### Trigger Brand Compass
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/brand/{brand_id}/compass/trigger
Authorization: Bearer <tenant-api-key>
```

### Get Brand Compass
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/compass
Authorization: Bearer <tenant-api-key>
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
Requires tenant authorization. Accepts multipart/form-data requests.

```http
POST /tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <tenant-api-key>
Content-Type: multipart/form-data

# Form Fields:
name: "Sample Content"
description: "Content description"
source_type: "SAMPLE" # SAMPLE, GUIDELINES, or KNOWLEDGE

# Content can be provided in one of these three ways:
1. file: <file upload>
2. url: "https://example.com/content"
3. text: "Direct text content..."
```

Important notes:
- Only SAMPLE source type supports non-text content (IMAGE, AUDIO, VIDEO)
- GUIDELINES and KNOWLEDGE sources must be TEXT content type
- Content type is automatically detected from the uploaded file or URL
- If no content is provided, the request will be rejected
- For text content:
  - Uploaded files should have text/* content type
  - URL should return text/* content type
  - Direct text input is always treated as TEXT content type

Response (201 Created):
```json
{
    "source_id": "src-123456",
    "name": "Sample Content",
    "description": "Content description",
    "source_type": "SAMPLE",
    "content_type": "TEXT", // Automatically detected: TEXT, IMAGE, AUDIO, or VIDEO
    "status": "PROCESSING", // or "COMPLETED" if no analysis prompts exist
    "created_at": "2024-01-08T12:00:00Z",
    "updated_at": "2024-01-08T12:00:00Z",
    "location": "s3://bucket-name/sources/tenant=123/brand=456/uuid_filename"
}
```

### Get Source
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/source/{source_id}
Authorization: Bearer <tenant-api-key>
```

### List Sources
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <tenant-api-key>
```

Query parameters:
- `source_type`: Filter by source type
- `status`: Filter by status

### Delete Source
Requires tenant authorization.

```http
DELETE /tenant/{tenant_id}/brand/{brand_id}/source/{source_id}
Authorization: Bearer <tenant-api-key>
```

### Reprocess Source
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/brand/{brand_id}/source/{source_id}/reprocess
Authorization: Bearer <tenant-api-key>
```

## Prompt Management

### Create Prompt
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/prompt
Authorization: Bearer <tenant-api-key>
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
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/prompt/{prompt_id}
Authorization: Bearer <tenant-api-key>
```

### List Prompts
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/prompt
Authorization: Bearer <tenant-api-key>
```

Query parameters:
- `content_type`: Filter by content type

### Update Prompt
Requires tenant authorization.

```http
PUT /tenant/{tenant_id}/prompt/{prompt_id}
Authorization: Bearer <tenant-api-key>
Content-Type: application/json

{
    "name": "Updated Name",
    "description": "Updated description",
    "prompt_text": "Updated prompt text"
}
```

### Delete Prompt
Requires tenant authorization.

```http
DELETE /tenant/{tenant_id}/prompt/{prompt_id}
Authorization: Bearer <tenant-api-key>
```

## Worker Management

### Create Worker
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/worker
Authorization: Bearer <tenant-api-key>
Content-Type: application/json

{
    "name": "Social Media Generator",
    "description": "Generate social media posts",
    "output_type": "TEXT",           // TEXT or MULTI_MODAL (multi modal coming soon)
    "prompt": "Create a social media post that matches our brand voice"
}
```

Important notes:
- TEXT workers use Claude 3.5 Sonnet and can only generate text content
- MULTI_MODAL workers use Gemini 1.5 Pro and can generate images and text content

### Get Worker
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/worker/{worker_id}
Authorization: Bearer <tenant-api-key>
```

### List Workers
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/worker
Authorization: Bearer <tenant-api-key>
```

Query parameters:
- `output_type`: Filter by output type

### Update Worker
Requires tenant authorization.

```http
PUT /tenant/{tenant_id}/worker/{worker_id}
Authorization: Bearer <tenant-api-key>
Content-Type: application/json

{
    "name": "Updated Name",
    "description": "Updated description",
    "prompt": "Updated prompt"
}
```

### Delete Worker
Requires tenant authorization.

```http
DELETE /tenant/{tenant_id}/worker/{worker_id}
Authorization: Bearer <tenant-api-key>
```

## Generation Management

### Create Generation
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation
Authorization: Bearer <tenant-api-key>
Content-Type: application/json

{
    "context": "Optional context for generation",
    "source_ids": ["src-123", "src-456"],  // Optional: Array of source IDs to include in generation context
    "use_source_context": true             // Optional: Whether to use source analysis (default: true)
    "metadata": {                          // Optional: Metadata about the generation, this can be used to store any information you want to store along with the generation
        "key_1": "value_1",
        "key_2": "value_2"
    }
}
```

Response for create generation request:
```json
{
    "tenant_id": "your-tenant-id",
    "result": null,
    "worker_id": "your-worker-id",
    "output_type": "your-output-type",
    "status": "PROCESSING",                              // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "prompt": "your-worker-prompt",
    "source_ids": [],
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "context": "your-context",
    "generation_id": "your-generation-id",               // generation id
    "current_version_id": "latest-version-id",           // version id
    "updated_at": "2025-02-14T15:49:44.120298+00:00",
    "use_source_context": true,
    "brand_id": "your-brand-id",
    "metadata": {                                        // if included in the create generation request, else null
        "key_1": "value_1",
        "key_2": "value_2"
    }
}
```

### Get Generation
Requires tenant authorization.
Note that this will fetch the latest version of the generation.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}
Authorization: Bearer <tenant-api-key>
```

Response for get generation request:
```json
{
    "tenant_id": "your-tenant-id",
    "result": null, 
    "worker_id": "your-worker-id",
    "output_type": "your-output-type",
    "status": "PROCESSING",                              // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "prompt": "your-worker-prompt",
    "source_ids": [],
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "context": "your-context",
    "generation_id": "your-generation-id",               // generation id
    "current_version_id": "latest-version-id",           // version id
    "updated_at": "2025-02-14T15:49:44.120298+00:00",
    "use_source_context": true,
    "brand_id": "your-brand-id"
    "metadata": {                                        // if included in the create generation request, else null
        "key_1": "value_1",
        "key_2": "value_2"
    }
}
```

### Get Generation Version
You can fetch the generation version, using generation id and current version id from the response of the create generation request.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}/version/{version_id}
Authorization: Bearer <tenant-api-key>
```

Response for get generation version request:
```json
{
    "result": null,
    "feedback": null,
    "previous_version_id": null,
    "version_id": "your-version-id",
    "status": "PROCESSING",                               // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "generation_id": "your-generation-id",
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "output_type": "your-output-type"
}
```

### List Generations
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation
Authorization: Bearer <tenant-api-key>
```

### List Generation Versions
Requires tenant authorization.

```http
GET /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}/version
Authorization: Bearer <tenant-api-key>
```

### Submit Feedback for Generation
Requires tenant authorization.

```http
POST /tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}/version/{version_id}/feedback
Authorization: Bearer <tenant-api-key>
Content-Type: application/json

{
    "feedback": "Your feedback about the resonse, to improve the next generation version output"
}
```

Response for submit feedback for generation request:
```json
{
    "result": null,
    "feedback": "Your feedback about the resonse",        // Feedback
    "previous_version_id": "previous-version-id",         // Previous version id
    "version_id": "your-version-id",                      // New version id
    "status": "PROCESSING",                               // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "generation_id": "your-generation-id",                // generation id
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "output_type": "your-output-type"
}
```

## API Configuration

Brand Memory uses different AI providers for specific tasks:

### Model Usage

- **Text Analysis & Generation**: Uses Anthropic's Claude 3.5 Sonnet model (`claude-3-5-sonnet-20241022`)
  - Handles all text-based operations
  - Requires Anthropic API key

- **Text Embeddings**: Uses OpenAI's embedding model (`text-embedding-3-large`)
  - Creates vector representations of text content
  - Used for semantic search and content organization
  - Requires OpenAI API key

- **Multi-modal Content**: Uses Google's Gemini model (`gemini-1.5-pro-001`)
  - Processes images, audio, and video content
  - Handles analysis of non-text media
  - Requires Google AI API key

### Concurrency Management

Each tenant can optionally configure concurrency limits per content type. If not specified, the system will use default values:

```json
"concurrency_limits": {
    "TEXT": 10,    // Maximum parallel text operations
    "IMAGE": 5,    // Maximum parallel image operations
    "VIDEO": 3,    // Maximum parallel video operations
    "AUDIO": 3     // Maximum parallel audio operations
}
```

These limits help:
- Manage API rate limits across providers
- Control resource utilization
- Ensure stable system performance
- Prevent overloading of processing queues

If not specified, the system will use default concurrency values that are suitable for most use cases.

## Brand Compass

The Brand Compass is a comprehensive brand analysis report that provides a holistic understanding of your brand by analyzing all brand-related content. It uses specialized workers to analyze different aspects of your brand content and synthesize the findings.

### Brand Compass Workers

Brand Compass workers are specialized analysis workers that need to be created and configured for your tenant. These workers analyze different aspects of your brand:

1. First, create the necessary workers using the worker endpoints
2. Then, associate these workers with your tenant by updating the `brand_compass_worker_ids` field

Example worker configuration:
```json
{
    "brand_compass_worker_ids": [
        "worker-tone-analysis-123",
        "worker-style-patterns-456",
        "worker-messaging-789"
    ]
}
```

### Brand Compass Status

The Brand Compass process has several states:
- `NOT_STARTED`: Initial state
- `PROCESSING`: Analysis in progress
- `COMPLETED`: Analysis finished successfully
- `FAILED`: Analysis encountered an error

### Trigger Brand Compass Analysis

Initiates a new Brand Compass analysis:

```http
POST /tenant/{tenant_id}/brand/{brand_id}/compass/trigger
Authorization: Bearer <tenant-api-key>
```

Response:
```json
{
    "status": "PROCESSING",
    "triggered_at": "2025-02-18T10:22:27.415498+00:00",
    "generation_version_tuples": [
        {
            "generation_id": "your-generation-id-1",
            "version_id": "your-version-id-1"
        },
        {
            "generation_id": "your-generation-id-2",
            "version_id": "your-version-id-2"
        }
        // ... more generation version tuples
    ]
}
```

### Get Brand Compass Status

Retrieve the current status and results of the Brand Compass analysis:

```http
GET /tenant/{tenant_id}/brand/{brand_id}/compass
Authorization: Bearer <tenant-api-key>
```

Response:
```json
{
    "status": "PROCESSING",
    "generations": [
        {
            "status": "COMPLETED",
            "generation_id": "your-generation-id-1",
            "version_id": "your-version-id-1",
            "result": {
                "status": "success",                            // success, error
                "content": "your-brand-compass-content"
            },
            "created_at": "2025-02-18T10:22:31.744188+00:00",
            "feedback": null,
            "previous_version_id": null,
            "output_type": "TEXT"
        },
        {
            "status": "PROCESSING",
            "generation_id": "your-generation-id-2",
            "version_id": "your-version-id-2",
            "result": null,
            "created_at": "2025-02-18T10:22:31.744188+00:00",
            "feedback": null,
            "previous_version_id": null,
            "output_type": "TEXT"
        }
        // ... other worker generations
    ],
    "triggered_at": "2024-01-08T12:00:00Z",
    "completed_at": null,
    "progress": {                                               // only returned if the brand compass is under PROCESSING state
        "total_workers": 5,
        "completed_workers": 2,
        "percent_complete": 40
    }
}
```

