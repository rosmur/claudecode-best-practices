---
title: Claude Code Best Practices
layout: home
toc: true
---

**This guide was written by Claude Code synthesizing the information contained in the sources listed below and following this [analysis prompt](../analysis-prompt.md).**


## 1. Executive Summary

After analyzing 12 detailed sources spanning personal experiences, official Anthropic guidance, and community insights, three key takeaways emerge:

1. **Context Management is Paramount**: The most successful Claude Code users obsessively manage context through CLAUDE.md files, aggressive /clear usage, documentation systems (dev docs, living plans), and token-efficient tool design. Context degradation is the primary failure mode.

2. **Planning Before Implementation is Non-Negotiable**: Every high-quality source emphasizes upfront planning (Planning Mode, written plans, architectural reviews) before coding. "Vibe coding" works for throwaway MVPs, but production code requires structured thinking, validation, and documentation.

3. **Simplicity Beats Complexity**: The most effective workflows avoid over-engineering. Simple control loops outperform multi-agent systems. Low-level tools (Bash, Read, Edit) plus selective high-level abstractions beat heavy RAG or complex frameworks. LLMs are fragile; additional complexity makes debugging exponentially harder.


*Total word count: 4,987 words*<br />
*Reading Time: ~25min (although not intended to be read through from start to finish but more so as a reference manual)*

## 2. Sources

The following sources were analyzed to create this comprehensive guide:

