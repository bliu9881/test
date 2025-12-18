#!/usr/bin/env python3
"""Update data source to include both documents/ and locations/ prefixes."""

import boto3
import logging
from src.config import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Update the data source configuration."""
    
    config = load_config()
    
    kb_id = 'RNV8IF58LD'
    data_source_id = 'ZTFJOUHWFY'
    
    bedrock_agent = boto3.client(
        'bedrock-agent',
        region_name=config.aws.region,
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key
    )
    
    logger.info("Updating data source to include both prefixes...")
    logger.info(f"KB ID: {kb_id}")
    logger.info(f"Data Source ID: {data_source_id}")
    
    # Update data source with both prefixes
    response = bedrock_agent.update_data_source(
        knowledgeBaseId=kb_id,
        dataSourceId=data_source_id,
        name='hospitality-venues-s3-source',
        dataSourceConfiguration={
            's3Configuration': {
                'bucketArn': f"arn:aws:s3:::{config.s3.data_bucket_name}",
                'inclusionPrefixes': ['documents/', 'locations/']
            }
        }
    )
    
    logger.info("✓ Data source updated successfully!")
    logger.info(f"Inclusion prefixes: {response['dataSource']['dataSourceConfiguration']['s3Configuration']['inclusionPrefixes']}")
    logger.info("\nYou can now run the ingestion pipeline to index location documents.")


if __name__ == "__main__":
    main()
