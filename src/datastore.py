"""Defines a datastore class which is used to store user data."""

import json
import time


initial_obj = {
    'users': {},
    'guilds': {},
}


class Datastore:
    """Stores the data for users and guilds in the Discord Bot."""

    def __init__(self):
        """Initialises the data_store object.

        The data is initialised with the data from the persistence.json
        file. If this file does not exist, then the data is initialised
        from the initial object.
        """

        self.last_update_time = 0

        try:
            with open('persistence.json', 'r') as file:
                self.__store = json.load(file)
        except (OSError, json.JSONDecodeError):
            self.__store = initial_obj

    def get(self):
        """Returns the data stored in the data store.

        Return Value:
            Returns a dictionary containing the profiles of the users and guilds.
        """

        return self.__store

    def set(self, store):
        """Sets the data in the data store.

        Stores the data given in store in the data store and writes the
        data to the persistence.json file so that the data can be loaded
        when the data store is initialised.

        Arguments:
            store           (dict)   - The data to store in the data store.
        """

        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

        # Only update the persistence file if it was not updated in the last
        # 5 seconds to reduce the time it takes to save the data store.

        curr_time = time.time()
        if curr_time > self.last_update_time + 5:
            self.last_update_time = curr_time
            with open('persistence.json', 'w') as file:
                json.dump(self.__store, file)

print('Loading Datastore...\n')

global data_store
data_store = Datastore()