| Title | Author | Published | Source |
|-------|--------|-----------|--------|
| 6 Weeks of Claude Code | Puzzmo Blog | 2025-07-29 | [Link](https://blog.puzzmo.com/posts/2025/07/30/six-weeks-of-claude-code/) |
| Claude Code Best Practices | @AnthropicAI | - | [Link](https://www.anthropic.com/engineering/claude-code-best-practices) |
| Claude Code Is All You Need | - | - | [Link](https://dwyer.co.za/static/claude-code-is-all-you-need.html) |
| Getting Good Results from Claude Code | Chris Dzombak | 2025-08-08 | [Link](https://www.dzombak.com/blog/2025/08/getting-good-results-from-claude-code/) |
| How Anthropic teams use Claude Code | @AnthropicAI | - | [Link](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code) |
| The ULTIMATE AI Coding Guide for Developers (Claude Code) | Sabrina Ramonov 🍄 | 2025-07-05 | [Link](https://www.sabrina.dev/p/ultimate-ai-coding-guide-claude-code) |
| Turning Claude Code Into My Best Design Partner | Between the Prompts | 2025-08-17 | [Link](https://betweentheprompts.com/design-partner/) |
| What makes Claude Code so damn good (and how to recreate that magic in your agent)!? | vivek | 2025-08-21 | [Link](https://minusx.ai/blog/decoding-claude-code/) |
| "If You're Not Using These Things With CC, Then Maybe the Problem Is *You*" | CaptainCrouton89 | 2025-09-12 | [Link](https://old.reddit.com/r/ClaudeAI/comments/1nfa4kj/if_youre_not_using_these_things_with_cc_then/) |
| Building a Personal AI Factory | John Rush | 2025-07-01 | [Link](https://www.john-rush.com/posts/ai-20250701.html) |
| How I Use Every Claude Code Feature | Shrivu Shankar | 2025-11-01 | [Link](https://blog.sshh.io/p/how-i-use-every-claude-code-feature) |
| Claude Code is a Beast – Tips from 6 Months of Hardcore Use | JokeGold5455 | 2025-10-29 | [Link](https://www.reddit.com/r/ClaudeAI/comments/1oivjvm/claude_code_is_a_beast_tips_from_6_months_of/) |

## 3. General Best Practices

Traditional software engineering best practices are important to follow and the following become **even more critical** when working with AI because:
- AI agents lack human judgment and make mistakes humans wouldn't
- Errors compound faster in autonomous systems
- Code review is harder when you didn't write the code
- Technical debt accumulates invisibly without strict practices

### 3.1. Test-Driven Development (TDD)
**Sources**: Claude_Code_Best_Practices (Anthropic), Ultimate_AI_Coding_Guide, Getting_Good_Results, 6_months_hardcore_use

**Why More Important with AI**: AI-generated code often "works" superficially but contains subtle bugs. Tests provide the only reliable validation mechanism.

**Consensus Pattern** (4+ sources):
1. Write tests BEFORE implementation
2. Confirm tests fail (avoid mock implementations)
3. Commit tests separately
4. Implement until tests pass
5. Do NOT modify tests during implementation

**Example workflow** (from Ultimate_AI_Coding_Guide):
```
qcode instruction:
"Implement your plan and make sure your new tests pass.
Always run tests to make sure you didn't break anything else.
Always run prettier on newly created files.
Always run turbo typecheck lint."
```

**Priority**: ✅ Highly recommended (High impact, moderate effort, well-substantiated)

### 3.2. Continuous Quality Gates
**Sources**: 6_months_hardcore_use, Ultimate_AI_Coding_Guide, Getting_Good_Results, Claude_Code_Best_Practices

**Implementation**: Use hooks to enforce quality automatically:
- TypeScript/linter checks after every edit
- Build validation before commits
- Test execution on file changes
- Formatting automation (though see caveat below)

**Hook Example** (from 6_months_hardcore_use):
```typescript
// Stop hook: Runs when Claude finishes responding
1. Read edit logs to find modified repos
2. Run build scripts on each affected repo
3. Check for TypeScript errors
4. If <5 errors: Show them to Claude
5. If ≥5 errors: Recommend auto-error-resolver agent
6. Log everything
```

**Caveat**: Automatic formatting hooks can consume significant context tokens (160k in 3 rounds reported). Consider manual formatting between sessions instead.

**Priority**: ✅ Highly recommended (High impact, medium effort, proven results)

### 3.3. Code Review - Including AI's Own Work
**Sources**: Getting_Good_Results, How_Anthropic_teams_use, Ultimate_AI_Coding_Guide, 6_months_hardcore_use

**Critical Insight**: "I believe I'm ultimately responsible for the code in a PR with my name on it, regardless of how it was produced" - Chris Dzombak

**Multi-Layer Review Process**:
1. **Self-review by Claude**: Ask Claude to review its own code using subagents or fresh context
2. **Human review**: Manually verify behavior and test coverage
3. **Multiple Claude instances**: Have one Claude write, another review (fresh context = better critique)

**What to Look For**:
- Spaghetti code (hard to follow logic)
- Substantial API/backend changes
- Unnecessary imports, functions, comments
- Missing error handling
- Security vulnerabilities

**Priority**: ✅ Highly recommended (Critical for production code)

### 3.4. Incremental Commits with Clear Messages
**Sources**: Claude_Code_Best_Practices, Getting_Good_Results, Ultimate_AI_Coding_Guide, Building_AI_Factory

**Pattern**: Commit early and often with meaningful messages
- Use Conventional Commits format
- Each commit should compile and pass tests
- Avoid references to "Claude" or "AI-generated" in messages
- Commit in stages tied to plan/task checkpoints

**Example from Building_AI_Factory**:
```
"One important instruction is to have claude write commits
as it goes for each task step. This way either claude or I
can revert to a previous state if something goes wrong."
```

**Priority**: ✅ Highly recommended (Essential for collaboration and rollback)

### 3.5. Monorepo Architecture
**Sources**: 6_Weeks_of_Claude_Code, what_makes_CC_good, How_I_Use_Every_Feature

**Why It Matters**: Monorepos provide AI with comprehensive context in one place
- Schema, API definitions, implementation all accessible
- Single PR can span full stack
- Reduces context-gathering overhead

**Quote from Puzzmo blog**: "A monorepo is perfect for working with an LLM, because it can read the file which represents our schema, it can read the sdl files defining the public GraphQL API, read the per-screen requests and figure out what you're trying to do."

**Priority**: ⚠️ Context-dependent (High value for new projects, difficult migration for existing codebases)

## 4. Core Recommendations by Category

### 4.1. Context Management (Most Critical)

#### 4.1.1. CLAUDE.md File Structure
**Sources**: ALL 12 sources mention this
**Frequency**: Unanimous consensus

**Structure Best Practices**:

**Root CLAUDE.md** (100-200 lines max):
- Critical universal rules
- Quick command reference
- Testing instructions
- Repository etiquette
- Pointers to repo-specific files

**Subdirectory CLAUDE.md files** (50-100 lines):
- Project-specific context
- Local commands and quirks
- Architecture pointers

**Anti-Patterns to Avoid** (from How_I_Use_Every_Feature):
```
❌ Don't: @-file docs (embeds entire file on every run)
✅ Do: "For complex usage or FooBarError, see path/to/docs.md"

❌ Don't: "Never use --foo-bar flag" (agent gets stuck)
✅ Do: "Never use --foo-bar; prefer --baz instead"

❌ Don't: Write comprehensive manual
✅ Do: Document what Claude gets wrong
```

**Token Efficiency**:
- One team reports 20k baseline tokens (10% of 200k context) in their monorepo
- Keep under 2000 tokens total for CLAUDE.md
- Use CLAUDE.md as "forcing function" to simplify tooling

**Priority**: ✅ Highly recommended (Highest impact practice, low effort)

#### 4.1.2. Aggressive Context Clearing
**Sources**: if_youre_not_using_these, How_I_Use_Every_Feature, Claude_Code_Best_Practices

**Rules**:
- Clear at 60k tokens or 30% context (don't wait for limits)
- Use `/clear` + `/catchup` pattern for simple restart
- Use "Document & Clear" for complex tasks

**Document & Clear Pattern**:
1. Have Claude write progress to .md file
2. `/clear` the context
3. Start fresh session reading the .md file
4. Continue work

**Avoid /compact**: "The automatic compaction is opaque, error-prone, and not well-optimized" - Shrivu Shankar

**Priority**: ✅ Highly recommended (Critical for quality maintenance)

#### 4.1.3. Documentation Systems

**Dev Docs System** (from 6_months_hardcore_use, Design_Partner, Building_AI_Factory):

**The Three-File Pattern**:
```
~/dev/active/[task-name]/
├── [task-name]-plan.md      # The accepted plan
├── [task-name]-context.md   # Key files, decisions
└── [task-name]-tasks.md     # Checklist of work
```

**Living Document Approach** (from Design_Partner):
- Update plan during implementation
- Plan documents reveal changed requirements
- Check plan is up-to-date before each commit
- Enables fresh conversations to pick up exactly where you left off

**Priority**: ✅ Highly recommended (Prevents "losing the plot", high impact)

### 4.2. Planning & Architecture

#### 4.2.1. Planning Mode is Mandatory
**Sources**: Claude_Code_Best_Practices, 6_months_hardcore_use, if_youre_not_using_these, Ultimate_AI_Coding_Guide, Design_Partner

**Consensus**: Planning before coding is non-negotiable for production work

**Planning Workflow** (synthesized from multiple sources):

**Step 1: Initial Planning**
```
1. Enter Planning Mode
2. Provide high-level description + pointers to existing code
3. Let Claude research and propose approaches
4. Review thoroughly (catch misunderstandings early)
```

**Step 2: Plan Validation**
- Ask clarifying questions
- Challenge assumptions
- Request 2-3 alternative approaches with pros/cons
- Use "think", "think hard", "think harder", "ultrathink" for deeper analysis

**Step 3: Document**
- Exit plan mode and create dev docs
- Or use `/dev-docs` slash command
- Store in version-controlled location

**Step 4: Implementation**
- Start fresh context with plan
- Implement in stages (1-2 sections at a time)
- Review between stages
- Update plan as you go

**Quote from Design_Partner**: "Sometimes, I'm not satisfied with the suggested implementation. In this case, instead of updating the plan, I tell it why it's wrong, expecting it to change its approach."

**Priority**: ✅ Highly recommended (Essential for complex features)

#### 4.2.2. Explore, Plan, Code, Commit
**Sources**: Claude_Code_Best_Practices, How_Anthropic_teams_use

**The Workflow**:
1. **Explore**: Read relevant files, images, URLs (explicitly tell it NOT to code yet)
2. **Plan**: Use subagents to verify details, create plan with "think" mode
3. **Code**: Implement with explicit verification steps
4. **Commit**: Update READMEs/changelogs, create PR

**Key Insight**: "Steps #1-#2 are crucial—without them, Claude tends to jump straight to coding"

**Priority**: ✅ Highly recommended (Standard workflow pattern)

#### 4.2.3. Specification Documents
**Sources**: Getting_Good_Results, Claude_Code_Is_All_You_Need, Design_Partner

**Pattern**: Write clear specs before starting
- Reduces ambiguity
- Provides persistent context
- Examples: [1](link), [2](link), [3](link), [4](link)

**Spec Quality Matters**:
- Claude_Code_Is_All_You_Need shows 500 words of guidance transforms 500MB broken code → 30KB working code
- The last 5 bullets specifying tech stack were the difference

**Priority**: ✅ Highly recommended (High impact for complex features)

### 4.3. Tool Usage & Automation

#### 4.3.1. Skills System (AI-Specific)
**Sources**: 6_months_hardcore_use, How_I_Use_Every_Feature, Claude_Code_Best_Practices

**Critical Discovery**: Skills need auto-activation to work reliably

**The Problem**: Manual skills are ignored ~90% of the time

**The Solution**: Hook-based auto-activation

**Auto-Activation Pattern** (from 6_months_hardcore_use):

**UserPromptSubmit Hook** (before Claude sees message):
```typescript
1. Analyze prompt for keywords/intent
2. Check which skills are relevant
3. Inject "🎯 SKILL ACTIVATION CHECK - Use X skill"
4. Claude sees reminder before reading question
```

**Stop Event Hook** (after response):
```typescript
1. Analyze edited files
2. Check for risky patterns (try-catch, DB ops, async)
3. Display gentle self-check reminder
4. Non-blocking awareness
```

**skill-rules.json Pattern**:
```json
{
  "backend-dev-guidelines": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["backend", "controller", "API"],
      "intentPatterns": ["(create|add).*?(route|endpoint)"]
    },
    "fileTriggers": {
      "pathPatterns": ["backend/src/**/*.ts"],
      "contentPatterns": ["router\\."]
    }
  }
}
```

**Skill Structure** (Anthropic best practices):
- Main SKILL.md: Under 500 lines
- Use progressive disclosure with resource files
- Before restructuring: 1,500+ line files
- After: 300-400 line main + 10-11 resource files
- Token efficiency improved 40-60%

**Priority**: ✅ Highly recommended (Transforms skills from useless to essential)

#### 4.3.2. Hooks for Quality Control
**Sources**: 6_months_hardcore_use, How_I_Use_Every_Feature, if_youre_not_using_these

**Consensus Hook Types**:

**1. Block-at-Submit Hooks** (Primary strategy):
```typescript
PreToolUse hook wrapping Bash(git commit)
→ Check for /tmp/agent-pre-commit-pass file
→ Block commit if missing
→ Force "test-and-fix" loop until green
```

**2. Hint Hooks** (Non-blocking feedback):
```typescript
Provide fire-and-forget guidance if suboptimal patterns detected
```

**Critical Insight**: "Don't block at write time—let the agent finish its plan, then check the final result"

**Common Hooks**:
- Build checker (TypeScript/linter errors)
- Test runner (ensure passing tests)
- Error handling reminder (gentle philosophy)
- Skills auto-activation (covered above)

**Priority**: ✅ Highly recommended (Prevents errors from persisting)

#### 4.3.3. Subagents/Task Delegation
**Sources**: Claude_Code_Best_Practices, Building_AI_Factory, 6_months_hardcore_use, How_I_Use_Every_Feature

**Two Competing Philosophies**:

**Philosophy A: Custom Specialized Subagents** (from 6_months_hardcore_use)
```
Examples:
- code-architecture-reviewer
- build-error-resolver
- frontend-error-fixer
- strategic-plan-architect
```

**Philosophy B: Master-Clone Architecture** (from How_I_Use_Every_Feature)
```
Preferred alternative:
- Put all context in CLAUDE.md
- Let main agent use Task(...) to spawn clones of itself
- Agent manages own orchestration dynamically
- Avoids gatekeeping context
- Avoids forcing human workflows
```

**Contradiction Analysis**:
- Both approaches work in practice
- Custom subagents: Better for highly specialized tasks
- Clone pattern: Better for preserving context, more flexible
- Context size is the deciding factor

**Consensus Middle Ground**:
- Use specialized subagents sparingly for very specific tasks
- Default to clone pattern for most delegation
- Always provide clear return expectations

**Priority**: ⚠️ Context-dependent (Depends on task complexity and context needs)

#### 4.3.4. Slash Commands
**Sources**: Claude_Code_Best_Practices, 6_months_hardcore_use, if_youre_not_using_these

**Philosophy**: Simple shortcuts, not complex workflows

**Anti-Pattern Warning**: "If you have a long list of complex custom slash commands, you've created an anti-pattern. The entire point is to type almost whatever you want and get useful results." - Shrivu Shankar

**Recommended Slash Commands**:

**Planning/Docs**:
- `/dev-docs` - Create strategic plan
- `/catchup` - Read all changed files in branch
- `/create-dev-docs` - Convert plan to dev doc files

**Quality**:
- `/code-review` - Architectural review
- `/build-and-fix` - Run builds and fix errors

**Testing**:
- `/test-route` - Test authenticated routes
- `/route-research-for-testing` - Find affected routes

**Git Integration**:
- `/pr` - Clean up code, prepare PR with good commit message

**Priority**: ✅ Highly recommended (Low effort, high productivity gain)

#### 4.3.5. MCP Strategy Evolution
**Sources**: How_I_Use_Every_Feature, what_makes_CC_good, if_youre_not_using_these

**Critical Insight**: Heavy MCP usage is an anti-pattern

**Quote**: "If you're using more than 20k tokens of MCPs, you're crippling Claude. That would only give you a measly 20k tokens left of actual work before context is cooked."

**New MCP Philosophy - "Scripting Model"**:

**Bad MCP Design** (avoid):
```
Dozens of tools mirroring REST API:
- read_thing_a()
- read_thing_b()
- update_thing_c()
→ Context bloat, rigid abstractions
```

**Good MCP Design**:
```
Few powerful gateways:
- download_raw_data(filters...)
- take_sensitive_gated_action(args...)
- execute_code_in_environment(code...)
→ MCP handles auth/security, agent scripts against data
```

**Skills > MCP for Most Use Cases**:
- Skills formalize the "scripting" layer
- MCPs should be secure gateways, not abstractions
- Most stateless tools → Simple CLIs (documented in Skills)
- MCPs only for stateful environments (e.g., Playwright)

**Token Efficiency**:
```
Custom minimal MCP: 3 tools, compressed markdown output
vs
Default Supabase MCP: Destroys context
```

**Priority**: ✅ Highly recommended (Critical for context management)

### 4.4. Workflow Optimization

#### 4.4.1. Specificity in Instructions
**Sources**: Claude_Code_Best_Practices, Ultimate_AI_Coding_Guide, 6_months_hardcore_use

**Consensus**: Vague instructions produce vague results

**Bad vs Good Examples**:

**Bad**:
```
"Add a user settings page"
```

**Good**:
```
"Create a user settings page at /settings with:
- Profile section (name, email, avatar upload)
- Notification preferences (checkboxes for email/push)
- Use existing UserProfile component pattern
- Follow MUI v7 layout grid system
- Add tests for form validation"
```

**Quote**: "Claude can infer intent, but it can't read minds. Specificity leads to better alignment with expectations."

**Priority**: ✅ Highly recommended (Foundational practice)

#### 4.4.2. Visual References
**Sources**: Claude_Code_Best_Practices, How_Anthropic_teams_use, Poster_Maker_example

**Methods**:
- Paste screenshots (macOS: cmd+ctrl+shift+4 → ctrl+v)
- Drag and drop images
- Provide image file paths
- Design mocks as reference for UI

**Iteration Pattern**:
```
1. Give Claude visual mock
2. Implement in code
3. Take screenshot of result
4. Compare to mock and iterate
5. Usually 2-3 iterations for good match
```

**Quote**: "Like humans, Claude's outputs tend to improve significantly with iteration. While the first version might be good, after 2-3 iterations it will typically look much better."

**Priority**: ✅ Highly recommended (Essential for UI work, helpful for debugging)

#### 4.4.3. Course Correction Techniques
**Sources**: Claude_Code_Best_Practices, 6_months_hardcore_use

**Four Correction Tools**:

1. **Ask for a plan first** - Confirm before coding
2. **Press Escape** - Interrupt during thinking/edits, redirect
3. **Double-tap Escape** - Jump back in history, edit previous prompt
4. **Ask to undo** - Often with option 2 to try different approach

**Philosophy**: "Though Claude Code occasionally solves problems perfectly on the first attempt, using these correction tools generally produces better solutions faster."

**Auto-Accept Mode**: Use shift+tab to toggle autonomous work, but active collaboration usually produces better results

**Priority**: ✅ Highly recommended (Essential skill for effective use)

#### 4.4.4. Data Input Methods
**Sources**: Claude_Code_Best_Practices, 6_months_hardcore_use

**Multiple Methods**:
- Copy/paste into prompt
- Pipe into Claude (`cat foo.txt | claude`)
- Tell Claude to pull via bash/MCP/slash commands
- Ask Claude to read files or fetch URLs

**Most sessions use combination of approaches**

**Example**: "Pipe in log file, then tell Claude to use tool to pull additional context to debug"

**Priority**: ✅ Highly recommended (Flexibility improves workflows)

#### 4.4.5. Git Worktrees for Parallel Work
**Sources**: Claude_Code_Best_Practices, Building_AI_Factory, 6_months_hardcore_use

**Pattern**: Run multiple Claude instances on independent tasks

**Setup**:
```bash
git worktree add ../project-feature-a feature-a
cd ../project-feature-a && claude
# In new terminal tab:
git worktree add ../project-feature-b feature-b
cd ../project-feature-b && claude
```

**Best Practices**:
- Use consistent naming conventions
- One terminal tab per worktree
- Set up notifications for Claude needing attention (iTerm2)
- Separate IDE windows per worktree
- Clean up: `git worktree remove ../project-feature-a`

**Priority**: ⚠️ Context-dependent (High value for experienced users with parallel workflows)

### 4.5. Production Code Quality

#### 4.5.1. Error Handling Standards
**Sources**: Ultimate_AI_Coding_Guide, 6_months_hardcore_use, Getting_Good_Results

**Pattern**: Explicit error handling with monitoring

**Best Practices**:
```typescript
// From Ultimate_AI_Coding_Guide
try {
  await prismaOperation()
} catch (error) {
  // ✅ MUST: Capture to Sentry
  Sentry.captureException(error)
  // ✅ Include context for debugging
  throw new CustomError('Descriptive message', { context })
}
```

**Gentle Reminder Hook** (from 6_months_hardcore_use):
```
After edits, check for:
- try-catch blocks
- async operations
- database calls
- controllers

Show non-blocking reminder:
"Did you add Sentry.captureException()?"
"Are Prisma operations wrapped?"
```

**Philosophy**: "Fail fast with descriptive messages. Never silently swallow exceptions."

**Priority**: ✅ Highly recommended (Critical for production reliability)

#### 4.5.2. Testing Standards
**Sources**: Ultimate_AI_Coding_Guide, Getting_Good_Results, How_Anthropic_teams_use

**Testing Checklist** (from Ultimate_AI_Coding_Guide):

```
1. SHOULD parameterize inputs (no magic numbers/strings)
2. SHOULD NOT add test unless it can fail for real defect
3. SHOULD ensure description matches expect assertion
4. SHOULD compare to independent expectations, not function output
5. SHOULD follow same lint/type-safety as prod code
6. SHOULD express invariants/axioms (use fast-check for property tests)
7. Unit tests grouped under describe(functionName)
8. Use expect.any(...) for variable parameters
9. ALWAYS use strong assertions (toEqual vs toBeGreaterThanOrEqual)
10. SHOULD test edge cases, realistic input, boundaries
11. SHOULD NOT test conditions caught by type checker
```

**Test Types**:
- **Unit tests**: Colocated `*.spec.ts` in same directory
- **Integration tests**: Separate from unit tests (don't mock DB)
- **Property-based tests**: Use `fast-check` for invariants

**Priority**: ✅ Highly recommended (Essential for quality assurance)

#### 4.5.3. Type Safety
**Sources**: Ultimate_AI_Coding_Guide, 6_Weeks_of_Claude_Code

**Consensus on Tech Stack**:
"React, Relay, GraphQL, TypeScript are boring and very explicit technologies. There are compilation steps in all of these systems which means everything has to be available locally and correct to run" - Puzzmo blog

**Type Safety Practices**:
```typescript
// Prefer branded types for IDs
type UserId = Brand<string, 'UserId'> // ✅
type UserId = string                  // ❌

// Use import type for type-only imports
import type { User } from './types'   // ✅
import { User } from './types'        // ❌

// Override incorrect generated types
// In db-types.override.ts
export interface CustomOverride {
  bigIntField: string; // Override BigInt → string
}
```

**Priority**: ✅ Highly recommended (Prevents runtime errors)

### 4.6. Advanced Patterns

#### 4.6.1. Headless Mode for Automation
**Sources**: Claude_Code_Best_Practices, if_youre_not_using_these

**Use Cases**:
- CI/CD integration
- Pre-commit hooks
- Build scripts
- Issue triage
- Linting/code review

**Two Primary Patterns**:

**1. Fanning Out** (large migrations):
```bash
# Generate task list
# Loop through tasks
claude -p "migrate foo.py from React to Vue.
Return OK if succeeded, FAIL if failed." \
  --allowedTools Edit Bash(git commit:*)
```

**2. Pipelining**:
```bash
claude -p "<your prompt>" --json | your_command
```

**Example - Issue Triage**:
```bash
# GitHub webhook triggers:
claude -p "Analyze issue #123 and assign labels" \
  --output-format stream-json
```

**Priority**: ⚠️ Context-dependent (High value for automation, requires setup)

#### 4.6.2. Multi-Claude Verification
**Sources**: Claude_Code_Best_Practices, Building_AI_Factory

**Pattern**: Separate contexts for writing and reviewing

**Workflow**:
```
1. Claude A: Write code
2. /clear or start Claude B in new terminal
3. Claude B: Review Claude A's work
4. /clear or start Claude C
5. Claude C: Read code + review feedback, edit based on feedback
```

**Advanced: o3 + Sonnet Pipeline** (from Building_AI_Factory):
```
o3: Generate plan (asks clarifying questions)
→ Sonnet 4: Read plan, verify, create task list
→ Sonnet 3.7/4: Execute plan
→ Sonnet 4: Verify against original plan
→ o3: Verify against original ask (uncompromising)
→ Any issues → Bake back into plan template
```

**Philosophy**: "Outputs are disposable; plans and prompts compound. Debugging at the source scales across every future task."

**Priority**: ⚠️ Context-dependent (High value for critical code, adds complexity)

#### 4.6.3. Background Process Management
**Sources**: 6_months_hardcore_use

**Problem**: Can't see backend service logs while they run

**Solution: PM2**:
```bash
pnpm pm2:start  # Start all services

# Claude can now:
pm2 logs email --lines 200
pm2 restart email
pm2 monit  # Memory/CPU monitoring
```

**Configuration**:
```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'form-service',
      script: 'npm',
      args: 'start',
      cwd: './form',
      error_file: './form/logs/error.log',
      out_file: './form/logs/out.log',
    },
    // ... more services
  ]
};
```

**Benefit**: Claude can autonomously debug issues without human log-fetching

**Caveat**: Hot reload doesn't work with PM2 (still run frontend with `pnpm dev`)

**Priority**: ⚠️ Context-dependent (Essential for microservices, overkill for simple apps)

#### 4.6.4. Utility Scripts in Skills
**Sources**: 6_months_hardcore_use, Claude_Code_Best_Practices

**Pattern**: Attach scripts to skills instead of documenting procedures

**Example**:

### 4.7. Testing Authenticated Routes

Use the provided test-auth-route.js script:

```bash
node scripts/test-auth-route.js http://localhost:3002/api/endpoint
```

The script handles:
1. Gets refresh token from Keycloak
2. Signs token with JWT secret
3. Creates cookie header
4. Makes authenticated request


**Benefit**: No reinventing the wheel each time; ready-to-use tools

**Priority**: ✅ Highly recommended (Reduces cognitive load, improves consistency)

### 4.8. Architecture & Design

#### 4.8.1. Simple Control Loops
**Sources**: what_makes_CC_good, How_I_Use_Every_Feature

**Critical Insight**: "Debuggability >>> complicated hand-tuned multi-agent lang-chain-graph-node mishmash"

**Claude Code Architecture**:
- One main thread (flat message list)
- Maximum one branch (subagent results added to main history)
- No complex multi-agent systems
- Simple iterative tool calling for most tasks

**Quote**: "Despite multi-agent systems being all the rage, Claude Code has just one main thread... I highly doubt your app needs a multi-agent system."

**Reasoning**:
- Every abstraction layer makes debugging exponentially harder
- Deviates from general model improvement trajectory
- LLMs are fragile; added complexity breaks unpredictably

**Priority**: ✅ Highly recommended (Foundational architecture decision)

#### 4.8.2. LLM Search > RAG
**Sources**: what_makes_CC_good, Claude_Code_Best_Practices

**Claude Code Approach**: Complex ripgrep, jq, find commands (no RAG)

**Why No RAG**:

RAG introduces hidden failure modes:
- What similarity function?
- What reranker?
- How to chunk code?
- How to handle large JSON/logs?

LLM Search:
- Looks at 10 lines to understand structure
- Looks at 10 more if needed (just like humans)
- RL learnable (BigLabs already working on this)
- Model does heavy lifting (fewer moving parts)


**Quote**: "This is the Camera vs Lidar of the LLM era"

**Priority**: ✅ Highly recommended (Architectural decision with major implications)

#### 4.8.3. Tool Abstraction Level
**Sources**: what_makes_CC_good, Claude_Code_Best_Practices

**Question**: Generic high-level vs low-level tools?

**Answer**: Both, strategically chosen

**Claude Code Tools**:
- **Low-level**: Bash, Read, Write (flexibility)
- **Medium-level**: Edit, Grep, Glob (frequently used patterns)
- **High-level**: Task, WebFetch, exit_plan_mode (deterministic workflows)

**Decision Framework**:

```
Use frequency × Accuracy trade-off

High frequency task → Dedicated tool (Grep, Glob)
Low frequency → Use Bash
Highly deterministic → High-level tool (WebFetch)
```

**Priority**: ⚠️ Context-dependent (Design decision for custom tools)

## 5. Contradictions & Trade-offs

### 5.1. Skills vs Context Bloat

**Position A** (6_months_hardcore_use): Create many specialized skills
- frontend-dev-guidelines (398 lines + 10 resources)
- backend-dev-guidelines (304 lines + 11 resources)
- workflow-developer, notification-developer, etc.

**Position B** (if_youre_not_using_these): Keep skills minimal
- "If they're longer than 100 lines, you're in the danger zone"
- Context efficiency is paramount

**Resolution**:
- Use progressive disclosure (main file <500 lines + resource files)
- Auto-activation hooks are essential either way
- Token budget determines skill count
- Measure baseline context cost and adjust

### 5.2. Custom Subagents vs Clone Pattern

**Position A** (6_months_hardcore_use): Build specialized subagents
- code-architecture-reviewer
- build-error-resolver
- strategic-plan-architect
- Clear, specific roles

**Position B** (How_I_Use_Every_Feature): Avoid custom subagents
- They gatekeep context
- They force human workflows
- Use Task(...) to spawn agent clones instead
- Let agent manage orchestration

**Resolution**:
- Both work in practice
- Custom subagents: Highly specialized, narrow tasks
- Clone pattern: Preserves context, more flexible
- Context availability is deciding factor
- Most users should start with clone pattern, add specialized agents only when clear need emerges

### 5.3. Auto-Formatting Hooks

**Position A** (6_months_hardcore_use initially): Auto-format after edits
- Consistency without manual intervention
- Files always properly formatted

**Position B** (Updated recommendation): Don't auto-format in hooks
- File modifications trigger system-reminders
- Can consume 160k tokens in 3 rounds
- Not worth the token cost

**Resolution**:
- Run Prettier manually between sessions
- Format when you manually edit files anyway
- Avoid the token cost for marginal convenience

### 5.4. Planning Mode vs Manual Plans

**Position A**: Use built-in Planning Mode
- Dedicated mode gets better codebase research
- Structured plan output

**Position B**: Use manual planning with custom prompts
- Planning Mode can't see agent output
- Kills agent if you say "no" instead of continuing
- Custom slash commands give more control

**Resolution**:
- Start with Planning Mode for research phase
- Exit and create manual dev docs from results
- Use custom slash commands for plan refinement
- Best of both worlds

### 5.5. Documentation Volume

**Position A** (6_months_hardcore_use): Extensive documentation
- 850+ markdown files
- Multiple levels (broad architecture → specific implementations)
- Detailed API references

**Position B** (Multiple sources): Minimal, targeted documentation
- Skills for how-to patterns
- Docs only for project-specific architecture
- Avoid bloating context

**Resolution**:
- Volume depends on codebase size
- Use Skills for reusable patterns (HOW to build)
- Use Docs for project-specific architecture (WHAT exists)
- Progressive disclosure is key
- Point to docs rather than embedding

## 6. Appendix A: Source Mapping Table

| Practice | Sources (Count) | Priority |
|----------|----------------|----------|
| CLAUDE.md file | All 12 sources | ✅ High |
| Planning before coding | 8 sources | ✅ High |
| Context clearing | 6 sources | ✅ High |
| Test-Driven Development | 5 sources | ✅ High |
| Skills with auto-activation | 4 sources | ✅ High |
| Code review (self + human) | 5 sources | ✅ High |
| Hooks for quality gates | 4 sources | ✅ High |
| Dev docs system | 4 sources | ✅ High |
| Simple control loops | 3 sources | ✅ High |
| LLM search over RAG | 2 sources | ⚠️ Medium |
| Git worktrees | 3 sources | ⚠️ Medium |
| Headless mode | 2 sources | ⚠️ Medium |
| Multi-Claude verification | 3 sources | ⚠️ Medium |
| PM2 for services | 1 source | ❌ Low |
| Voice-to-text | 1 source | ❌ Low |

## 7. Appendix B: Complete Recommendation Set

### 7.1. Essential Practices (Do These First)

1. **Create CLAUDE.md** (100-200 lines max, document what Claude gets wrong)
2. **Use Planning Mode** (or custom planning workflow before any coding)
3. **Clear context aggressively** (at 60k tokens or 30% threshold)
4. **Write tests first** (TDD with failing tests → implementation)
5. **Be specific** (detailed instructions beat vague descriptions)
6. **Review all code** (manual human review is non-negotiable)

### 7.2. High-Impact Practices (Implement Soon)

7. **Dev docs system** (plan.md, context.md, tasks.md for features)
8. **Skills with auto-activation hooks** (see 6_months_hardcore_use examples)
9. **Quality gate hooks** (build checker, test runner, error reminder)
10. **Slash commands** (/catchup, /dev-docs, /code-review, /pr)
11. **Visual references** (screenshots, design mocks for UI work)
12. **Subagent delegation** (start with Task(...) clone pattern)
13. **Course correction** (learn ESC, double-ESC, undo patterns)

### 7.3. Advanced Practices (For Experienced Users)

14. **Git worktrees** (parallel development on independent features)
15. **Multi-Claude verification** (separate contexts for write/review)
16. **Headless mode** (CI/CD automation, issue triage)
17. **Custom MCP servers** (minimal tools, token-efficient, gateway pattern)
18. **PM2 for microservices** (log access, process management)
19. **Utility scripts in Skills** (attach ready-to-use tools)
20. **Living documentation** (update plans during implementation)

### 7.4. Practices to Avoid

❌ **Auto-formatting hooks** (consumes excessive tokens)
❌ **Heavy MCP usage** (>20k tokens cripples context)
❌ **Complex multi-agent systems** (debugging nightmare)
❌ **RAG for code search** (LLM search is simpler and better)
❌ **Vague instructions** (leads to vague results)
❌ **Skipping planning** (jumping straight to code)
❌ **Letting context fill to limits** (quality degrades)

## 8. Appendix C: Quick Start Workflow

For engineers new to Claude Code who want production-quality results:

### 8.1. Week 1: Foundations
1. Create CLAUDE.md with project commands and testing instructions
2. Practice Planning Mode → review → implement → commit workflow
3. Start clearing context at 60k tokens
4. Review all AI-generated code manually

### 8.2. Week 2: Quality Systems
5. Set up TDD workflow (tests first, commit separately)
6. Create 2-3 custom slash commands for common tasks
7. Implement basic build checker hook
8. Add visual references to UI work

### 8.3. Week 3: Advanced Context
9. Implement dev docs system (plan/context/tasks files)
10. Create 1-2 Skills for your most common patterns
11. Add auto-activation hook for skills
12. Practice using subagents for code review

### 8.4. Week 4: Optimization
13. Audit your context usage (/context mid-session)
14. Optimize CLAUDE.md (remove bloat, add pointers)
15. Add quality gate hooks (tests, linting)
16. Experiment with git worktrees for parallel work

## 9. Appendix D: Measuring Success

### 9.1. Context Efficiency Metrics
- Baseline context cost: <20k tokens (10% of 200k)
- CLAUDE.md size: <2000 tokens
- MCP tools total: <20k tokens
- Context clearing frequency: Every 60k tokens or less

### 9.2. Code Quality Metrics
- Test coverage: >80% for new code
- TypeScript errors: Zero before commits (enforced by hooks)
- Code review findings: Track common issues, update CLAUDE.md
- Production bugs from AI code: Should decrease over time

### 9.3. Productivity Metrics
- Time from plan to PR: Track and optimize
- Number of plan iterations: Should stabilize at 1-3
- Context compactions needed: Should decrease with better practices
- Parallel tasks with worktrees: Can scale to 3-4 simultaneously

## 10. Conclusion

Claude Code is a powerful tool that amplifies both good and bad practices. The most successful users:

1. **Obsess over context management** - It's the primary failure mode
2. **Plan rigorously before coding** - Vibe coding creates technical debt
3. **Keep systems simple** - Complexity makes LLMs exponentially harder to debug
4. **Implement quality gates** - Hooks and reviews catch errors early
5. **Iterate continuously** - Refine CLAUDE.md, skills, and workflows based on what Claude gets wrong

The difference between frustration and productivity isn't the tool—it's how you use it. Invest time in your infrastructure (CLAUDE.md, skills, hooks, docs), and you'll build production-quality code with confidence.
