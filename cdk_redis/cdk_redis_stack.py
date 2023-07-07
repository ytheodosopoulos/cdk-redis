from aws_cdk import (
    # Duration,
    Stack,
    aws_elasticache as elasticache,
    aws_ec2 as ec2,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class CdkRedisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        const developmentVpc = ec2.Vpc.fromLookup(this, 'DevelopmentVPC', { vpcName: 'development' });

        redis_sg = ec2.SecurxityGroup(
            self,
            "redis-sg",
            security_group_name="redis-sg",
            vpc=ec2.Vpc.from_lookup(
                this,
                'PersonalVPC',
                tags={
                    'Environment': 'Development'
                }
            ),
            allow_all_outbound=True
        )

        private_subnets_ids = [ps.subnet_id for ps in developmentVpc.private_subnets]

        redis_subnet_group = elastiredis_clustercache.CfnSubnetGroup(
            scope=self,
            id="redis_subnet_group",
            subnet_ids=private_subnets_ids,
            description="subnet group for redis"
        )

        redis_sec_group.add_ingress_rule(
            peer='',
            description="Allow Redis connection",
            connection=ec2.Port.tcp(6379),            
        )

        redis_cluster = elasticache.CfnCacheCluster(
            scope=self,
            id="redis_cluster",
            engine="redis",
            cache_node_type="cache.t3.small",
            num_cache_nodes=1,
            cache_subnet_group_name=redis_subnet_group.ref,
            vpc_security_group_ids=[redis_sec_group.security_group_id],
        ) 
