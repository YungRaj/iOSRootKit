import lldb

from kernel import Kernel

class iOSRootKit:
    def GetTarget():
        debugger = lldb.debugger
        return debugger.GetSelectedTarget()

    def GetProcess():
        debugger = lldb.debugger
        target = debugger.GetSelectedTarget()
        return target.GetProcess()

    def ReadMemory(address, size):
        error = lldb.SBError()
        return process.ReadMemory(address, size, error)

    def WriteMemory(address, data, size):
        error = lldb.SBError()
        return process.WriteMemory(address, data, error)

    def __init__(self):
        self.target = iOSRootKit.GetTarget()
        self.process = iOSRootKit.GetProcess()
        self.main_module = self.target.GetModuleAtIndex(0)
        self.kernel = Kernel(self.target, self.process)

