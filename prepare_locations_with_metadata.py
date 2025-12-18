#!/usr/bin/env python3
"""Prepare location documents with metadata for Bedrock Knowledge Base ingestion."""

import json
import logging
import uuid
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


def generate_location_metadata(location: Dict[str, Any], location_id: str, article_hash: str) -> Dict[str, Any]:
    """Generate Bedrock-compatible metadata for a location."""
    
    # Extract basic info
    display_name = location.get('displayName', 'Unknown Location') if location.get('displayName', 'Unknown Location') else 'unknown'
    categories = location.get('categories', []) if location.get('categories', []) else []
    primary_category = location.get('primaryCategory', 'general') if location.get('primaryCategory', 'general') else 'unknown'
    
    # Extract address info
    address_data = location.get('address', {})
    city = address_data.get('city', 'unknown') if address_data.get('city', 'unknown') else 'unknown'
    country = address_data.get('country', 'unknown') if address_data.get('country', 'unknown') else 'unknown'
    
    # Extract coordinates
    coords = location.get('coordinates', {})
    latitude = coords.get('latitude', 0.0) if coords.get('latitude', 0.0) else 0.0
    longitude = coords.get('longitude', 0.0) if coords.get('longitude', 0.0) else 0.0

    
    # Ensure arrays have at least one value (Bedrock requirement)
    if not categories:
        categories = ["general"]
    
    # Build metadata in AWS Bedrock format
    metadata = {
        "metadataAttributes": {
            "locationId": str(location_id),
            "article_hash": article_hash,
            "displayName": display_name,
            "categories":categories[:10],  # Limit to 10
            "primaryCategory": primary_category,
            "city": city,
            "country": country,
            "latitude": latitude,
            "longitude": longitude
        }
    }
    
    return metadata


def main():
    """Prepare location documents with metadata."""
    
    # Load config
    config = load_config()
    
    # Load locations
    logger.info("Loading locations from global_locations.json...")
    with open('global_locations.json', 'r') as f:
        json_data = json.load(f)
    
    # Handle Firestore export format
    if isinstance(json_data, dict) and 'data' in json_data:
        locations_dict = json_data['data']
    else:
        locations_dict = json_data
    
    logger.info(f"Found {len(locations_dict)} locations")

    
    # Create output directory
    output_dir = Path('documents_to_upload/locations')
    output_dir.mkdir(exist_ok=True)
    
    # Process locations
    processed = 0
    skipped = 0
    
    for location_id, location_data in locations_dict.items():
        try:
            collections = location_data.get('__collections__', {})
            mentions = collections.get('contextual_mentions', {})
            
            for article_hash, mention_data in mentions.items():
                chunks = mention_data.get('chunks', [])
                chunk_texts = []
                for chunk in chunks:
                    chunk_text = chunk.get('chunkText', '').strip()
                    if chunk_text:
                        chunk_texts.append(chunk_text)

                content = "\n".join(chunk_texts)
                random_id = uuid.uuid4()
                # Save document content (plain text only)
                doc_file = output_dir / f"{random_id}.txt"
                with open(doc_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Generate and save metadata
                metadata = generate_location_metadata(location=location_data, 
                                                      location_id=location_id,
                                                      article_hash=article_hash)
                metadata_file = output_dir / f"{random_id}.txt.metadata.json"
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                # Upload to S3

                prefix = "locations/"
                s3_article_key = f"{prefix}{random_id}.txt"
                s3_client.put_object(Bucket=config.s3.data_bucket_name,
                                     Key=s3_article_key,
                                     Body=content)
                
                s3_metadata_key = f"{prefix}{random_id}.txt.metadata.json"
                s3_client.put_object(Bucket=config.s3.data_bucket_name,
                                     Key=s3_metadata_key,
                                     Body=json.dumps(metadata))
            
            processed += 1
            
            if processed % 50 == 0:
                logger.info(f"Processed {processed} locations...")
        
        except Exception as e:
            logger.error(f"Error processing location {location_id}: {e}")
            skipped += 1
            continue
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Location document preparation complete!")
    logger.info(f"{'='*60}")
    logger.info(f"Processed: {processed} locations")
    logger.info(f"Skipped: {skipped} locations")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Files created: {processed * 2} (txt + metadata.json pairs)")
    logger.info(f"{'='*60}")
    
    return processed


if __name__ == "__main__":
    main()

#%%
temp = "Hello" if not None else "World"
print(temp)
# %%
