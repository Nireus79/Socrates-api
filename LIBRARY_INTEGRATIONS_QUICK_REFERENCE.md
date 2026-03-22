# Library Integrations - Quick Reference Guide

## REST API Endpoints

### Base: `/libraries`

#### Status Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/libraries/status` | GET | Get status of all library integrations |
| `/libraries/analyzer/status` | GET | Get socratic-analyzer status |
| `/libraries/learning/status` | GET | Get socratic-learning status |
| `/libraries/conflict/status` | GET | Get socratic-conflict status |
| `/libraries/knowledge/status` | GET | Get socratic-knowledge status |
| `/libraries/docs/status` | GET | Get socratic-docs status |

#### Code Analysis (socratic-analyzer)

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/libraries/analyzer/analyze-code` | POST | Analyze code quality | `code` (str), `filename` (str, optional) |

**Response**:
```json
{
  "quality_score": 75,
  "issues_count": 3,
  "patterns": [...],
  "recommendations": [...]
}
```

#### Learning Analytics (socratic-learning)

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/libraries/learning/log-interaction` | POST | Log interaction | `session_id`, `agent_name`, `input_data`, `output_data`, `tokens_used`, `cost`, `duration_ms`, `success`, `tags` |
| `/libraries/learning/status` | GET | Get status | (none) |

**Response** (log-interaction):
```json
{
  "status": "logged"
}
```

#### Conflict Resolution (socratic-conflict)

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/libraries/conflict/detect-and-resolve` | POST | Detect and resolve conflicts | `field`, `agent_outputs`, `agents` |
| `/libraries/conflict/status` | GET | Get status | (none) |

**Response**:
```json
{
  "conflict_detected": true/false,
  "recommended_value": "...",
  "confidence": 0.95
}
```

#### Knowledge Management (socratic-knowledge)

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/libraries/knowledge/store` | POST | Store knowledge item | `tenant_id`, `title`, `content`, `tags` (optional) |
| `/libraries/knowledge/search` | GET | Search knowledge | `tenant_id`, `query`, `limit` (default: 5) |
| `/libraries/knowledge/status` | GET | Get status | (none) |

**Response** (store):
```json
{
  "item_id": "kb-123",
  "title": "...",
  "status": "created"
}
```

**Response** (search):
```json
[
  {
    "title": "...",
    "content_preview": "..."
  },
  ...
]
```

#### Documentation Generation (socratic-docs)

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/libraries/docs/generate-readme` | POST | Generate documentation | `project_info` (dict) |
| `/libraries/docs/status` | GET | Get status | (none) |

**Response** (generate-readme):
```
# Project Name

Project description...

## Installation

...

## Usage

...
```

---

## CLI Commands

### Base: `socrates libraries`

#### Status Commands

```bash
# Show status of all library integrations
socrates libraries status

# Output:
# ============================================================
# Socratic Library Integration Status
# ============================================================
#
# Overall: 7/7 libraries enabled
#
# Library                  Status
# ----------------------------------------
# learning                 Enabled
# analyzer                 Enabled
# conflict                 Enabled
# knowledge                Enabled
# workflow                 Enabled
# docs                     Enabled
# performance              Enabled
```

#### Code Analysis

```bash
# Analyze Python file
socrates libraries analyze --file path/to/file.py

# Output:
# Analyzing code in 'path/to/file.py'...
# Analysis complete!
#
# Quality Score: 85/100
# Issues Found: 2
#
# Recommendations:
#   • Add type hints to function parameters
#   • Use context managers for file operations
#   • Simplify conditional logic
```

#### Knowledge Management

```bash
# Store knowledge item
socrates libraries knowledge-store \
  --tenant-id org-123 \
  --title "Python Best Practices" \
  --content "Always use type hints..." \
  --tags python practices best-practices

# Search knowledge
socrates libraries knowledge-search \
  --tenant-id org-123 \
  --query "type hints" \
  --limit 10

# Output:
# Searching knowledge base...
# Found 3 results:
#
# 1. Python Type Hints Guide
#    Type hints are optional annotations that specify the types...
#
# 2. Static Type Checking with mypy
#    mypy is a static type checker for Python...
#
# 3. Advanced Type Hints Patterns
#    Generic types, protocols, type aliases...
```

#### Documentation

```bash
# Generate documentation
socrates libraries docs-generate \
  --project-name "My Project" \
  --description "A Socratic tutoring application"

# Output:
# Generating documentation for 'My Project'...
# Documentation generated!
#
# # My Project
#
# A Socratic tutoring application
#
# ## Installation
#
# ...
```

---

## Python API Usage

```python
from socratic_system.orchestration.orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator(api_key_or_config="your-key")

# Analyze code
result = orchestrator.analyze_code_quality(code, filename)
# Returns: {"quality_score": int, "issues_count": int, ...}

# Log interaction
result = orchestrator.log_learning_interaction(
    session_id, agent_name, input_data, output_data,
    tokens=0, cost=0.0, duration_ms=0.0, success=True
)

# Detect conflicts
result = orchestrator.detect_agent_conflicts(
    field_name, agent_outputs_dict, agents_list
)

# Store knowledge
result = orchestrator.store_knowledge(
    tenant_id, title, content, tags=None
)

# Search knowledge
results = orchestrator.search_knowledge(tenant_id, query)

# Generate documentation
documentation = orchestrator.generate_documentation(project_info_dict)

