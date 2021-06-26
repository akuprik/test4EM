"""
Classes for migrate process
"""
import ipaddress

CLOUD_TYPES = ('aws', 'azure', 'vsphere', 'vcloud')
MIGRATION_STATES = ('not started', 'running', 'error', 'success')


class TrustList(list):
    """
    Common list for save delete
    """
    def delete_item(
        self,
        item
    ):
        """
        Deletes an Item and returns deleted item
        :param item: item for delete
        :return: deleted item
        """
        try:
            i = self.index(item)
        except ValueError:
            return item
        return self.pop(i)

    def get_itme_by_index(self, index):
        try:
            return self[index]
        except IndexError:
            return None

    def __str__(self):
        s = ''
        for x in self:
            s += f"({x})\n "
        return s


class Credentials:
    def __init__(
        self,
        user_name='',
        password='',
        domain=''
    ):
        self.user_name = user_name
        self.password = password
        self.domain = domain

    def __str__(self):
        return f"user_name:{self.user_name}, " \
               f"password:{self.password}, " \
               f"domain: {self.domain} "


class MountPoint:
    def __init__(
        self,
        mount_point_name='',
        total_size=0,
    ):
        self.mount_point_name = mount_point_name
        self.total_size = total_size

    def __str__(self):
        return f"m_p_n:'{self.mount_point_name}', sz:{self.total_size}"


class WorkLoad:
    def __init__(
        self,
        ip,
        credentials=Credentials(),
        storage=[MountPoint],
    ):
        try:
            self.ip = ipaddress.ip_address(ip)
        except ValueError:
            self.ip = ipaddress.ip_address('127.0.0.1')
        self.credentials = credentials
        self.storage = storage

    def get_mount_point(self, mount_point_name):
        for x in self.storage:
            if x.mount_point_name == mount_point_name:
                return x
        return None

    def add_mount_point(self, mount_point):
        """
        adds then mount_point if not found it
        :param mount_point: MountPoint
        """
        if not self.get_mount_point(mount_point.mount_point_name):
            self.storage.append(mount_point)

    def delete_mount_point(self, mount_point_name):
        try:
            return self.storage.pop(
                self.storage.index(
                    self.get_mount_point(mount_point_name)
                )
            )
        except ValueError:
            return None

    def key_for_search(self):
        """
        Returns the string for the searching
        :return: string
        """
        return f"{self.ip}{self.credentials}"

    def __str__(self):
        s = f"ip = {self.ip}, " \
            f"{self.credentials}, " \
            f"storage: "
        for x in self.storage:
            s += f"({x}) "
        return s


class Source(WorkLoad):
    pass


class MigrationTarget:
    def __init__(
        self,
        cloud_type: int,
        cloud_credentials: Credentials,
        target_vm: WorkLoad,
    ):
        if 0 <= cloud_type < len(CLOUD_TYPES):
            self.cloud_type = cloud_type
        else:
            self.cloud_type = 0
        self.cloud_credentials = cloud_credentials
        self.target_vm = target_vm

    def __str__(self):
        return f"c_t:{CLOUD_TYPES[self.cloud_type]} c_cred:({self.cloud_credentials}) " \
               f"t_vm:({self.target_vm})"


class Migration:
    def __init__(
        self,
        selected_mount_points: list,
        source: Source,
        migration_target: MigrationTarget,
        migration_state=0,
    ):
        self.selected_mount_points = set(selected_mount_points)
        self.source = source
        self.migration_target = migration_target
        if 0 <= migration_state < len(MIGRATION_STATES):
            self.migration_state = migration_state
        else:
            self.migration_state = 0

    def key_for_search(self):
        return f"{''.join(self.selected_mount_points)}" \
               f"{self.source.ip}" \
               f"{self.migration_target}"

    def run(self):
        return self.migration_state

    def __str__(self):
        return f"(selected: {', '.join(self.selected_mount_points)} " \
               f"source: {self.source} " \
               f"m_target: {self.migration_target} " \
               f"m_state: {MIGRATION_STATES[self.migration_state]}) "

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
        return self[source.ip]

    def __str__(self):
        s = ''
        for x in self.values():
            s += f"({x}) "
        return s


class MigrationTargets(TrustList):
    """
    list of migration targets
    """
    pass


class Migrations(TrustList):
    """
    list of migrations
    """
    def append(self, migration: Migration):
        """
        checks for availability before adding
        :param migration: Migration
        """
        for x in self:
            if x.key_for_search() == migration.key_for_search():
                return
        super().append(migration)


class AllCollection:
    """
    list of all objects (interaction level)
    """
    def __init__(
        self,
        sources=Sources(),
        migration_targets=MigrationTargets(),
        migrations=Migrations(),
    ):
        self.sources = sources
        self.migration_targets = migration_targets
        self.migrations = migrations

    def add_new_source(self, ip, username, password, domain, storage=[]):
        """
        Creates the new source and adds to the list
        :param ip: ip_address
        :param username: str
        :param password: str
        :param domain:  str
        :param storage: list of MountPoint
        :return: Source
        """
        source = Source(ip, Credentials(username, password, domain), storage)
        self.sources.add_source(source)
        return source

    def delete_source(self, ip):
        return self.sources.pop(ip)

    def add_new_migration_target(
        self,
        cloud_type,
        cloud_username,
        cloud_password,
        cloud_domain,
        target_vm: WorkLoad,
    ):
        """
        creates a new migration target and adds list
        :param cloud_type: str from CLOUD_TYPES
        :param cloud_username: str
        :param cloud_password: str
        :param cloud_domain: str
        :param target_vm: WorkLoad
        :return: MigrationTarget
        """
        try:
            c_type = CLOUD_TYPES.index(cloud_type)
        except ValueError:
            c_type = 0
        migration_target = MigrationTarget(
            c_type,
            Credentials(cloud_username, cloud_password, cloud_domain),
            target_vm
        )
        self.migration_targets.append(migration_target)
        return migration_target

    def delete_migration_target(self, migration_target: MigrationTarget):
        return self.migration_targets.delete_item(migration_target)

    def delete_migration_target_by_index(self, index):
        return self.migration_targets.delete_item(
            self.migration_targets.get_itme_by_index(index))

    def add_new_migration(
        self,
        selected_mount_points: list,
        source: Source,
        migration_target: MigrationTarget,
    ):
        """
        Creates a new migration and add to the list
        :param selected_mount_points: List of selected mount point names
        :param source: Source
        :param migration_target: MigrationTarget
        :return: Migration
        """

        migration = Migration(
            selected_mount_points,
            source,
            migration_target
        )
        self.migrations.append(migration)
        return migration

    def delete_migration(self, migration: Migration):
        return self.migrations.delete_item(migration)

    def delete_migration_by_index(self, index):
        return self.migrations.delete_item(
            self.migrations.get_itme_by_index(index))

    def __str__(self):
        return f"sources: {self.sources} \n" \
               f"migration_targets:\n{self.migration_targets} \n" \
               f"migrations: {self.migrations} \n"

