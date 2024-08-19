import lldb

from kernel import Kernel
from macho import *

class Kext:
    def __init__(self, target, process, kernel, base, size, name):
        self.target = target
        self.process = process
        self.kernel = kernel
        self.base = base;
        self.name = name;
        self.segments = {}
        self.ProcessMachO()

    def ProcessMachO(self):
        size = 0
        current_addr = self.base
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

                sects = []
                sect_addr = current_addr + ctypes.sizeof(segment_command_64)

                for i in range(segment_command.nsects):
                    sect = section_64.from_buffer_copy(Kernel.Read(self.process, sect_addr, ctypes.sizeof(section_64)))

                    sects.append(sect)

                    print('%s 0x%x 0x%x' % (sect.sectname.decode("utf-8"), sect.addr, sect.addr + sect.size))

                    sect_addr += ctypes.sizeof(section_64)

                segname = segment_command.segname.decode("utf-8")

                self.segments[segname] = (segment_command, sects)

            current_addr += cmd.cmdsize
        return size