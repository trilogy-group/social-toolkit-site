---
sidebar_position: 3
---

# Architecture Overview

Brand Memory is built with a scalable, multi-tenant architecture designed for high-volume content processing and generation.

## System Components

### API Layer

The API layer provides RESTful endpoints for:
- Tenant management
- Brand management
- Content analysis
- Content generation

### Processing System

The processing system handles:
1. **Content Analysis**:
   - Text analysis
   - Image analysis
   - Video analysis
   - Audio analysis

2. **Content Generation**:
   - Text generation
   - Image generation (coming soon)
   - Video generation (coming soon)
   - Audio generation (coming soon)

### Queue System

Uses AWS SQS for:
- Analysis job queuing
- Generation job queuing

### Storage Layer

Multiple storage systems:
1. **OpenSearch**:
   - Content embeddings
   - Semantic search
   - Analysis results

2. **S3**:
   - Source content
   - Generated content
   - Binary assets

3. **DynamoDB**:
   - Tenant data
   - Brand data
   - Job status
   - System metadata

## Multi-tenant Architecture

### Tenant Hierarchy

Tenants can be organized in a hierarchical structure using parent-child relationships. This allows for:
- Structured organization of brands and content
- Inheritance of settings and configurations
- Simplified management of related tenants
- Flexible organization structure for enterprises

### Tenant Isolation

Each tenant has:
- Dedicated OpenSearch index
- Isolated S3 prefixes
- Separate API keys
- Independent concurrency limits

## Processing Pipeline

### Analysis Pipeline

1. **Content Submission**:
   - Validate content
   - Store in S3
   - Create job record

2. **Queue Processing**:
   - Pick up analysis job
   - Load content
   - Apply analysis prompts

3. **Result Storage**:
   - Store analysis results
   - Create embeddings
   - Update job status

### Generation Pipeline

1. **Request Handling**:
   - Validate request
   - Create job record
   - Queue generation task

2. **Content Generation**:
   - Load brand context
   - Apply generation worker
   - Create content

3. **Result Handling**:
   - Store generated content
   - Update job status
