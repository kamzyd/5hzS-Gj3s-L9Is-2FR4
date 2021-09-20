from datetime import datetime, timedelta

class MemoizationError(Exception):
    '''Raised when memoization process fails.'''
    pass

class memoize:
    '''Memorizes various results of the function provided dependent on
       passed parameters.
    
       Methods:
       memoized(self, *resolver)
       Properties:
       func, default_key, timeout
       Read-only: summorial_memory
    '''

    # parameters according to the example given
    def __init__(self, func, *resolver, timeout = 5000):
        # the current default failure handling "int object not callable"
        # does not deliver the correct error information. That is why
        # substitute information is added.
        if not func or not callable(func):
            raise MemoizationError("Failed to initialize a memoize instance.\n"
                                   "No function provided.")

        if not resolver:
            raise MemoizationError("Failed to initialize a memoize instance.\n"
                                   "No resolver provided.")

        # for caching a  dictionary is used. Lists
        # cannot be used because if the sum of arguments
        # was used as key and if there was a function that
        # returned enormous values the lists would become
        # astronomicly large.
        # The following is the format of the stored data:
        # {(key): [(calculation date), (result)], (key):
        # [(calculation date), (result)], ...}.
        self.__summorial_memory = {}
        self.default_key = 0
        self.func = func
        self.timeout = timeout

        self.default_key = sum(list(resolver))
        self.__summorial_memory = {self.default_key: [datetime.now(), self.func(*resolver)]}


    def memoized(self, *resolver):

        if not resolver:
            return self.__summorial_memory[self.default_key][1]

        resolver_sum = sum(list(resolver))
        dt = datetime.now()

        if resolver_sum in self.__summorial_memory:             #what happens to timeout values? Are they deleted?
            duration = dt - self.__summorial_memory[resolver_sum][0]
            if duration < timedelta(milliseconds=self.timeout):
                return self.__summorial_memory[resolver_sum][1]
            else:
                self.__summorial_memory[resolver_sum][1] = self.func(*resolver)
                self.__summorial_memory[resolver_sum][0] = dt
                return self.__summorial_memory[resolver_sum][1]
        else:
            self.__summorial_memory.update({resolver_sum:[dt, self.func(*resolver)]})
            return self.__summorial_memory[resolver_sum][1]


    # Read-only field accessors

    def summorialmemory(self):
        '''dictionary with all values and their definition times'''
        return self.__summorial_memory
