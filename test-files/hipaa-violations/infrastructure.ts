/**
 * Healthcare Infrastructure Stack
 * WARNING: This file contains intentional HIPAA violations for testing purposes
 */

import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class HealthcareInfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VIOLATION 1: VPC without proper network segmentation
    const vpc = new ec2.Vpc(this, 'HealthcareVPC', {
      maxAzs: 2,
      // VIOLATION 2: No private subnets for PHI data
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,  // All resources in public subnets
        },
      ],
    });

    // VIOLATION 3: Security group allows unrestricted access
    const dbSecurityGroup = new ec2.SecurityGroup(this, 'DBSecurityGroup', {
      vpc,
      description: 'Security group for patient database',
      allowAllOutbound: true,
    });

    // VIOLATION 4: Allowing access from anywhere
    dbSecurityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),  // 0.0.0.0/0
      ec2.Port.tcp(5432),
      'Allow PostgreSQL from anywhere'
    );

    // VIOLATION 5: RDS without encryption at rest
    const patientDatabase = new rds.DatabaseInstance(this, 'PatientDB', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_14,
      }),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC,  // VIOLATION 6: Database in public subnet
      },
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T3,
        ec2.InstanceSize.MICRO
      ),
      // VIOLATION 7: No encryption at rest
      storageEncrypted: false,
      
      // VIOLATION 8: Publicly accessible database
      publiclyAccessible: true,
      
      // VIOLATION 9: No automated backups
      backupRetention: cdk.Duration.days(0),
      
      // VIOLATION 10: Deletion without protection
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      deletionProtection: false,
      
      // VIOLATION 11: No multi-AZ for high availability
      multiAz: false,
      
      // VIOLATION 12: Hardcoded credentials
      credentials: rds.Credentials.fromPassword(
        'admin',
        cdk.SecretValue.unsafePlainText('Hospital123!')  // Hardcoded password
      ),
    });

    // VIOLATION 13: S3 bucket without encryption
    const patientDataBucket = new s3.Bucket(this, 'PatientDataBucket', {
      // VIOLATION 14: No encryption at rest
      encryption: s3.BucketEncryption.UNENCRYPTED,
      
      // VIOLATION 15: Public read access
      publicReadAccess: true,
      
      // VIOLATION 16: No versioning for audit trail
      versioned: false,
      
      // VIOLATION 17: No lifecycle policy for data retention
      lifecycleRules: [],
      
      // VIOLATION 18: No access logging
      serverAccessLogsPrefix: undefined,
      
      // VIOLATION 19: Bucket can be deleted with data
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      
      // VIOLATION 20: No MFA delete requirement
      // VIOLATION 21: CORS allows all origins
      cors: [
        {
          allowedOrigins: ['*'],
          allowedMethods: [s3.HttpMethods.GET, s3.HttpMethods.PUT, s3.HttpMethods.POST],
          allowedHeaders: ['*'],
        },
      ],
    });

    // VIOLATION 22: Lambda without encryption for environment variables
    const patientApiFunction = new lambda.Function(this, 'PatientAPI', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
def handler(event, context):
    # VIOLATION 23: Logging PHI in Lambda
    print(f"Processing patient data: {event}")
    return {"statusCode": 200, "body": "OK"}
      `),
      environment: {
        // VIOLATION 24: Hardcoded credentials in environment
        DB_HOST: patientDatabase.dbInstanceEndpointAddress,
        DB_USER: 'admin',
        DB_PASSWORD: 'Hospital123!',
        DB_NAME: 'patients',
        // VIOLATION 25: API keys in plain text
        EXTERNAL_API_KEY: 'sk_live_1234567890abcdef',
      },
      // VIOLATION 26: No VPC configuration for Lambda
      // VIOLATION 27: Excessive timeout
      timeout: cdk.Duration.minutes(15),
      
      // VIOLATION 28: CloudWatch logs without encryption
      logRetention: logs.RetentionDays.INFINITE,  // VIOLATION 29: Infinite retention
    });

    // VIOLATION 30: Overly permissive IAM policy
    patientApiFunction.addToRolePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['*'],  // All actions
        resources: ['*'],  // All resources
      })
    );

    // VIOLATION 31: API Gateway without authentication
    const api = new apigateway.RestApi(this, 'PatientAPI', {
      restApiName: 'Patient Service',
      description: 'API for patient data management',
      
      // VIOLATION 32: No API key requirement
      // VIOLATION 33: No request validation
      // VIOLATION 34: No throttling
      deployOptions: {
        // VIOLATION 35: No access logging
        accessLogDestination: undefined,
        
        // VIOLATION 36: Detailed error messages
        dataTraceEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        
        // VIOLATION 37: No throttling limits
        throttlingBurstLimit: undefined,
        throttlingRateLimit: undefined,
      },
    });

    // VIOLATION 38: API endpoint without authorization
    const patients = api.root.addResource('patients');
    patients.addMethod('GET', new apigateway.LambdaIntegration(patientApiFunction), {
      // VIOLATION 39: No authorization
      authorizationType: apigateway.AuthorizationType.NONE,
      
      // VIOLATION 40: No API key required
      apiKeyRequired: false,
    });

    patients.addMethod('POST', new apigateway.LambdaIntegration(patientApiFunction), {
      authorizationType: apigateway.AuthorizationType.NONE,
    });

    // VIOLATION 41: CloudWatch log group without encryption
    new logs.LogGroup(this, 'APILogs', {
      logGroupName: '/aws/apigateway/patient-api',
      retention: logs.RetentionDays.INFINITE,  // VIOLATION 42: Infinite retention
      // VIOLATION 43: No KMS encryption
      encryptionKey: undefined,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // VIOLATION 44: EC2 instance for processing PHI
    const processingInstance = new ec2.Instance(this, 'ProcessingServer', {
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC,  // VIOLATION 45: Public subnet
      },
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T3,
        ec2.InstanceSize.MEDIUM
      ),
      machineImage: ec2.MachineImage.latestAmazonLinux(),
      
      // VIOLATION 46: No encryption for EBS volumes
      blockDevices: [
        {
          deviceName: '/dev/xvda',
          volume: ec2.BlockDeviceVolume.ebs(20, {
            encrypted: false,  // Unencrypted volume
          }),
        },
      ],
      
      // VIOLATION 47: SSH access from anywhere
      keyName: 'my-key-pair',
    });

    // VIOLATION 48: Security group allowing SSH from anywhere
    processingInstance.connections.allowFromAnyIpv4(
      ec2.Port.tcp(22),
      'Allow SSH from anywhere'
    );

    // VIOLATION 49: Security group allowing HTTP (not HTTPS)
    processingInstance.connections.allowFromAnyIpv4(
      ec2.Port.tcp(80),
      'Allow HTTP from anywhere'
    );

    // VIOLATION 50: No CloudTrail for audit logging
    // VIOLATION 51: No AWS Config for compliance monitoring
    // VIOLATION 52: No GuardDuty for threat detection
    // VIOLATION 53: No AWS WAF for API protection
    // VIOLATION 54: No VPC Flow Logs
    // VIOLATION 55: No Systems Manager Session Manager (using SSH instead)

    // Outputs with sensitive information
    // VIOLATION 56: Exposing database endpoint
    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: patientDatabase.dbInstanceEndpointAddress,
      description: 'Patient database endpoint',
    });

    // VIOLATION 57: Exposing database credentials
    new cdk.CfnOutput(this, 'DatabasePassword', {
      value: 'Hospital123!',
      description: 'Database password',
    });

    // VIOLATION 58: Exposing S3 bucket name
    new cdk.CfnOutput(this, 'PatientDataBucket', {
      value: patientDataBucket.bucketName,
      description: 'S3 bucket for patient data',
    });

    // VIOLATION 59: Exposing API endpoint without authentication info
    new cdk.CfnOutput(this, 'APIEndpoint', {
      value: api.url,
      description: 'Patient API endpoint (no auth required)',
    });
  }
}
