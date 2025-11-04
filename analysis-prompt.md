---
description: Prompt for analyzing Claude Code best practices from engineering sources
---

# Analyzing Best Methods for Using Claude Code

Analyze best practices for using Claude Code based on sources listed in `@sources.csv`
(content available in `source_content/` folder).

## Process Flow

### 1. Filter & Categorize Content
- **Separate general vs. AI-specific practices**: Identify content that applies to traditional
  software development vs. practices specifically important for agentic AI coding
- **Highlight fundamentals**: Mark general engineering practices (version control, testing, CI)
  that have heightened importance when working with AI agents
- **Document criteria**: Note why each practice is categorized as general or AI-specific

### 2. Organize & Identify Patterns
- **Group by semantic areas**: Create logical categories (e.g., Testing Strategies,
  Prompt Engineering, Code Review, CI/CD Integration)
- **Highlight consensus**: Identify practices mentioned in 2+ sources and note the frequency
- **Note contradictions**: Flag conflicting recommendations with source attribution

### 3. Evaluate & Prioritize
Apply these criteria to each practice:
- **Impact**: High/Medium/Low value for production software quality
- **Effort**: Implementation complexity and learning curve
- **Specificity**: How unique this is to Claude Code vs. general AI coding
- **Evidence**: Whether the source provides data, examples, or anecdotal support

**Flag items as:**
- ✅ Highly recommended (high impact, reasonable effort, well reasoned, well substantiated)
- ⚠️ Context-dependent (valuable in specific scenarios)
- ❌ Low priority (minimal impact or excessive effort or insufficient evidence provided)

## Output Guidance

These are soft guidlines.

**Format**: Markdown report saved as `claude-code-best-practices-report.md`

**Structure**:
1. Executive Summary (2-3 key takeaways)
2. General Best Practices
    1. Best Practices that are eve more crucial in agentic AI coding workflows
2. Core Recommendations by Category (with priority/importance/impact flags)
    1. Highlight consensus Findings (practices cited by multiple sources) in each category
    2. If sources conflict, present both views with source attribution rather than choosing
3. Contradictions & Trade-offs
4. Appendix: 
    1. Source mapping table
    2. Complete set of recommendations

**Style**:
- Target audience: Software engineers building production systems with Claude Code
- Depth: Sufficient detail for actionability without excessive verbosity
- Include code examples where relevant
- Maximum length: 5000 words

## Error Handling
- If `source_content/` is missing, STOP AND RAISE A FLAG.
