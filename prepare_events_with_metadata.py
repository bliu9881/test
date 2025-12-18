#!/usr/bin/env python3
"""Prepare event documents with metadata for Bedrock Knowledge Base ingestion."""

import json
import logging
import boto3
from pathlib import Path
from typing import Dict, Any, List
from src.config import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()
s3_client = boto3.client(
        's3',
        region_name=config.aws.region,
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key
    )


def generate_event_metadata(event: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Bedrock-compatible metadata for an event."""
    
    # Extract basic info
    article_hash = event.get('articleHashes', 'unknown')[0] if event.get('articleHashes', 'unknown')[0] else 'unknown'
    location_id = event.get('linkedLocationId', 'unknown') if event.get('linkedLocationId', 'unknown') else 'unknown'
    category = event.get('category', 'general') if event.get('category', 'general') else 'general'
    display_name = event.get("linkedLocationName", 'unknown') if event.get("linkedLocationName", 'unknown') else 'unknown'
    
    # Build metadata in AWS Bedrock format
    metadata = {
        "metadataAttributes": {
            "locationId": str(location_id),
            "article_hash": article_hash,
            "displayName": display_name,
            "categories":[category],  # Limit to 10
        }
    }
    
    return metadata


def main():
    """Prepare event documents with metadata."""
    
    # Load config
    config = load_config()
    
    # Load events
    logger.info("Loading events from global_events.json...")
    with open('global_events.json', 'r') as f:
        json_data = json.load(f)
    
    # Handle Firestore export format
    if isinstance(json_data, dict) and 'data' in json_data:
        events_dict = json_data['data']
    else:
        events_dict = json_data
    
    logger.info(f"Found {len(events_dict)} events")
    
    # Create output directory
    output_dir = Path('documents_to_upload/events')
    output_dir.mkdir(exist_ok=True)
    
    # Process events
    processed = 0
    skipped = 0
    
    for event_key, event_data in events_dict.items():
        try:
            # Extract all chunk texts
            chunk_texts = []
    
            collections = event_data.get('__collections__', {})
            mentions = collections.get('contextual_mentions', {})
            
            for article_hash, mention_data in mentions.items():
                mention_list = mention_data.get('mentions', [])
                for mention in mention_list:
                    chunk_text = mention.get('chunkText', '').strip()
                    if chunk_text:
                        chunk_texts.append(chunk_text)
            
            # Combine all chunk texts into document content
            content = "\n\n".join(chunk_texts)
            
            # Skip if content too short
            if len(content.strip()) < 50:
                skipped += 1
                continue
            
            event_hash = event_data.get('eventHash', event_key)
            
            # Save document content (plain text only)
            doc_file = output_dir / f"{event_hash}.txt"
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Generate and save metadata
            metadata = generate_event_metadata(event_data)
            metadata_file = output_dir / f"{event_hash}.txt.metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            prefix = "events/"
            s3_article_key = f"{prefix}{event_hash}.txt"
            s3_client.put_object(Bucket=config.s3.data_bucket_name,
                                    Key=s3_article_key,
                                    Body=content)
            
            s3_metadata_key = f"{prefix}{event_hash}.txt.metadata.json"
            s3_client.put_object(Bucket=config.s3.data_bucket_name,
                                    Key=s3_metadata_key,
                                    Body=json.dumps(metadata))
            
            processed += 1
            
            if processed % 10 == 0:
                logger.info(f"Processed {processed} events...")
        
        except Exception as e:
            logger.error(f"Error processing event {event_key}: {e}")
            skipped += 1
            continue
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Event document preparation complete!")
    logger.info(f"{'='*60}")
    logger.info(f"Processed: {processed} events")
    logger.info(f"Skipped: {skipped} events")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Files created: {processed * 2} (txt + metadata.json pairs)")
    logger.info(f"{'='*60}")
    
    return processed


if __name__ == "__main__":
    main()