# Get status
status = orchestrator.get_library_status()
# Returns: {"learning": bool, "analyzer": bool, ...}
```

---

## Library Dependencies

### Required (Base Installation)

```
socratic-core>=0.1.1              # Framework
socrates-nexus>=0.3.0             # LLM client
socratic-agents>=0.1.2            # Multi-agent
socratic-rag>=0.1.0               # Knowledge retrieval
socratic-security==0.4.0          # Security
```

### Optional (Feature-Specific)

```
socratic-learning>=0.1.1          # Learning analytics
socratic-analyzer>=0.1.0          # Code analysis
socratic-conflict>=0.1.0          # Conflict resolution
socratic-knowledge>=0.1.0         # Knowledge management
socratic-workflow>=0.1.1          # Workflow orchestration
socratic-docs>=0.1.0              # Documentation generation
socratic-performance>=0.1.0       # Performance monitoring
```

If optional libraries aren't installed, endpoints return graceful errors or empty results.

---

## Error Handling

All endpoints handle errors gracefully:

```json
{
  "status": "error",
  "message": "socratic-analyzer is not available. Is socratic-analyzer installed?"
}
```

CLI commands display user-friendly error messages:
```
Error: Connection error: Is the API server running at http://localhost:8000?
```

---

## Environment Variables

```bash
# API Server Configuration
SOCRATES_API_URL=http://localhost:8000

# Library-Specific Configuration
RAG_DATA_DIR=/path/to/vector/store
PINECONE_API_KEY=your-key
QDRANT_URL=http://localhost:6333
OPENAI_API_KEY=your-key

# Authentication
ANTHROPIC_API_KEY=your-key
JWT_SECRET_KEY=your-secret
```

---

## Response Status Codes

| Status | Meaning | Example Cause |
|--------|---------|---------------|
| 200 | Success | Operation completed successfully |
| 400 | Bad Request | Invalid parameters provided |
| 500 | Server Error | Unhandled exception in endpoint |
| 503 | Service Unavailable | Library not installed |

---

## Performance Characteristics

| Operation | Latency | Notes |
|-----------|---------|-------|
| Code analysis | 100-500ms | Depends on code size |
| Knowledge storage | 50-200ms | Includes indexing |
| Knowledge search | 200-1000ms | Semantic search overhead |
| Conflict detection | 50-200ms | Analysis complexity |
| Documentation generation | 1-5s | LLM call required |
| Library status check | <10ms | Cached status |

---

## Examples

### Example 1: Code Review Pipeline

```python
# Step 1: Generate code
code = orchestrator.generate_code(spec)

# Step 2: Analyze quality
analysis = orchestrator.analyze_code_quality(code)
print(f"Quality: {analysis['quality_score']}/100")

# Step 3: Store in knowledge base
orchestrator.store_knowledge(
    tenant_id="org-123",
    title=f"Generated Code - {spec}",
    content=code,
    tags=["generated", "reviewed"]
)

# Step 4: Log for learning
orchestrator.log_learning_interaction(
    session_id="session-456",
    agent_name="code_generator",
    input_data={"spec": spec},
    output_data={"code": code, "quality": analysis['quality_score']},
    duration_ms=2500
)
```

### Example 2: Multi-Agent Conflict Resolution

```python
# Get outputs from multiple agents
agent1_output = orchestrator.process_request("agent1", request)
agent2_output = orchestrator.process_request("agent2", request)

# Detect conflicts
resolution = orchestrator.detect_agent_conflicts(
    field="implementation_strategy",
    agent_outputs={
        "agent1": agent1_output["strategy"],
        "agent2": agent2_output["strategy"]
    },
    agents=["agent1", "agent2"]
)

if resolution["conflict_detected"]:
    # Use recommended value
    final_strategy = resolution["recommended_value"]
else:
    # Use agreement
    final_strategy = agent1_output["strategy"]
```

### Example 3: Knowledge-Based Learning

```bash
# Search for relevant knowledge
socrates libraries knowledge-search \
  --tenant-id user-123 \
  --query "debugging techniques for performance issues"

# Store learned pattern
socrates libraries knowledge-store \
  --tenant-id user-123 \
  --title "Performance Debugging Case Study" \
  --content "Discovered that n² loop was cause..." \
  --tags debugging performance case-study
```

---

## Troubleshooting

### API Returns 503 for Library Operations

**Cause**: Optional library not installed

**Solution**: Install the library
```bash
pip install socratic-learning socratic-analyzer # etc.
```

### CLI Command Not Found

**Cause**: socrates-cli not installed or outdated

**Solution**: Reinstall CLI
```bash
pip install --upgrade socrates-cli
```

### Knowledge Search Returns Empty Results

**Cause**: Knowledge base empty or query too specific

**Solution**:
1. Store some knowledge items first
2. Try broader search query
3. Check tenant_id is correct

### Code Analysis Reports High Issues Count

**Cause**: Normal for new/unoptimized code

**Solution**:
1. Review recommendations
2. Implement suggested improvements
3. Re-run analysis to track progress

---

## Additional Resources

- Full Integration Summary: `FULL_LIBRARY_INTEGRATION_SUMMARY.md`
- API Documentation: Available at `/docs` when API running
- CLI Help: `socrates --help` and `socrates libraries --help`
- Library Source: https://github.com/Nireus79/ (PyPI packages)
