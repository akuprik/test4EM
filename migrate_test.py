import unittest

import migrate_classes


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

if __name__ == '__main__':
    unittest.main()
