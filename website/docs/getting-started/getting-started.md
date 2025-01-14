---
sidebar_position: 2
---

# Getting Started

This guide will help you get started with Social Toolkit. We'll walk through the process of setting up your tenant, creating your first brand, and using the system for content analysis and generation.

## Prerequisites

Before you begin, you'll need:

1. **API Keys**:
   - Anthropic API key (for Claude)
   - OpenAI API key (for embeddings)
   - Google AI API key (for Gemini)

2. **OpenSearch Instance**:
   - Host URL
   - Port
   - Region
   - Index name

## Step 1: Create Your Tenant

Your first step is to create a tenant. A tenant represents your organization or application and contains all your brands and configurations.

```http
POST https://social-toolkit.ti.trilogy.com/tenant
Content-Type: application/json

{
    "name": "Your application name",
    "description": "Your application description",
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
    }
}
```

Save the `tenant_id` from the response for future use.

## Step 2: Create Analysis Prompts

Analysis prompts are configured at the tenant level and define how content will be analyzed. Create prompts for different aspects of your content and for different content types:

```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/prompt
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
```

The response will include a `status` field. Continue polling until the status is `COMPLETED` or `FAILED`. Typical analysis time is 15-180 seconds and can very based on content type.

## Step 7: Generate Content

Content generation is also an asynchronous process:

1. Submit generation request:
```http
POST https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation
Content-Type: application/json

{
    "context": "Create a post about our new feature"
}
```

The response will include a `generation_id` that you'll need for checking the generation status.

2. Poll for generation results:
```http
GET https://social-toolkit.ti.trilogy.com/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}
```

The response will include a `status` field. Continue polling until the status is `COMPLETED` or `FAILED`. Typical generation time is 15-60 seconds depending on the content type.
