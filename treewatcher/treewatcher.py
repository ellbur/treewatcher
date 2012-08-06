
import pyinotify as pin

def run_watch_files(proc, path):
    '''alias for run_watching_files(proc, [path])'''
    return run_watching_files(proc, [path])

def run_watching_files(proc, paths):
    '''
    Run the command (callable) ``proc`` and track watched files under the
    directories ``paths``.
    
    Parameters:
        - proc:  A callable. It will be called.
        - paths: A list of strings, the directories to monitor.
    
    Returns:
        result, accesses:
            - result: the return from ``proc()``.
            - accesses: A ``RecordHandler`` object containg information
              about file accesses.
    
    The fields of ``accesses`` are:
        - created
        - deleted
        - accessed
        - modified
    
    which are sets of strings.
    '''
    watcher = pin.WatchManager()
    
    handler = RecorderHandler()
    notifier = pin.Notifier(watcher, handler, timeout=1)
    for _ in set(paths):
        watcher.add_watch(_, handler.ev_mask,
            rec=True, quiet=False, auto_add=True)
    
    result = proc()
    
    notifier.process_events()
    while notifier.check_events():
        notifier.read_events()
        notifier.process_events()
    
    return result, handler
    
class RecorderHandler(pin.ProcessEvent):
    '''
    Holds lists of files access during the operation. These are
    stored in four fields (all sets):
        - created
        - deleted
        - accessed
        - modified
    
    which hold path names (usually absolute -- don't count on it).
    '''
    
    def __init__(self):
        self.created  = set()
        self.deleted  = set()
        self.accessed = set()
        self.modified = set()
        
        self.ev_mask = (
              pin.IN_CREATE
            | pin.IN_DELETE
            | pin.IN_ACCESS
            | pin.IN_CLOSE_WRITE
        )
    
    def process_IN_CREATE(self, ev):
        self.created.add(ev.pathname)
    
    def process_IN_DELETE(self, ev):
        self.deleted.add(ev.pathname)
        
    def process_IN_ACCESS(self, ev):
        self.accessed.add(ev.pathname)
    
    def process_IN_CLOSE_WRITE(self, ev):
        self.modified.add(ev.pathname)
        
    def __str__(self):
        return (
            'created: %s, deleted: %s, accessed: %s, modified: %s' % (
                str(self.created),
                str(self.deleted),
                str(self.accessed),
                str(self.modified)
            )
        )
    
    def __repr__(self):
        return self.__str__()

