import lldb

from macho import *

class Kernel:
    def GetKernelCache(target, process):
        if hasattr(Kernel.GetKernelCache, "kernel_cache"):
            return GetKernelCache.kernel_cache

        thread = process.GetSelectedThread()
        frame = thread.GetFrameAtIndex(0)
        pc = 0xfffffff029e0c000

        kaslr_align = 0x4000
        near = pc & ~(kaslr_align - 1)
        found = False

        while True:
            mh = mach_header_64.from_buffer_copy(Kernel.Read(process, near, ctypes.sizeof(mach_header_64)))
            if mh.magic == MH_MAGIC_64:
                if mh.filetype == 0xC and mh.flags == 0 and mh.reserved == 0:
                    found = True
                    break

            near -= kaslr_align

        if (found):
            Kernel.GetKernelCache.kernel_cache = near
            print("KernelCache address = 0x%x" %(near))
            return near

        return 0

    def Read(process, address, size):
        error = lldb.SBError()
        return process.ReadMemory(address, size, error)

    def Write(process, address, data, size):
        error = lldb.SBError()
        process.WriteMemory(address, size, error)

    def ReadString(process, address):
        str = b''
        b = Kernel.Read(process, address, 1)
        while b != b'\0':
            str += b
            b = Kernel.Read(process, address + len(str), 1)
        return str.decode("utf-8")


    def __init__(self, target, process):
        self.kernel_cache = Kernel.GetKernelCache(target, process)
        self.target = target
        self.process = process
        self.kexts = []
        self.ProcessAllKexts()

    def GetMachOSize(self, addr):
        size = 0
        current_addr = addr
        mh = mh = mach_header_64.from_buffer_copy(Kernel.Read(self.process, current_addr, ctypes.sizeof(mach_header_64)))
        current_addr += ctypes.sizeof(mach_header_64)
        for i in range(mh.ncmds):
            cmd = load_command.from_buffer_copy(Kernel.Read(self.process, current_addr, ctypes.sizeof(load_command)))

            if cmd.cmd == LC_SEGMENT_64:
                segment_command = segment_command_64.from_buffer_copy(Kernel.Read(self.process, current_addr, ctypes.sizeof(segment_command_64)))

                vmaddr = segment_command.vmaddr
                vmsize = segment_command.vmsize

                fileoff = segment_command.fileoff
                filesize = segment_command.filesize

                if vmsize > 0:
                    size = max(size, (vmaddr + vmsize) - addr)

            current_addr += cmd.cmdsize
        return size


    def ProcessAllKexts(self):
        current_addr = self.kernel_cache
        mh = mh = mach_header_64.from_buffer_copy(Kernel.Read(self.process, current_addr, ctypes.sizeof(mach_header_64)))
        current_addr += ctypes.sizeof(mach_header_64)
        for i in range(mh.ncmds):
            cmd = load_command.from_buffer_copy(Kernel.Read(self.process, current_addr, ctypes.sizeof(load_command)))

            if cmd.cmd == LC_FILESET_ENTRY:
                fileset = fileset_entry_command.from_buffer_copy(Kernel.Read(self.process, current_addr, ctypes.sizeof(fileset_entry_command)))
                base = fileset.vmaddr
                size = 0
                
                entry_id_addr = current_addr + fileset.entry_id
                entry_id = Kernel.ReadString(self.process, entry_id_addr)

                print("Kext %s = 0x%x" % (entry_id, base))

                from kext import Kext

                self.kexts.append(Kext(self.target, self.process, self, base, size, entry_id))

            current_addr += cmd.cmdsize