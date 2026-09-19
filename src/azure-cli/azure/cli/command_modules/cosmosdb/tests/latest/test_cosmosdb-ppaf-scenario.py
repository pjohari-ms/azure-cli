# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import Mock

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
from azure.cli.testsdk.scenario_tests import AllowLargeResponse


class TestCosmosdbPerPartitionAutomaticFailoverModel(unittest.TestCase):

    def test_create_and_update_use_generated_sdk_models(self):
        from azure.cli.command_modules.cosmosdb.custom import (
            _create_database_account,
            cli_cosmosdb_update,
        )
        from azure.mgmt.cosmosdb.models import (
            ConsistencyPolicy,
            DatabaseAccountCreateUpdateParameters,
            DatabaseAccountGetResults,
            DatabaseAccountUpdateParameters,
        )

        client = Mock()
        client.begin_create_or_update.return_value.result.return_value = object()
        _create_database_account(
            client=client,
            resource_group_name='resource-group',
            account_name='account',
            arm_location='westus',
            enable_per_partition_automatic_failover=True)

        create_request = client.begin_create_or_update.call_args.args[2]
        self.assertIsInstance(create_request, DatabaseAccountCreateUpdateParameters)
        self.assertTrue(create_request.per_partition_automatic_failover_enabled)
        self.assertTrue(
            create_request.as_dict()['properties']['perPartitionAutomaticFailoverEnabled'])

        client.reset_mock()
        client.get.return_value = DatabaseAccountGetResults(
            consistency_policy=ConsistencyPolicy(
                default_consistency_level='Session',
                max_staleness_prefix=100,
                max_interval_in_seconds=5),
            backup_policy=None)
        client.begin_update.return_value.result.return_value = object()
        cli_cosmosdb_update(
            client=client,
            resource_group_name='resource-group',
            account_name='account',
            enable_per_partition_automatic_failover=False)

        update_request = client.begin_update.call_args.args[2]
        self.assertIsInstance(update_request, DatabaseAccountUpdateParameters)
        self.assertFalse(update_request.per_partition_automatic_failover_enabled)
        self.assertFalse(
            update_request.as_dict()['properties']['perPartitionAutomaticFailoverEnabled'])


class CosmosdbPerPartitionAutomaticFailoverScenarioTest(ScenarioTest):

    @AllowLargeResponse()
    @ResourceGroupPreparer(name_prefix='cli_test_cosmosdb_ppaf', location='southcentralus')
    def test_cosmosdb_per_partition_automatic_failover(self, resource_group):
        self.kwargs.update({
            'acc': self.create_random_name(prefix='ppaf-test-', length=20)
        })

        self.cmd(
            'az cosmosdb create -n {acc} -g {rg} '
            '--locations regionName=southcentralus failoverPriority=0 '
            '--locations regionName=eastus failoverPriority=1 '
            '--enable-per-partition-automatic-failover true')
        self.cmd('az cosmosdb show -n {acc} -g {rg}', checks=[
            self.check('perPartitionAutomaticFailoverEnabled', True),
        ])

        self.cmd('az cosmosdb update -n {acc} -g {rg} --tags ppaf=preserved')
        self.cmd('az cosmosdb show -n {acc} -g {rg}', checks=[
            self.check('perPartitionAutomaticFailoverEnabled', True),
        ])

        self.cmd(
            'az cosmosdb update -n {acc} -g {rg} '
            '--enable-per-partition-automatic-failover false')
        self.cmd('az cosmosdb show -n {acc} -g {rg}', checks=[
            self.check('perPartitionAutomaticFailoverEnabled', False),
        ])

        self.cmd('az cosmosdb delete -n {acc} -g {rg} --yes')