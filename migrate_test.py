import os
import unittest

import migrate_classes
import migrate_func


class TestBaseClasses(unittest.TestCase):
    """
    Testing the base classes: MountPoint, Credentials, WorkLoad, TrustList
    """
    def test_mount_point(self):
        # test empty params
        mount_point = migrate_classes.MountPoint()
        self.assertEqual(
            "m_p_n:'', sz:0",
            str(mount_point),
            'Empty MountPoint creating is wrong')

        # test valid type params
        mount_point = migrate_classes.MountPoint('C:\\', 123123123123)
        self.assertEqual(
            "m_p_n:'C:\\', sz:123123123123",
            str(mount_point),
            'MountPoint with valid params creating is wrong')

        # test not valid type params
        mount_point = migrate_classes.MountPoint(10, '1231231sd23123')
        self.assertEqual(
            "m_p_n:'10', sz:0",
            str(mount_point),
            'MountPoint with not valid params creating is wrong')

    def test_credentials(self):
        # test empty params
        credentials = migrate_classes.Credentials()
        self.assertEqual(
            "user_name:, password:, domain: ",
            str(credentials),
            'Empty Credentials creating is wrong')

        # test valid type params
        credentials = migrate_classes.Credentials(
            'test_user',
            'test_password',
            'test_domain'
        )
        self.assertEqual(
            "user_name:test_user, password:test_password, domain: test_domain",
            str(credentials),
            'Credentials with valid params creating is wrong'
        )

    def test_work_load(self):
        # test empty params
        with self.assertRaises(TypeError):
            work_load = migrate_classes.WorkLoad()

        # test with valid IP
        work_load = migrate_classes.WorkLoad('121.0.0.1')
        self.assertEqual(
            5,
            str(work_load).find('121.0.0.1'),
            'WorkLoad: valid IP is wrong '
        )

        # test with not valid IP
        work_load = migrate_classes.WorkLoad(
            '512.1.1.1',
            migrate_classes.Credentials('u', 'p', 'd'),
        )
        self.assertEqual(
            5,
            str(work_load).find('127.0.0.1'),
            'WorkLoad: valid IP is wrong '
        )

        self.assertEqual(0, len(work_load.storage), 'storage is not empty')

        # test add mount point
        mount_point = work_load.add_mount_point(
            migrate_classes.MountPoint('C:\\', 12312))
        self.assertEqual(1, len(work_load.storage), 'error: add mount point')
        self.assertEqual(
            str(mount_point),
            str(work_load.storage[0]),
            'error: add mount point',
        )

        mount_point = work_load.add_mount_point(mount_point)
        self.assertEqual(
            1,
            len(work_load.storage),
            'error: add mount point equ')

        # test get_mount_point
        self.assertEqual(
            str(mount_point),
            str(work_load.get_mount_point(mount_point.mount_point_name)),
            'error : get_mount_point'
        )

        self.assertIsNone(
            work_load.get_mount_point('no_name'),
            'error : get_mount_point no_name'
        )

        # test is_allow_mount_point
        self.assertTrue(
            work_load.is_allow_mount_point(mount_point),
            'error: test is_allow_mount_point',
        )
        self.assertTrue(work_load.is_logged_in, 'error: is_logged_in')

        # test delete_mount_point
        self.assertIsNone(
            work_load.delete_mount_point('no_name'),
            'error: delete mount point (not None)')

        self.assertEqual(
            1,
            len(work_load.storage),
            'error: delete mount point')

        work_load.delete_mount_point(mount_point.mount_point_name),
        self.assertEqual(
            0,
            len(work_load.storage),
            'error: delete mount point')

        # test key_for_search()
        self.assertEqual(
            "127.0.0.1user_name:u, password:p, domain: d",
            work_load.key_for_search(),
            'error: key search'
        )

        self.assertFalse(
            work_load.is_allow_mount_point(mount_point),
            'error: test is_allow_mount_point',
        )

    def test_trust_list(self):
        trust_list = migrate_classes.TrustList(
            [migrate_classes.MountPoint('C:\\', 12312)],
        )
        # get_item_by_index
        self.assertEqual(
            "m_p_n:'C:\\', sz:12312",
            str(trust_list.get_item_by_index(0)),
        )
        self.assertIsNone(trust_list.get_item_by_index(1))

        # delete_item
        item = trust_list.get_item_by_index(0)
        self.assertEqual(
            str(item),
            str(trust_list.delete_item(item)),
            'error: delete_item',
        )
        self.assertEqual(0, len(trust_list))

        # delete from empty
        self.assertEqual(
            str(item),
            str(trust_list.delete_item(item)),
            'error: delete_item',
        )


