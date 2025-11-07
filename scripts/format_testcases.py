#!/usr/bin/env python3
"""
Script to format test cases from TestRigor API response into readable files.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def format_timestamp(timestamp_str):
    """Format ISO timestamp to readable format."""
    if not timestamp_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return timestamp_str


def format_test_case(test_case):
    """Format a single test case into readable markdown."""
    content = []
    
    # Header
    content.append(f"# {test_case.get('description', 'Untitled Test Case')}\n")
    
    # Metadata
    content.append("## Metadata\n")
    content.append(f"- **UUID**: `{test_case.get('uuid', 'N/A')}`")
    content.append(f"- **Status**: {'🚫 Disabled' if test_case.get('disabled') else '✅ Enabled'}")
    content.append(f"- **Created**: {format_timestamp(test_case.get('createdAt'))}")
    
    created_by = test_case.get('createdBy', {})
    if created_by:
        content.append(f"- **Created By**: {created_by.get('name', 'N/A')} ({created_by.get('email', 'N/A')})")
    
    if test_case.get('modifiedAt'):
        content.append(f"- **Modified**: {format_timestamp(test_case.get('modifiedAt'))}")
        modified_by = test_case.get('modifiedBy', {})
        if modified_by:
            content.append(f"- **Modified By**: {modified_by.get('name', 'N/A')} ({modified_by.get('email', 'N/A')})")
    
    # Labels
    labels = test_case.get('labels', [])
    if labels:
        content.append(f"- **Labels**: {', '.join(labels)}")
    
    content.append("")
    
    # Custom Steps
    content.append("## Test Steps\n")
    custom_steps = test_case.get('customSteps', '')
    if custom_steps:
        content.append("```")
        content.append(custom_steps)
        content.append("```")
    else:
        content.append("*No steps defined*")
    
    content.append("")
    
    return '\n'.join(content)


def create_index(test_cases, metadata):
    """Create an index file with summary of all test cases."""
    content = []
    
    content.append("# Test Cases Index\n")
    content.append(f"**Last Updated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    content.append(f"**Total Test Cases**: {metadata.get('totalElements', len(test_cases))}\n")
    content.append("---\n")
    
    # Sort by creation date (newest first)
    sorted_cases = sorted(
        test_cases,
        key=lambda x: x.get('createdAt', ''),
        reverse=True
    )
    
    for i, tc in enumerate(sorted_cases, 1):
        status_icon = '🚫' if tc.get('disabled') else '✅'
        desc = tc.get('description', 'Untitled')
        uuid = tc.get('uuid', 'N/A')
        created = format_timestamp(tc.get('createdAt'))
        
        content.append(f"## {i}. {status_icon} {desc}\n")
        content.append(f"- **UUID**: `{uuid}`")
        content.append(f"- **File**: [`{uuid}.md`](./{uuid}.md)")
        content.append(f"- **Created**: {created}")
        
        # Count steps
        steps = tc.get('customSteps', '')
        step_count = len([s for s in steps.split('\n') if s.strip()]) if steps else 0
        content.append(f"- **Steps**: {step_count}")
        
        content.append("")
    
    return '\n'.join(content)


def main():
    """Main function to process test cases."""
    # Read the API response
    response_file = Path('test-cases-response.json')
    if not response_file.exists():
        print("❌ Error: test-cases-response.json not found!")
        exit(1)
    
    try:
        with open(response_file, 'r', encoding='utf-8') as f:
            response = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        exit(1)
    
    print(f"📥 API Response received")
    print(f"   Status: {response.get('status')}")
    
    # Extract test cases
    test_cases = response.get('data', {}).get('content', [])
    
    if not test_cases:
        print("⚠️  No test cases found in response")
        print(f"   Response keys: {list(response.keys())}")
        if 'data' in response:
            print(f"   Data keys: {list(response['data'].keys())}")
        return
    
    print(f"✅ Found {len(test_cases)} test case(s)")
    
    # Create output directory
    output_dir = Path('test-cases')
    output_dir.mkdir(exist_ok=True)
    
    # Clear existing files (optional - comment out to keep old versions)
    for old_file in output_dir.glob('*.md'):
        old_file.unlink()
    
    # Save each test case
    for tc in test_cases:
        uuid = tc.get('uuid')
        if not uuid:
            print(f"⚠️  Skipping test case without UUID")
            continue
        
        filename = output_dir / f"{uuid}.md"
        content = format_test_case(tc)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        desc = tc.get('description', 'Untitled')
        print(f"   📝 {desc}")
    
    # Create index file
    metadata = response.get('data', {})
    index_content = create_index(test_cases, metadata)
    index_file = output_dir / 'INDEX.md'
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"📋 Created index file")
    print(f"\n🎉 Successfully processed {len(test_cases)} test cases!")


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
