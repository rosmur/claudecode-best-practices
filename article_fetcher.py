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
3) Check for which articles have already been retreived.
4) Fetch only the items that are not already retreived.
5) Save the fetched content into markdown files in a folder named "source_content"
6) Save fetch results into a csv in that folder that details if content was retreived from each link successfully and what the length in words and characters were of the retreeived content

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


def get_already_fetched_urls(results_csv: Path) -> set:
    """
    Read the results CSV and return a set of URLs that were successfully fetched.
    """
    already_fetched = set()

    if not results_csv.exists():
        return already_fetched

    try:
        with open(results_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only consider successfully fetched articles
                if row.get('success', '').lower() == 'true':
                    already_fetched.add(row['url'])
    except Exception as e:
        print(f"Warning: Could not read existing results CSV: {e}")

    return already_fetched


def main():
    """Main execution function."""
    # Setup paths
    script_dir = Path(__file__).parent
    sources_csv = script_dir / "sources.csv"
    output_dir = script_dir / "source_content"
    results_csv = output_dir / "fetch_results.csv"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Check for already fetched articles
    already_fetched = get_already_fetched_urls(results_csv)
    if already_fetched:
        print(f"Found {len(already_fetched)} already fetched articles. They will be skipped.\n")

    # Prepare results storage
    results = []

    # Load existing results if they exist
    if results_csv.exists():
        try:
            with open(results_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                results = list(reader)
                # Convert string 'True'/'False' to boolean for consistency
                for r in results:
                    r['success'] = r['success'].lower() == 'true'
        except Exception as e:
            print(f"Warning: Could not load existing results: {e}")
            results = []

    # Read sources CSV
    print("Reading sources.csv...")
    with open(sources_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sources = list(reader)

    # Filter out already fetched sources
    sources_to_fetch = [s for s in sources if s['source'] not in already_fetched]

    print(f"Found {len(sources)} total articles.")
    print(f"Already fetched: {len(already_fetched)}")
    print(f"To fetch: {len(sources_to_fetch)}\n")

    # Fetch each article (only the ones not already fetched)
    for idx, row in enumerate(sources_to_fetch, 1):
        title = row['title']
        url = row['source']

        print(f"[{idx}/{len(sources_to_fetch)}] Fetching: {title}")
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
    print(f"Saving results to {results_csv}...")

    with open(results_csv, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['title', 'url', 'success', 'filename', 'word_count', 'char_count', 'error']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Print summary
    newly_fetched = len([r for r in results if r['url'] not in already_fetched])
    total_successful = sum(1 for r in results if r['success'])
    total_failed = sum(1 for r in results if not r['success'])

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total articles in sources.csv: {len(sources)}")
    print(f"  Already fetched (skipped): {len(already_fetched)}")
    print(f"  Newly attempted: {len(sources_to_fetch)}")
    print(f"  Newly fetched successfully: {sum(1 for r in results if r['success'] and r['url'] not in already_fetched)}")
    print(f"  Total in results CSV: {len(results)}")
    print(f"    - Successful: {total_successful}")
    print(f"    - Failed: {total_failed}")
    print(f"  Results saved to: {results_csv}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
