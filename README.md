# Claude Code Best Practices

This is a simple repo to summarize various articles/blog posts about the best ways to use Claude Code and synthesize this into a unified best practices guide here: [Claude Code Best Practices](index.md). This is authored by Claude Code itself.

Given Claude Code is only a few months old now and agentic coding is still very much a nascent domain, the intent is to have this repo stay live/current. Please consider contributing/participating as detailed below.

## Collation

Read the collation and analysis here:

rosmur.github.io/claudecode-best-practices/

## Process

### Source Acquisition

Mostly through encountering top performing (lot of upvotes) posts on Hackernews and Reddit. The current sources indexed are [here](sources.csv)

### Source Content Fetching

The content from each source is fetched through `article_fetcher.py`.

### Analysis

Claude Code (using Opus 4.1) is asked to analyze the source content with this [prompt](analysis-prompt.md).  The prompt was initially written by me, then reviewed/enhanced by Claude Code, then reviewed, edited and finalized by me.


## Contributing

If you have new sources to add, find any errors, issues or have feedback to the recommendations, please open a GitHub Issue.

Please use the discussion section to suggest new articles to include in this repo or add new tips, practices etc.

## Roadmap

- [ ] Automate summary update when new sources are added
- [x] Codify synthesis+summarization prompt
- [ ] Update content based on discussions in GitHub Issues and Discussions sections
