"""
functions for migrate process
"""
import os
import pickle

import migrate_classes


def get_all_collection(filename='migrates.pkl'):
    """
    Load all migration objects from file or create empty
    :param filename: path
    :return: migrate_classes.AllCollection()
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            all_collection = pickle.load(f)
            if type(all_collection).__name__ == 'AllCollection':
                return all_collection
    return migrate_classes.AllCollection()


def safe_all_collection(all_collection, filename='migrates.pkl'):
    """
    safe to file all migration objects
    :param all_collection: migrate_classes.AllCollection
    :param filename: path
    """
    if type(all_collection).__name__ == 'AllCollection':
        with open(filename, 'wb') as f:
            pickle.dump(all_collection, f)


