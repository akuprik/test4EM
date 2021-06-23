"""
Classes for migrate process
"""
import ipaddress
import pickle

CLOUD_TYPES = ('aws', 'azure', 'vsphere', 'vcloud')
MIGRATION_STATES = ('not started', 'running', 'error', 'success')


class Credentials:
    def __init__(
        self,
        user_name='',
        password='',
        domain=''
    ):
        self.username = user_name
        self.password = password
        self.domain = domain


class MountPoint:
    def __init__(
        self,
        mount_point_name='',
        total_size=0,
    ):
        self.mount_point_name = mount_point_name
        self.total_size = total_size


class WorkLoad:
    def __init__(
        self,
        ip,
        credential=Credentials(),
        storage=[],
    ):
        try:
            self.ip = ipaddress.ip_address(ip)
        except ValueError:
            self.ip = ipaddress.ip_address('127.0.0.1')
        self.credential = credential
        self.storage = storage


class Source(WorkLoad):
    pass


class MigrationTarget:
    def __init__(
        self,
        cloud_type=0,
        cloud_credentials=Credentials(),
        target_vm=WorkLoad(),
    ):
        if 0 <= cloud_type < len(CLOUD_TYPES):
            self.cloud_type = cloud_type
        else:
            self.cloud_type = 0
        self.cloud_credentials = cloud_credentials
        self.target_vm=target_vm


class Migration:
    def __init__(
        self,
        selected_mount_points=[],
        source=Source(),
        migration_target=MigrationTarget(),
        migration_state=0,
    ):
        self.selected_mount_points = set()
        self.source = source
        self.migration_target = MigrationTarget
        if 0 <= migration_state < len(MIGRATION_STATES):
            self.migration_state = migration_state
        else:
            self.migration_state = 0

    def run(self):
        return self.migration_state


class Sources(dict):
    """
    list of sources
    """
    def add_source(self, source):
        """
        ensures the uniqueness of the source IP
        :param source: Source
        """
        try:
            self[source.ip] = source
        except:
            pass


class MigrationTargets(list):
    """
    list of migration targets
    """
    pass


class Migrations(list):
    """
    list of migrations
    """


class AllCollection:
    """
    list of all objects
    """
    def __init__(self, sources, migration_targets, migrations):
        self.sources = sources
        self.migration_targets = migration_targets
        self.migtations = migrations

