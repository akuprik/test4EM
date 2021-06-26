import migrate_classes
import migrate_func

FILE_MIGRATES = 'mig.pkl'


all_collection = migrate_func.get_all_collection()
print(all_collection)
source = all_collection.add_new_source('127.0.0.2', 'user', 'pass', 'dom')
source.add_mount_point(migrate_classes.MountPoint('C:\\', 10000))
source.add_mount_point(migrate_classes.MountPoint('D:\\test\\', 10000))
#print(source)

work_load = migrate_classes.WorkLoad(
    '127.0.0.5',
    migrate_classes.Credentials('uuser', 'p', 'd'),
    []
)
migration_target = all_collection.add_new_migration_target(
    'aws',
    'c_uname',
    'c_pass',
    'c_domain',
    work_load,
)

migration_target.target_vm.add_mount_point(
    migrate_classes.MountPoint('E:\\target\\', 10000))

migration = all_collection.add_new_migration(['C:\\'],source,migration_target)

print (migration)


migrate_func.safe_all_collection(all_collection)
