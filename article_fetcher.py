#!/usr/bin/env python3
# /// script
# dependencies = [
#   "newspaper4k",
#   "lxml_html_clean",
# ]
# ///
"""
Article Fetcher

Author: Claude Code

Prompt:
write a python script that fetches article content from the @sources.csv file and complies to the following:

1) Use PEP-723 script header
2) Use newspaper4k library
3) Save the fetched content into markdown files in a folder named "source_content"
4) Save fetch results into a csv in that folder that details if content was retreived from each link successfully and what the length in words and characters were of the retreeived content

"""

import csv
import os
import re
from pathlib import Path
from newspaper import Article
from typing import List, Dict


def sanitize_filename(title: str) -> str:
    """Convert title to a safe filename."""
    # Remove or replace invalid filename characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces with underscores
    safe_title = safe_title.replace(' ', '_')
    # Limit length to avoid filesystem issues
    safe_title = safe_title[:100]
    return safe_title


def fetch_article(url: str) -> Dict[str, any]:
    """
    Fetch article content from URL using newspaper4k.

    Returns dict with success status, content, and metadata.
    """
    result = {
        'success': False,
        'title': '',
        'text': '',
        'authors': [],
        'publish_date': None,
        'error': None
    }

    try:
        article = Article(url)
        article.download()
        article.parse()

        result['success'] = True
        result['title'] = article.title
        result['text'] = article.text
        result['authors'] = article.authors
        result['publish_date'] = article.publish_date

    except Exception as e:
        result['error'] = str(e)

    return result


def save_to_markdown(title: str, content: str, url: str, output_dir: Path,
                     authors: List[str] = None, publish_date: str = None) -> str:
    """
    Save article content to a markdown file.

    Returns the filename used.
    """
    filename = f"{sanitize_filename(title)}.md"
    filepath = output_dir / filename

    # Build markdown content with metadata
    md_content = f"# {title}\n\n"
    md_content += f"**Source:** {url}\n\n"

    if authors:
        md_content += f"**Authors:** {', '.join(authors)}\n\n"

    if publish_date:
        md_content += f"**Published:** {publish_date}\n\n"

    md_content += "---\n\n"
    md_content += content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)

    return filename


def main():
    """Main execution function."""
    # Setup paths
    script_dir = Path(__file__).parent
    sources_csv = script_dir / "sources.csv"
    output_dir = script_dir / "source_content"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Prepare results storage
    results = []

    # Read sources CSV
    print("Reading sources.csv...")
    with open(sources_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sources = list(reader)

    print(f"Found {len(sources)} articles to fetch.\n")

    # Fetch each article
    for idx, row in enumerate(sources, 1):
        title = row['title']
        url = row['source']

        print(f"[{idx}/{len(sources)}] Fetching: {title}")
        print(f"  URL: {url}")

        # Fetch article
        article_data = fetch_article(url)

        if article_data['success']:
            # Get content stats
            text = article_data['text']
            word_count = len(text.split())
            char_count = len(text)

            # Save to markdown
            try:
                filename = save_to_markdown(
                    article_data['title'] or title,
                    text,
                    url,
                    output_dir,
                    article_data['authors'],
                    article_data['publish_date']
                )

                results.append({
                    'title': title,
                    'url': url,
                    'success': True,
                    'filename': filename,
                    'word_count': word_count,
                    'char_count': char_count,
                    'error': ''
                })

                print(f"  ✓ Success: {word_count} words, {char_count} characters")
                print(f"  Saved to: {filename}\n")

            except Exception as e:
                results.append({
                    'title': title,
                    'url': url,
                    'success': False,
                    'filename': '',
                    'word_count': 0,
                    'char_count': 0,
                    'error': f"Save error: {str(e)}"
                })
                print(f"  ✗ Failed to save: {str(e)}\n")
        else:
            results.append({
                'title': title,
                'url': url,
                'success': False,
                'filename': '',
                'word_count': 0,
                'char_count': 0,
                'error': article_data['error']
            })
            print(f"  ✗ Failed: {article_data['error']}\n")

    # Save results to CSV
    results_csv = output_dir / "fetch_results.csv"
    print(f"Saving results to {results_csv}...")

    with open(results_csv, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['title', 'url', 'success', 'filename', 'word_count', 'char_count', 'error']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Print summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total articles: {len(results)}")
    print(f"  Successfully fetched: {successful}")
    print(f"  Failed: {len(results) - successful}")
    print(f"  Results saved to: {results_csv}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
