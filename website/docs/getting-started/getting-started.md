---
sidebar_position: 2
---

# Getting Started

This guide will help you get started with Social Toolkit. We'll walk through the process of setting up your tenant, creating your first brand, and using the system for content analysis and generation.

## Prerequisites

Before you begin, you'll need:

1. **API Keys**:
   - **Anthropic API key**: Used for all text-based operations (analysis and generation) using the Claude 3.5 Sonnet model
   - **OpenAI API key**: Used for creating text embeddings with text-embedding-3-large model
   - **Google AI API key**: Used for analysing and generating non-text content (images, audio, video) using Gemini 1.5 Pro

2. **OpenSearch Instance (Optional)**:
   If you want to use your own OpenSearch instance instead of the default SDK's vector store:
   - Host URL
   - Port
   - Region
   - Index name

## Step 1: Create Your Tenant

Your first step is to create a tenant. A tenant represents your organization or application and contains all your brands and configurations. This is a public endpoint that doesn't require authorization.

Basic configuration:
```http
POST https://social-toolkit.ti.trilogy.com/tenant
Content-Type: application/json

{
    "name": "Your application name",
    "description": "Your application description",
    "settings": {
        "anthropic_api_key": "your-anthropic-key",
        "openai_api_key": "your-openai-key",
        "google_ai_api_key": "your-google-ai-key"
    }
}
```

The response will include your tenant ID and API key:
```json
{
    "tenant_id": "t-123456",
    "api_key": "sk-tenant-abcdef123456",
    // ... other response fields ...
}
```

Save both the `tenant_id` and `api_key` - you'll need them for all subsequent requests.

## Authentication for Subsequent Requests

For all following API calls, you must include your tenant API key in the Authorization header:

```http
Authorization: Bearer sk-tenant-abcdef123456
```

## Step 2: Create Analysis Prompts

Analysis prompts are configured at the tenant level and define how content will be analyzed. Create prompts for different aspects of your content and for different content types:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/prompt
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Voice Analysis",
    "description": "Analyze content tone and voice",
    "content_type": "TEXT",
    "prompt_text": "Analyze this content and describe how it reflects our brand voice. Consider tone, style, and messaging."
}
```

## Step 3: Set Up Brand Compass Workers

Before creating your brand, you'll need to set up specialized workers for the Brand Compass analysis. These workers will analyze different aspects of your brand content, for example:

1. **Create Voice Analysis Worker**:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/worker
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Voice Analysis",
    "description": "Analyzes brand voice characteristics",
    "output_type": "TEXT",
    "prompt": "Analyze the content for voice characteristics including tone, style, and personality. Consider formality, emotion, and distinctive patterns."
}
```

2. **Create Style Pattern Worker**:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/worker
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Style Pattern Analysis",
    "description": "Identifies consistent style patterns",
    "output_type": "TEXT",
    "prompt": "Identify recurring style patterns in the content including word choice, sentence structure, and formatting conventions."
}
```

3. **Create Messaging Analysis Worker**:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/worker
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Messaging Analysis",
    "description": "Analyzes key messages and themes",
    "output_type": "TEXT",
    "prompt": "Identify core messages, themes, and value propositions present in the content."
}
```

**Update Tenant with Brand Compass Workers**:
```http
PUT https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "brand_compass_worker_ids": [
        "worker-id-1",
        "worker-id-2",
        "worker-id-3"
    ]
}
```

## Step 4: Create Generation Workers

After setting up Brand Compass workers, create workers for content generation. The system supports two types of workers:

1. **Text Workers** - Generate text-based content:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/worker
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Blog Post Generator",
    "description": "Generates blog post content",
    "type": "TEXT",
    "output_type": "TEXT",
    "prompt": "Create a blog post that aligns with our brand guidelines, maintaining our established voice and expertise level."
}
```

2. **Multi-Modal Workers** - Generate text and image content (coming soon):
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/worker
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Social Image Generator",
    "description": "Generates social media images",
    "output_type": "MULTI_MODAL",
    "prompt": "Create an engaging social media image that reflects our brand style and visual identity."
}
```

## Step 5: Create Your Brand

Next, create a brand under your tenant. A brand will use your tenant's prompts and workers to analyze and generate content specific to that brand.

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Your Brand",
    "description": "Your brand description"
}
```

Save the `brand_id` from the response.

## Step 6: Add Brand Content

Brand Memory uses three types of sources to understand and generate content for your brand:

### 1. Sample Content

Add examples of your brand's content:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: multipart/form-data

# Form Fields:
name: "Blog Post Sample"
description: "Example of our blog writing style"
source_type: "SAMPLE"
text: "Your sample content here..."
```

You can also upload files or provide URLs:
```http
# Using file upload
file: <file upload>

# Or using URL
url: "https://example.com/content"
```

### 2. Brand Knowledge

