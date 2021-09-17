from datetime import datetime, timedelta

class MemoizationError(Exception):
    '''Raised when memoization process fails.'''
    pass

class memoize:
    '''Memorizes various results of the function provided dependent on
       handed over parameters
    
       Methods:
       memoized(self, *resolver)

       Properties:
       func, resolver, timeout
       Read-only: summorial_memory, latest_mod
    '''

    # parameters according to the example given
    def __init__(self, func, *resolver, timeout = 5000):
        # the current default failure handling "int object not callable"
        # does not deliver the correct error information. That is why
        # substitute information is added. It is easy to find such errors
        # so it might be unnecessary but anyway..
        if not func or not callable(func):
            raise MemoizationError("Failed to initialize a memoize instance.\n"
                                   "No function provided.")

        # for caching a simple dictionary is used. Nothing more is needed.
        # The following is the format of the stored data:
        # {(resolver): [(calculation date), (result)], (resolver):
        # [(calculation date), (result)], ...}.
        self.__summorial_memory = {}
        self.__latest_mod = datetime.now()
        self.func = func
        self.timeout = timeout

        # following the design-principle shown in the example. "If
        # resolver is provided the cache key is determined."
        # "By default, the first argument provided to the memorized
        # function ( = resolver[0] ) is used as the map cache key.".
        # It might be a misunderstanding but one argument of the
        # function is not definite enough to conclusively determine
        # if a key exists so the resolver is used in its full glory.
        if resolver:
            self.__summorial_memory[resolver] = [datetime(1, 1, 1, 0, 0), None]

    def memoized(self, *resolver):
        if not resolver:
            raise MemoizationError("Failed to memoize.\n"
                                   "No resolver provided.")

        # if the current time is calculated just once it will increase
        # efficiency. However the tolerance will rise as well because
        # the constant of 'time.now()' will be acceptably outdated at
        # the time of implementation (it might give the impression of
        # a little bit higher timeout than defined dependent on the
        # clock frequency). Although, worth it in this case.
        dt = datetime.now()

        # delete all keys and values to save memory (they become
        # rubbish with no reference). The particular values have
        # different durations so not every one might be outdated.
        # However, if the latest modification of summorial_memory
        # exceeds the timeout all values have to be outdated. It
        # is also possible to check every single key in order to
        # detect outdated values every time the method is executed
        # but such technique would result in too much of an efficiency
        # sacrifice.
        if (dt - self.__latest_mod) > timedelta(milliseconds=self.timeout):
            self.__summorial_memory.clear()

        # first argument should be used as map cache key. However,
        # here all are used to increase accuracy.
        if resolver in self.__summorial_memory:
            duration = dt - self.__summorial_memory[resolver][0]

            # if a value's existence duration is higher than timeout
            # it is re-calculated and returned
            if duration > timedelta(milliseconds=self.timeout):
                self.__summorial_memory[resolver][1] = self.func(*resolver)
                # update the last modification time
                self.__summorial_memory[resolver][0] = self.__latest_mod = dt
            
            return self.__summorial_memory[resolver][1]
        else:
            self.__latest_mod = dt
            self.__summorial_memory[resolver] = [dt, self.func(*resolver)]

            return self.__summorial_memory[resolver][1]
        

    # Read-only field accessors

    def latestmodification(self):
        '''time of the latest modification of the cache'''
        return self.__latest_mod

    def summorialmemory(self):
        '''dictionary with all values and their definition times'''
        return self.__summorial_memory
