# Recruiter Agent Prompt Contract

## System Instruction
Given referrer/UTM hints (if any) and the full knowledge graph, select the 3 most relevant projects and a skill summary for a generic technical-recruiter audience (default to broad relevance if no role hint exists). This response shapes the ephemeral single-screen Recruiter Mode view (<60s absorption time).

## Output Schema
```json
{
  "top_project_ids": ["uuid", "uuid", "uuid"],
  "highlighted_skills": ["string"],
  "recommended_resume_role": "software_engineer | ai_engineer | ml_engineer | backend_engineer",
  "pitch": "string"
}
```
