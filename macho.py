import lldb
import ctypes

LC_REQ_DYLD = 0x80000000

FAT_CIGAM = 0xbebafeca
MH_MAGIC_64 = 0xfeedfacf

MH_EXECUTE = 0x00000002
MH_KEXT_BUNDLE = 0x0000000b
MH_FILESET = 0x0000000c

LC_SYMTAB = 0x00000002
LC_UNIXTHREAD = 0x00000005
LC_LOAD_DYLIB = 0x0000000c
LC_DYSYMTAB = 0x0000000b
LC_SEGMENT_64 = 0x00000019
LC_UUID = 0x0000001b
LC_CODE_SIGNATURE = 0x0000001d
LC_ENCRYPTION_INFO = 0x00000021
LC_DYLD_INFO = 0x00000022
LC_DYLD_INFO_ONLY = (0x00000022 | LC_REQ_DYLD)
LC_FUNCTION_STARTS = 0x00000026
LC_MAIN = (0x28 | LC_REQ_DYLD)
LC_DATA_IN_CODE = 0x00000029
LC_DYLD_CHAINED_FIXUPS = (0x00000034 | LC_REQ_DYLD)
LC_FILESET_ENTRY = (0x00000035 | LC_REQ_DYLD)

N_STAB = 0xe0
N_PEXT = 0x10
N_TYPE = 0x0e
N_EXT = 0x01

N_UNDF = 0x0
N_ABS = 0x2
N_SECT = 0xe
N_PBUD = 0xc
N_INDR = 0xa

class mach_header_64(ctypes.Structure):
    _fields_ = [
        ("magic", ctypes.c_uint32),
        ("cputype", ctypes.c_uint32),
        ("cpusubtype", ctypes.c_uint32),
        ("filetype", ctypes.c_uint32),
        ("ncmds", ctypes.c_uint32),
        ("sizeofcmds", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("reserved", ctypes.c_uint32)
    ]

class load_command(ctypes.Structure):
	_fields_ = [
		("cmd", ctypes.c_uint32),
		("cmdsize", ctypes.c_uint32)
	]

class segment_command_64(ctypes.Structure):
    _fields_ = [
        ("cmd", ctypes.c_uint32),
        ("cmdsize", ctypes.c_uint32),
        ("segname", ctypes.c_char * 16),
        ("vmaddr", ctypes.c_uint64),
        ("vmsize", ctypes.c_uint64),
        ("fileoff", ctypes.c_uint64),
        ("filesize", ctypes.c_uint64),
        ("maxprot", ctypes.c_uint32),
        ("initprot", ctypes.c_uint32),
        ("nsects", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
    ]

class section_64(ctypes.Structure):
    _fields_ = [
        ("sectname", ctypes.c_char * 16),
        ("segname", ctypes.c_char * 16),
        ("addr", ctypes.c_uint64),
        ("size", ctypes.c_uint64),
        ("offset", ctypes.c_uint32),
        ("align", ctypes.c_uint32),
        ("reloff", ctypes.c_uint32),
        ("nreloc", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("reserved1", ctypes.c_uint32),
        ("reserved2", ctypes.c_uint32),
        ("reserved3", ctypes.c_uint32),
    ]

KMOD_MAX_NAME = 64

kmod_reference_t = ctypes.c_void_p 
kmod_start_func_t = ctypes.c_void_p
kmod_stop_func_t = ctypes.c_void_p

class kmod_info(ctypes.Structure):
    _fields_ = [
        ("next", ctypes.POINTER(ctypes.c_void_p)),
        ("info_version", ctypes.c_int32),
        ("id", ctypes.c_uint32),
        ("name", ctypes.c_char * KMOD_MAX_NAME),
        ("version", ctypes.c_char * KMOD_MAX_NAME),
        ("reference_count", ctypes.c_int32),
        ("reference_list", ctypes.POINTER(kmod_reference_t)),
        ("address", ctypes.c_void_p),
        ("size", ctypes.c_size_t),
        ("hdr_size", ctypes.c_size_t),
        ("start", ctypes.POINTER(kmod_start_func_t)),
        ("stop", ctypes.POINTER(kmod_stop_func_t))
    ]

class fileset_entry_command(ctypes.Structure):
	_fields_ = [
		("cmd", ctypes.c_uint32),
		("cmdsize", ctypes.c_uint32),
		("vmaddr", ctypes.c_uint64),
		("fileoff", ctypes.c_uint64),
		("entry_id", ctypes.c_uint32),
		("reserved", ctypes.c_uint32)
    ]
