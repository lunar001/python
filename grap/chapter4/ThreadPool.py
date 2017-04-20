#!/usr/bin/python

import threading


class WorkerTask(object):
    """ A task to be performed by the ThreadPool."""
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.function(*self.args, **self.kwargs)


class WorkerThread(threading.Thread):
    """ A thread managed by a thread pool."""
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.pool = pool
        self.busy = False
        self._started = False
        self._event = None

    def work(self):
        if self._started is True:
            if self._event is not True and not self._event.isSet():
                self._event.set()
        else:
            self._started = True
            self.start()

    def run(self):
        while True:
            self.busy = True
            while len(self.pool._tasks) > 0:
                try:
                    task = self.pool._tasks.pop()
                    task()
                except IndexError:
                    # Just incase another thread grabbed the task first.
                    pass
            #Sleep until needed again
            self.busy = False
            if self._event is None:
                self._event = threading.Event()
            else:
                self._event.clear()
            self._event.wait()

class ThreadPool(object):
    """Executes queued tasks in the background."""
    """We should init some thread, for to excute one Task 
       by multi thread, if only add task one time, just single thread"""
    def __init__(self, max_pool_size = 10):
        self.max_pool_size = max_pool_size
        self._threads = []
        self._tasks = []


    def _addTask(self, task):
        self._tasks.append(task)
        worker_thread = None
        # this methold to find the next thread is low performance
        for thread in self._threads:
            if thread.busy is False:
                worker_thread = thread
                break
        if worker_thread is None and len(self._threads) <= self.max_pool_size:
            worker_thread = WorkerThread(self)
            self._threads.append(worker_thread)
        if worker_thread is not None:
            worker_thread.work()

    def addTask(self, function, *args, **kwargs):
        self._addTask(WorkerTask(function, *args, **kwargs))

    def stop(self):
        for worker_thread in self._threads:
            worker_thread.join()

class GlobalThreadPool(object):
    """ ThreadPool Singleton class."""
    _instance = None
    
    def __init__(self):
        """ create singleton instance"""
        if GlobalThreadPool._instance is None:
            GlobalThreadPool._instance = ThreadPool()

    def __getattr__(self, attr):
        """ Delegate get access to implementation"""
        return getattr(self._instance, attr)

    def __setattr__(self, attr, val):
        """" Delegate set access to implementation"""
        return setattr(self._instance, attr, val)