class TestMigrates(unittest.TestCase):
    """
    Testing the migration classes (Source, MigrationTarget, Migrate)
    """
    def test_source(self):
        source = migrate_classes.Source('127.0.0.1')
        self.assertEqual(
            'ip = 127.0.0.1, user_name:, password:, domain: , storage: ',
            str(source),
            'error create source',
        )

    def test_migration_target(self):
        # create with valid cloud type
        mt = migrate_classes.MigrationTarget(
            0,
            migrate_classes.Credentials(),
            migrate_classes.WorkLoad('127.0.0.1'),
        )
        self.assertEqual(
            "c_t:aws c_cred:(user_name:, password:, domain: ) "
            "t_vm:(ip = 127.0.0.1, user_name:, password:, domain: , storage: )",
            str(mt),
            'error: create MigrationTarget'
        )
        # create with not valid cloud type
        mt = migrate_classes.MigrationTarget(
            10,
            migrate_classes.Credentials(),
            migrate_classes.WorkLoad('127.0.0.1'),
        )
        self.assertEqual(
            "c_t:aws c_cred:(user_name:, password:, domain: ) "
            "t_vm:(ip = 127.0.0.1, user_name:, password:, domain: , storage: )",
            str(mt),
            'error: create MigrationTarget with not valid CloudType'
        )

    def test_migration(self):
        # test create migration
        migration = migrate_classes.Migration(
            ['C:\\test\\'],
            migrate_classes.Source(
                ' ',
                migrate_classes.Credentials(),
            ),
            migrate_classes.MigrationTarget(
                0,
                migrate_classes.Credentials(),
                migrate_classes.WorkLoad(
                    '127.0.0.2',
                    migrate_classes.Credentials(),
                ),
            ),
        )
        self.assertEqual(
            "(selected: C:\\test\\ source: ip = 127.0.0.1, "
            "user_name:, password:,"
            " domain: , storage:  m_target: c_t:aws c_cred:(user_name:, "
            "password:, domain: ) t_vm:(ip = 127.0.0.2, user_name:, password:, "
            "domain: , storage: ) m_state: not started) ",
            str(migration)
        )

        migrate_classes.SLEEP_RUN = 0

        # test migrate with empty migration_target.storage
        migration.source.add_mount_point(
            migrate_classes.MountPoint('C:\\test\\', 135),
        )
        migration.run()
        self.assertEqual(
            '',
            '\n'.join(migration.migrate_log),
            'error: Migrate with empty target list',
        )

        # test migrate with mount_point in migration_target.storage
        migration.migration_target.target_vm.add_mount_point(
            migrate_classes.MountPoint('C:\\test\\', 500),
        )
        migration.run()
        self.assertEqual(
            "copy m_p_n:'C:\\test\\', sz:135 to m_p_n:'C:\\test\\', sz:500",
            '\n'.join(migration.migrate_log),
            'error: Migrate with not empty target list',
        )

        # test migrate with 2 mount_point in migration_target.storage
        # and 1 selected
        migration.migration_target.target_vm.add_mount_point(
            migrate_classes.MountPoint('D:\\test\\', 1500),
        )
        migration.run()
        self.assertEqual(
            "copy m_p_n:'C:\\test\\', sz:135 to m_p_n:'C:\\test\\', sz:500",
            '\n'.join(migration.migrate_log),
            'error: Migrate with not empty target list and one selected',
        )

        # test migrate with 2 mount_point in migration_target.storage
        # and 2 selected
        migration.selected_mount_points.add('D:\\test\\')
        migration.run()
        self.assertEqual(
            2,
            len(migration.migrate_log),
            'error: Migrate with not empty target list adn to 2 selected',
        )


