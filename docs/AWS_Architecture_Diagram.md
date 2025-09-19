```mermaid
graph TB
    %% External Access
    Users[Users/Clients] --> CF[CloudFront CDN]
    DevTeam[Development Team] --> CodeCommit[AWS CodeCommit]
    
    %% CDN and Load Balancing
    CF --> ALB[Application Load Balancer<br/>Multi-AZ]
    
    %% VPC and Networking
    subgraph VPC["VPC (10.0.0.0/16)"]
        subgraph PublicSubnets["Public Subnets"]
            subgraph AZ1Public["AZ-1a (10.0.1.0/24)"]
                ALB
                NAT1[NAT Gateway]
            end
            subgraph AZ2Public["AZ-2b (10.0.2.0/24)"]
                NAT2[NAT Gateway]
            end
        end
        
        subgraph PrivateSubnets["Private Subnets"]
            subgraph AZ1Private["AZ-1a (10.0.10.0/24)"]
                subgraph ECS1["ECS Cluster"]
                    WebApp1[Web App Container<br/>t3.medium]
                    API1[API Container<br/>t3.small]
                end
                Redis1[ElastiCache Redis<br/>cache.t3.micro]
            end
            
            subgraph AZ2Private["AZ-2b (10.0.20.0/24)"]
                subgraph ECS2["ECS Cluster"]
                    WebApp2[Web App Container<br/>t3.medium]
                    API2[API Container<br/>t3.small]
                end
                Redis2[ElastiCache Redis<br/>cache.t3.micro]
            end
        end
        
        subgraph DatabaseSubnets["Database Subnets"]
            subgraph AZ1DB["AZ-1a (10.0.30.0/24)"]
                RDSPrimary[RDS PostgreSQL<br/>db.t3.medium<br/>Primary]
            end
            subgraph AZ2DB["AZ-2b (10.0.40.0/24)"]
                RDSSecondary[RDS PostgreSQL<br/>db.t3.medium<br/>Read Replica]
            end
        end
    end
    
    %% Container Orchestration
    ALB --> ECS1
    ALB --> ECS2
    
    %% Database Connections
    ECS1 --> RDSPrimary
    ECS2 --> RDSPrimary
    RDSPrimary --> RDSSecondary
    
    %% Cache Connections
    ECS1 --> Redis1
    ECS2 --> Redis2
    
    %% Storage
    ECS1 --> S3[S3 Bucket<br/>Static Assets & Logs<br/>Versioning Enabled]
    ECS2 --> S3
    
    %% Secrets Management
    ECS1 --> SM[AWS Secrets Manager<br/>DB Credentials<br/>API Keys]
    ECS2 --> SM
    
    %% CI/CD Pipeline
    subgraph CICD["CI/CD Pipeline"]
        CodeCommit --> CodeBuild[AWS CodeBuild<br/>Build & Test]
        CodeBuild --> ECR[Amazon ECR<br/>Container Registry]
        ECR --> CodeDeploy[AWS CodeDeploy<br/>Blue/Green Deployment]
        CodeDeploy --> ECS1
        CodeDeploy --> ECS2
    end
    
    %% Monitoring and Logging
    subgraph Monitoring["Monitoring & Logging"]
        CW[CloudWatch<br/>Metrics & Alarms]
        CWLogs[CloudWatch Logs<br/>Application Logs]
        XRay[AWS X-Ray<br/>Distributed Tracing]
    end
    
    ECS1 --> CW
    ECS2 --> CW
    ECS1 --> CWLogs
    ECS2 --> CWLogs
    ECS1 --> XRay
    ECS2 --> XRay
    
    %% Security
    subgraph Security["Security Layer"]
        WAF[AWS WAF<br/>Web Application Firewall]
        KMS[AWS KMS<br/>Encryption Keys]
        IAM[IAM Roles & Policies<br/>Least Privilege Access]
    end
    
    CF --> WAF
    SM --> KMS
    S3 --> KMS
    RDSPrimary --> KMS
    
    %% Auto Scaling
    subgraph AutoScaling["Auto Scaling"]
        ASG[Auto Scaling Group<br/>Min: 2, Max: 10<br/>Target: CPU 70%]
        ECSAutoScaling[ECS Service Auto Scaling<br/>Target Tracking]
    end
    
    ASG --> ECS1
    ASG --> ECS2
    ECSAutoScaling --> ECS1
    ECSAutoScaling --> ECS2
    
    %% Backup and DR
    subgraph BackupDR["Backup & DR"]
        RDSBackup[RDS Automated Backups<br/>7-day retention]
        S3Backup[S3 Cross-Region Replication<br/>to us-west-2]
    end
    
    RDSPrimary --> RDSBackup
    S3 --> S3Backup
    
    %% Network Security
    IGW[Internet Gateway] --> PublicSubnets
    PrivateSubnets --> NAT1
    PrivateSubnets --> NAT2
    
    %% Security Groups (represented as styling)
    classDef publicSubnet fill:#e1f5fe
    classDef privateSubnet fill:#f3e5f5
    classDef database fill:#fff3e0
    classDef security fill:#ffebee
    classDef monitoring fill:#e8f5e8
    classDef storage fill:#fff8e1
    
    class AZ1Public,AZ2Public publicSubnet
    class AZ1Private,AZ2Private privateSubnet
    class AZ1DB,AZ2DB database
    class Security,WAF,KMS,IAM security
    class Monitoring,CW,CWLogs,XRay monitoring
    class S3,ECR storage