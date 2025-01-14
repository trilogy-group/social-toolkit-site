# server.py
import requests
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

API_URL = "https://social-toolkit.ti.trilogy.com"

@mcp.tool()
def list_tenants() -> any:
    """List Tenants"""
    try:
        response = requests.get(f"{API_URL}/tenant")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = "Failed to list tenants"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_tenant(tenant_id: str) -> any:
    """List Tenants"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def create_tenant(name: str, description: str = None, settings: dict = None, concurrency_limits: dict = None) -> any:
    """Create a new tenant with the specified parameters"""
    try:
        payload = {
            "name": name,
            "description": description,
            "settings": settings or {},
            "concurrency_limits": concurrency_limits
        }
        response = requests.post(f"{API_URL}/tenant", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = "Failed to create tenant"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def update_tenant(tenant_id: str, updates: dict) -> any:
    """Update an existing tenant's details"""
    try:
        response = requests.put(f"{API_URL}/tenant/{tenant_id}", json=updates)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to update tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def delete_tenant(tenant_id: str) -> any:
    """Delete a tenant"""
    try:
        response = requests.delete(f"{API_URL}/tenant/{tenant_id}")
        response.raise_for_status()
        return {"status": "success", "message": f"Tenant {tenant_id} deleted"}
    except Exception as e:
        error_msg = f"Failed to delete tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def create_brand(tenant_id: str, name: str, description: str = None, settings: dict = None) -> any:
    """Create a new brand for a tenant"""
    try:
        payload = {
            "name": name,
            "description": description,
            "settings": settings or {}
        }
        response = requests.post(f"{API_URL}/tenant/{tenant_id}/brand", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to create brand for tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_brand(tenant_id: str, brand_id: str) -> any:
    """Get brand details"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def list_brands(tenant_id: str) -> any:
    """List all active brands for a tenant"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/brand")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to list brands for tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def update_brand(tenant_id: str, brand_id: str, updates: dict) -> any:
    """Update brand details"""
    try:
        response = requests.put(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}", json=updates)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to update brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def delete_brand(tenant_id: str, brand_id: str) -> any:
    """Delete a brand"""
    try:
        response = requests.delete(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}")
        response.raise_for_status()
        return {"status": "success", "message": f"Brand {brand_id} deleted"}
    except Exception as e:
        error_msg = f"Failed to delete brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def trigger_brand_compass(tenant_id: str, brand_id: str) -> any:
    """Trigger the generation of a brand compass"""
    try:
        response = requests.post(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/compass/trigger")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to trigger brand compass for brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_brand_compass(tenant_id: str, brand_id: str) -> any:
    """Get the latest brand compass"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/compass")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get brand compass for brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def create_source(tenant_id: str, brand_id: str, name: str, source_type: str, 
                 content_type: str = None, description: str = None, 
                 file_path: str = None, url: str = None, text: str = None) -> any:
    """
    Create a new source for a brand. Must provide one of: file_path, url, or text.
    source_type must be one of: KNOWLEDGE, GUIDELINES, SAMPLE
    content_type must be one of: VIDEO, AUDIO, TEXT, IMAGE
    """
    try:
        # Prepare the multipart form data
        files = {}
        data = {
            "name": name,
            "source_type": source_type,
        }
        if description:
            data["description"] = description
        if content_type:
            data["content_type"] = content_type
            
        # Handle different input types
        if file_path:
            with open(file_path, 'rb') as f:
                files = {'file': f}
        elif url:
            data["url"] = url
        elif text:
            data["text"] = text
        else:
            raise ValueError("Must provide one of: file_path, url, or text")

        response = requests.post(
            f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/source",
            data=data,
            files=files
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to create source for brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_source(tenant_id: str, brand_id: str, source_id: str) -> any:
    """Get source details"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/source/{source_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get source {source_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def list_sources(tenant_id: str, brand_id: str, source_type: str = None, status: str = None) -> any:
    """
    List sources for a brand. 
    Optional filters:
    - source_type: KNOWLEDGE, GUIDELINES, SAMPLE
    - status: QUEUED, PROCESSING, COMPLETED, FAILED
    """
    try:
        params = {}
        if source_type:
            params['source_type'] = source_type
        if status:
            params['status'] = status
            
        response = requests.get(
            f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/source",
            params=params
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to list sources for brand {brand_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def delete_source(tenant_id: str, brand_id: str, source_id: str) -> any:
    """Delete a source and its associated data"""
    try:
        response = requests.delete(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/source/{source_id}")
        response.raise_for_status()
        return {"status": "success", "message": f"Source {source_id} deleted"}
    except Exception as e:
        error_msg = f"Failed to delete source {source_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def reprocess_source(tenant_id: str, brand_id: str, source_id: str) -> any:
    """Trigger reprocessing of a source"""
    try:
        response = requests.post(f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/source/{source_id}/reprocess")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to reprocess source {source_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def create_prompt(tenant_id: str, name: str, content_type: str, prompt_text: str, 
                 description: str = None, settings: dict = None) -> any:
    """
    Create a new prompt for a tenant
    content_type must be one of: VIDEO, AUDIO, TEXT, IMAGE
    """
    try:
        payload = {
            "name": name,
            "content_type": content_type,
            "prompt_text": prompt_text,
            "description": description,
            "settings": settings or {}
        }
        response = requests.post(f"{API_URL}/tenant/{tenant_id}/prompt", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = "Failed to create prompt"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_prompt(tenant_id: str, prompt_id: str) -> any:
    """Get prompt details"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/prompt/{prompt_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get prompt {prompt_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def list_prompts(tenant_id: str, content_type: str = None) -> any:
    """
    List all active prompts for a tenant
    Optional filter:
    - content_type: VIDEO, AUDIO, TEXT, IMAGE
    """
    try:
        params = {}
        if content_type:
            params['content_type'] = content_type
            
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/prompt", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to list prompts for tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def update_prompt(tenant_id: str, prompt_id: str, updates: dict) -> any:
    """
    Update prompt details. Updates can include:
    - name: str
    - description: str
    - prompt_text: str
    - settings: dict
    """
    try:
        response = requests.put(f"{API_URL}/tenant/{tenant_id}/prompt/{prompt_id}", json=updates)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to update prompt {prompt_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def delete_prompt(tenant_id: str, prompt_id: str) -> any:
    """Delete a prompt"""
    try:
        response = requests.delete(f"{API_URL}/tenant/{tenant_id}/prompt/{prompt_id}")
        response.raise_for_status()
        return {"status": "success", "message": f"Prompt {prompt_id} deleted"}
    except Exception as e:
        error_msg = f"Failed to delete prompt {prompt_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def create_worker(tenant_id: str, output_type: str, prompt: str, name: str, description: str = None) -> any:
    """
    Create a new worker for a tenant
    output_type must be one of: TEXT
    """
    try:
        payload = {
            "output_type": output_type,
            "prompt": prompt,
            "name": name,
            "description": description
        }
        response = requests.post(f"{API_URL}/tenant/{tenant_id}/worker", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = "Failed to create worker"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_worker(tenant_id: str, worker_id: str) -> any:
    """Get worker details"""
    try:
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/worker/{worker_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get worker {worker_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def list_workers(tenant_id: str, output_type: str = None) -> any:
    """
    List all workers for a tenant
    Optional filter:
    - output_type: TEXT
    """
    try:
        params = {}
        if output_type:
            params['output_type'] = output_type
            
        response = requests.get(f"{API_URL}/tenant/{tenant_id}/worker", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to list workers for tenant {tenant_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def update_worker(tenant_id: str, worker_id: str, updates: dict) -> any:
    """
    Update worker details. Updates can include:
    - prompt: str
    - name: str
    - description: str
    """
    try:
        response = requests.put(f"{API_URL}/tenant/{tenant_id}/worker/{worker_id}", json=updates)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to update worker {worker_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def create_generation(tenant_id: str, brand_id: str, worker_id: str, context: str = None) -> any:
    """
    Start a new generation process
    Optional:
    - context: Additional context for the generation
    """
    try:
        payload = {}
        if context:
            payload['context'] = context
            
        response = requests.post(
            f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = "Failed to create generation"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def get_generation(tenant_id: str, brand_id: str, worker_id: str, generation_id: str) -> any:
    """Get generation details"""
    try:
        response = requests.get(
            f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation/{generation_id}"
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to get generation {generation_id}"
        print(error_msg, e)
        return error_msg

@mcp.tool()
def list_generations(tenant_id: str, brand_id: str, worker_id: str) -> any:
    """List all generations for a brand and worker"""
    try:
        response = requests.get(
            f"{API_URL}/tenant/{tenant_id}/brand/{brand_id}/worker/{worker_id}/generation"
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        error_msg = f"Failed to list generations for worker {worker_id}"
        print(error_msg, e)
        return error_msg

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')