class TestMigrateList(unittest.TestCase):
    """
    Test lists (Sources, MigrationTargets, Migrations
    """
    def test_sources(self):
        s_list = migrate_classes.Sources()
        # test add_source
        source = s_list.add_source(
            migrate_classes.Source(''),
        )
        self.assertEqual(1, len(s_list), 'error: add_source')
        self.assertEqual(
            "(ip = 127.0.0.1, user_name:, password:, domain: , storage: ) ",
            str(s_list),
            'error: add_source',
        )

        # test add_source with came IP and change credentials
        source.credentials.user_name = 'user1'
        source = s_list.add_source(source)
        self.assertEqual(1, len(s_list), 'error: add_source')
        self.assertEqual(
            "(ip = 127.0.0.1, user_name:user1, "
            "password:, domain: , storage: ) ",
            str(s_list),
            'error: add_source with same IP and change credentials',
        )

    def test_migration_targets(self):
        """
        like TestBaseClasses.test_trust_list
        """
        pass

    def test_migrations(self):
        """
        test Migrations
        """
        migration = migrate_classes.Migration(
            ['C:\\test\\'],
            migrate_classes.Source(
                ' ',
                migrate_classes.Credentials(),
            ),
            migrate_classes.MigrationTarget(
                0,
                migrate_classes.Credentials(),
                migrate_classes.WorkLoad(
                    '127.0.0.2',
                    migrate_classes.Credentials(),
                ),
            ),
        )

        migrations = migrate_classes.Migrations()
        migrations.append(migration)
        self.assertEqual(1, len(migrations), 'error: append migration')
        # test append same migration
        migrations.append(migration)
        self.assertEqual(1, len(migrations), 'error: append migration')

    def test_all_collection(self):
        """
        test AllCollection
        """
        all_col = migrate_classes.AllCollection()
        # test add_new_source
        source = all_col.add_new_source(
            '127.0.0.1',
            'usename',
            'password',
            'domain.ru',
        )
        self.assertEqual(1, len(all_col.sources), "error: add_new_source")
        self.assertEqual(
            0,
            str(all_col).find(
                "sources: (ip = 127.0.0.1, user_name:usename, "
                "password:password, "
                "domain: domain.ru, storage: )",
            ),
            "error: add_new_source",
        )

        # test delete source
        source = all_col.delete_source(source.ip)
        self.assertEqual(0, len(all_col.sources), "error: delete_source")
        # test delete source from empty list
        self.assertIsNone(
            all_col.delete_source(source.ip),
            "error: delete_source from empty list"
        )
        self.assertEqual(
            0,
            len(all_col.sources),
            "error: delete_source from empty list",
        )

        # test add_new_migration_target
        mt = all_col.add_new_migration_target(
            'aws',
            'cloud_username',
            'cloud_password',
            'cloud_domain',
            migrate_classes.WorkLoad(
                '127.0.0.2',
            ),
        )
        self.assertEqual(1, len(all_col.migration_targets))
        self.assertEqual(
            31,
            str(all_col).find(str(mt))
        )

        # test del_migration_target
        mt = all_col.delete_migration_target(mt)
        self.assertEqual(0, len(all_col.migration_targets))

        # test del_migration_target from empty list
        s_mt = str(mt)
        mt = all_col.delete_migration_target(mt)
        self.assertEqual(0, len(all_col.migration_targets))
        self.assertEqual(s_mt, str(mt))

        # test add_new_migration
        migration = all_col.add_new_migration(
            ['C:\\test'],
            source,
            mt
        )
        self.assertEqual(1, len(all_col.migrations))
        self.assertEqual(45, str(all_col).find(str(migration)))

        # test delete_migration
        migration = all_col.delete_migration(migration)
        self.assertEqual(0, len(all_col.migrations))
        # test delete_migration from empty list
        s_mg = str(migration)
        migration = all_col.delete_migration(migration)
        self.assertEqual(0, len(all_col.migrations))
        self.assertEqual(s_mg, str(migration))


class TestFunctions(unittest.TestCase):
    """Test for functions in the migrate_func"""
    def test_save_to_file_and_load(self):

        filename = 'migratest.pkl'
        if os.path.exists(filename):
            os.remove(filename)
        # make empty AllCollection
        all_col = migrate_func.get_all_collection(filename)
        source = all_col.add_new_source(
            '127.0.0.1',
            'usename',
            'password',
            'domain.ru',
        )
        mt = all_col.add_new_migration_target(
            'aws',
            'cloud_username',
            'cloud_password',
            'cloud_domain',
            migrate_classes.WorkLoad(
                '127.0.0.2',
            ),
        )
        migration = all_col.add_new_migration(
            ['C:\\test'],
            source,
            mt
        )

        # test save AllCollection
        migrate_func.save_all_collection(all_col, filename)
        self.assertTrue(os.path.exists(filename))

        # test load AllCollection
        all_all_load = migrate_func.get_all_collection(filename)
        self.assertEqual(str(all_col),str(all_all_load))


if __name__ == '__main__':
    unittest.main()
