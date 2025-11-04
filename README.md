# Claude Code Best Practices

This is a simple repo to collate various articles/blog posts about the best ways to use Claude Code. This body of knowledge is then synthesized and summarized into [claudecode_bestpractices.md](claudecode_bestpractices.md) by Claude Code itself.

Given Claude Code is only a few months old now and agentic coding is still very much a nascent domain, the intent is to have this repo stay live/current. Please consider contributing/participating as detailed below.

## Process

### Source Acquisition

Mostly through encountering top performing (lot of upvotes) posts on Hackernews and Reddit. 

### Source Content Fetching

The content from each source is fetched through `article_fetcher.py`.

### Analysis

Claude Code (using Opus 4.1) is asked to analyze the source content with this [prompt](analysis_prompt.md).  The prompt was initially written by me, then reviewed/enhanced by Claude Code, then reviewed, edited and finalized by me.

### Output

Is available here

## Contributing

If you find any errors, issues or have alternate approaches to the current practices, please open a GitHub Issue.

Please use the discussion section to suggest new articles to include in this repo or add new tips, practices etc.

## Roadmap

- [ ] Automate summary update when new sources are added
- [ ] Codify synthesis+summarization prompt
- [ ] Update content based on discussions in GitHub Issues and Discussions sections