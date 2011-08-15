
import pyinotify as pin

def run_watch_files(proc, path):
    watcher = pin.WatchManager()
    
    handler = RecorderHandler()
    notifier = pin.Notifier(watcher, handler, timeout=1)
    watcher.add_watch(path, handler.ev_mask,
        rec=True, quiet=False, auto_add=True)
    
    result = proc()
    
    notifier.process_events()
    while notifier.check_events():
        notifier.read_events()
        notifier.process_events()
    
    return result, handler
    
class RecorderHandler(pin.ProcessEvent):
    
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