Add factual information about your brand:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: multipart/form-data

# Form Fields:
name: "Company History"
description: "Our company background"
source_type: "KNOWLEDGE"
text: "Company history and facts..."
```

### 3. Brand Guidelines

Add your brand rules and standards:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: multipart/form-data

# Form Fields:
name: "Voice Guidelines"
description: "Brand voice rules"
source_type: "GUIDELINES"
text: "Our brand voice guidelines..."
```

## Step 7: Analyze Content

The content analysis process is asynchronous:

1. Submit content for analysis:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: multipart/form-data

# Form Fields:
name: "Content Sample"
description: "Content to analyze"
source_type: "SAMPLE"
text: "Content to analyze..."
```

The response will include a `source_id` that you'll need for checking the analysis status.

2. Poll for analysis results:
```http
GET https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source/{source_id}
Authorization: Bearer <your-tenant-api-key>
```

## Step 8: Run Brand Compass Analysis

After adding your brand content, trigger the Brand Compass analysis to get a comprehensive understanding of your brand:

1. **Trigger the Analysis**:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/compass/trigger
Authorization: Bearer <your-tenant-api-key>
```

2. **Monitor Progress**:
```http
GET https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/compass
Authorization: Bearer <your-tenant-api-key>
```

The response will show the analysis progress:
```json
{
    "status": "PROCESSING",
    "generations": [
        {
            "generation_id": "generation-id-123",
            "version_id": "version-id-123",
            "previous_version_id": null,
            "output_type": "the-output-type",
            "status": "COMPLETED",
            "result": {
                "status": "success",
                "content": "...",
            },
            "created_at": "2025-02-14T15:49:44.120298+00:00",
            "feedback": null
        },
        {
            "generation_id": "generation-id-456",
            "version_id": "version-id-456",
            "previous_version_id": null,
            "output_type": "TEXT",
            "status": "PROCESSING",
            "result": null,
            "feedback": null,
            "created_at": "2025-02-14T15:49:44.120298+00:00",
        }
    ],
    "triggered_at": "2024-01-08T12:00:00Z",
    "completed_at": null,
    "progress": {
        "total_workers": 5,
        "completed_workers": 2,
        "percent_complete": 40
    }
}
```

Once completed, the Brand Compass will provide insights about your brand's:
- Voice and tone characteristics
- Style patterns and conventions
- Key messages and themes
- Content consistency
- Areas for improvement

## Step 9: Generate Content

1. Submit a generation request:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "context": "Optional context for the generation",
    "source_ids": ["src-123", "src-456"],  // Optional: Specific sources to include in generation context
    "use_source_context": true             // Optional: Whether to use source analysis (default: true)
}
```

The generation request accepts these parameters:
- `context`: Optional context to guide the generation
- `source_ids`: Optional array of source IDs that should be included in full during generation
- `use_source_context`: Optional boolean (default: true) that determines whether to use source analysis for generation

2. Check generation status:

The response will include generation id and version id:
```json
{
    "tenant_id": "your-tenant-id",
    "result": null,
    "worker_id": "your-worker-id",
    "output_type": "your-output-type",
    "status": "your-status", // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "prompt": "your-worker-prompt",
    "source_ids": [],
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "context": "your-context",
    "generation_id": "your-generation-id", // generation id
    "current_version_id": "a0943c12-3198-4c02-b342-b29d3f297c2a", // version id
    "updated_at": "2025-02-14T15:49:44.120298+00:00",
    "use_source_context": true,
    "brand_id": "your-brand-id"
}
```

Fetch the generation version using the generation id and version id:
```http
GET https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}/version/{version_id}
Authorization: Bearer <your-tenant-api-key>
```

Here is the response for the generation version:
```json
{
    "result": null,
    "feedback": null,
    "previous_version_id": null,
    "version_id": "your-version-id",
    "status": "PROCESSING", // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "generation_id": "your-generation-id",
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "output_type": "your-output-type"
}
```

You can fetch the generation as well, using the generation id but not that this will return the latest version of the generation.

Here is how you can fetch the generation:
```http
GET https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}
Authorization: Bearer <your-tenant-api-key>
```

Here is the response for the generation:
```json
{
    "tenant_id": "your-tenant-id",
    "result": null,
    "worker_id": "your-worker-id",
    "output_type": "your-output-type",
    "status": "PROCESSING", // NOT_STARTED, QUEUED, PROCESSING, COMPLETED, FAILED
    "prompt": "your-worker-prompt",
    "source_ids": [],
    "created_at": "2025-02-14T15:49:44.120298+00:00",
    "context": "your-context",
    "generation_id": "your-generation-id",
    "updated_at": "2025-02-14T15:49:44.120298+00:00",
    "use_source_context": true,
    "current_version_id": "your-version-id",
    "brand_id": "your-brand-id"
}
```
