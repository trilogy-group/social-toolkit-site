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

## Step 3: Create Generation Workers

Generation workers are also configured at the tenant level. They are specialized prompts for creating different types of content:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/worker
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Social Post Generator",
    "description": "Generate social media posts",
    "output_type": "TEXT",
    "prompt": "Create a social media post that matches our brand voice and style. Use our guidelines for tone and messaging."
}
```

## Step 4: Create Your Brand

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

## Step 5: Add Brand Content

Brand Memory uses three types of sources to understand and generate content for your brand:

### 1. Sample Content

Add examples of your brand's content:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Blog Post Sample",
    "description": "Example of our blog writing style",
    "source_type": "SAMPLE",
    "content_type": "TEXT",
    "content": "Your sample content here..."
}
```

### 2. Brand Knowledge

Add factual information about your brand:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Company History",
    "description": "Our company background",
    "source_type": "KNOWLEDGE",
    "content": "Company history and facts..."
}
```

### 3. Brand Guidelines

Add your brand rules and standards:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Voice Guidelines",
    "description": "Brand voice rules",
    "source_type": "GUIDELINES",
    "content": "Our brand voice guidelines..."
}
```

## Step 6: Analyze Content

The content analysis process is asynchronous:

1. Submit content for analysis:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source
Authorization: Bearer <your-tenant-api-key>
Content-Type: application/json

{
    "name": "Content Sample",
    "description": "Content to analyze",
    "source_type": "SAMPLE",
    "content_type": "TEXT",
    "content": "Content to analyze..."
}
```

The response will include a `source_id` that you'll need for checking the analysis status.

2. Poll for analysis results:
```http
GET https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/source/{source_id}
Authorization: Bearer <your-tenant-api-key>
```