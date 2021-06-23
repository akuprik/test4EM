"""
Classes for migrate process
"""

CLOUD_TYPES = ('aws', 'azure', 'vsphere', 'vcloud')
MIGRATION_STATES = ('not started', 'running', 'error', 'success')


class Credentials:
    user_name = ''
    password = ''
    domain = ''


class MountPoints:
    mount_point_name = ''
    total_size = ''


class WorkLoad:
    ip = ''
    credential = Credentials()
    storage = []


class Source(WorkLoad):
    pass


class MigrationTarget:
    cloud_type = CLOUD_TYPES(1)
    cloud_credentials = Credentials()
    target_vm = WorkLoad()


class Migration:
    selected_mount_points = []
    source = Source()
    migration_target = MigrationTarget()
    migration_state = 1

    def run(self):
        return self.migration_state




