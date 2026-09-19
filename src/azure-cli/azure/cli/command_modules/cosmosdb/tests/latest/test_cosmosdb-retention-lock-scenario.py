# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import datetime
import unittest
from unittest.mock import Mock

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
from azure.cli.testsdk.scenario_tests import AllowLargeResponse


class TestCosmosdbRetentionLockModel(unittest.TestCase):

    def test_create_and_update_use_generated_sdk_models(self):
        from azure.cli.command_modules.cosmosdb.custom import (
            _create_database_account,
            cli_cosmosdb_update,
        )
        from azure.mgmt.cosmosdb.models import (
            ConsistencyPolicy,
            ContinuousModeBackupPolicy,
            ContinuousModeProperties,
            DatabaseAccountCreateUpdateParameters,
            DatabaseAccountGetResults,
            DatabaseAccountUpdateParameters,
        )

        create_timestamp = datetime.datetime(2030, 1, 1, tzinfo=datetime.timezone.utc)
        client = Mock()
        client.begin_create_or_update.return_value.result.return_value = object()
        _create_database_account(
            client=client,
            resource_group_name='resource-group',
            account_name='account',
            arm_location='westus',
            backup_policy_type='Continuous',
            backup_retention_lock_expiration_timestamp='2030-01-01T00:00:00Z')

        create_request = client.begin_create_or_update.call_args.args[2]
        self.assertIsInstance(create_request, DatabaseAccountCreateUpdateParameters)
        self.assertIsInstance(create_request.backup_policy, ContinuousModeBackupPolicy)
        self.assertEqual(
            create_request.backup_policy.backup_retention_lock_expiration_timestamp,
            create_timestamp)
        self.assertEqual(
            create_request.as_dict()['properties']['backupPolicy']
            ['backupRetentionLockExpirationTimestamp'],
            '2030-01-01T00:00:00Z')

        update_timestamp = datetime.datetime(2030, 6, 1, tzinfo=datetime.timezone.utc)
        client.reset_mock()
        client.get.return_value = DatabaseAccountGetResults(
            consistency_policy=ConsistencyPolicy(
                default_consistency_level='Session',
                max_staleness_prefix=100,
                max_interval_in_seconds=5),
            backup_policy=ContinuousModeBackupPolicy(
                continuous_mode_properties=ContinuousModeProperties(tier='Continuous30Days')))
        client.begin_update.return_value.result.return_value = object()
        cli_cosmosdb_update(
            client=client,
            resource_group_name='resource-group',
            account_name='account',
            backup_retention_lock_expiration_timestamp='2030-06-01T00:00:00Z')

        update_request = client.begin_update.call_args.args[2]
        self.assertIsInstance(update_request, DatabaseAccountUpdateParameters)
        self.assertIsInstance(update_request.backup_policy, ContinuousModeBackupPolicy)
        self.assertEqual(
            update_request.backup_policy.backup_retention_lock_expiration_timestamp,
            update_timestamp)
        self.assertEqual(
            update_request.as_dict()['properties']['backupPolicy']
            ['backupRetentionLockExpirationTimestamp'],
            '2030-06-01T00:00:00Z')


class CosmosdbRetentionLockScenarioTest(ScenarioTest):

    @AllowLargeResponse()
    @ResourceGroupPreparer(name_prefix='cli_test_cosmosdb_retention_lock')
    def test_cosmosdb_retention_lock(self, resource_group):
        self.kwargs.update({
            'acc': self.create_random_name(prefix='retention-lock-', length=25),
            'create_timestamp': '2030-01-01T00:00:00Z',
            'update_timestamp': '2030-06-01T00:00:00Z'
        })

        self.cmd(
            'az cosmosdb create -n {acc} -g {rg} '
            '--backup-policy-type Continuous '
            '--backup-retention-lock-expiration-timestamp {create_timestamp}',
            checks=[
                self.check('backupPolicy.type', 'Continuous'),
                self.check('backupPolicy.backupRetentionLockExpirationTimestamp', '{create_timestamp}'),
            ])
        self.cmd('az cosmosdb show -n {acc} -g {rg}', checks=[
            self.check('backupPolicy.backupRetentionLockExpirationTimestamp', '{create_timestamp}'),
        ])

        self.cmd(
            'az cosmosdb update -n {acc} -g {rg} '
            '--backup-retention-lock-expiration-timestamp {update_timestamp}',
            checks=[
                self.check('backupPolicy.backupRetentionLockExpirationTimestamp', '{update_timestamp}'),
            ])

        self.cmd('az cosmosdb update -n {acc} -g {rg} --tags retention-lock=preserved')
        self.cmd('az cosmosdb show -n {acc} -g {rg}', checks=[
            self.check('backupPolicy.backupRetentionLockExpirationTimestamp', '{update_timestamp}'),
        ])

        self.cmd('az cosmosdb delete -n {acc} -g {rg} --yes')