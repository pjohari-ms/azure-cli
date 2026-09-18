# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer


class CosmosdbThroughputBucketsScenarioTest(ScenarioTest):

    @ResourceGroupPreparer(name_prefix='cli_test_cosmosdb_throughput_buckets')
    def test_cosmosdb_throughput_buckets_stable_api(self, resource_group):
        self.kwargs.update({
            'acc': self.create_random_name(prefix='buckets-', length=20),
            'db_name': self.create_random_name(prefix='database-', length=20),
            'ctn_name': self.create_random_name(prefix='container-', length=20),
            'throughput_buckets': '"[{\\"id\\": 1, \\"maxThroughputPercentage\\": 10, '
                                  '\\"isDefaultBucket\\": true}, {\\"id\\": 2, '
                                  '\\"maxThroughputPercentage\\": 20, \\"isDefaultBucket\\": false}, '
                                  '{\\"id\\": 3, \\"maxThroughputPercentage\\": 15}]"',
            'empty_throughput_buckets': '"[]"'
        })

        self.cmd('az cosmosdb create -n {acc} -g {rg}')
        self.cmd('az cosmosdb sql database create -g {rg} -a {acc} -n {db_name}')
        self.cmd(
            'az cosmosdb sql container create -g {rg} -a {acc} -d {db_name} '
            '-n {ctn_name} -p /partitionKey --throughput 400')
        self.cmd(
            'az cosmosdb sql container throughput update -g {rg} -a {acc} '
            '-d {db_name} -n {ctn_name} --throughput 400 '
            '--throughput-buckets {throughput_buckets}')

        bucket_checks = [
            self.check('resource.throughputBuckets[0].id', 1),
            self.check('resource.throughputBuckets[0].maxThroughputPercentage', 10),
            self.check('resource.throughputBuckets[0].isDefaultBucket', True),
            self.check('resource.throughputBuckets[1].id', 2),
            self.check('resource.throughputBuckets[1].maxThroughputPercentage', 20),
            self.check('resource.throughputBuckets[1].isDefaultBucket', False),
            self.check('resource.throughputBuckets[2].id', 3),
            self.check('resource.throughputBuckets[2].maxThroughputPercentage', 15),
        ]
        self.cmd(
            'az cosmosdb sql container throughput show -g {rg} -a {acc} '
            '-d {db_name} -n {ctn_name}',
            checks=bucket_checks)
        self.cmd(
            'az cosmosdb sql container throughput update -g {rg} -a {acc} '
            '-d {db_name} -n {ctn_name} --throughput 800')
        self.cmd(
            'az cosmosdb sql container throughput show -g {rg} -a {acc} '
            '-d {db_name} -n {ctn_name}',
            checks=bucket_checks + [self.check('resource.throughput', 800)])

        self.cmd(
            'az cosmosdb sql container throughput update -g {rg} -a {acc} '
            '-d {db_name} -n {ctn_name} --throughput 800 '
            '--throughput-buckets {empty_throughput_buckets}')
        self.cmd(
            'az cosmosdb sql container throughput show -g {rg} -a {acc} '
            '-d {db_name} -n {ctn_name}',
            checks=[self.check('length(resource.throughputBuckets)', 0)])

        self.cmd('az cosmosdb delete -n {acc} -g {rg} --yes')
