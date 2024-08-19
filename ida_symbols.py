import idaapi
import idautils
import idc

def get_function_end(ea):
    func = idaapi.get_func(ea)
    if not func:
        return None
    return func.end_ea

def main():
    for function_ea in idautils.Functions():
        function_name = idc.get_func_name(function_ea)
        function_start = function_ea
        function_end = get_function_end(function_ea)
        
        print(f"Function: {function_name}")
        print(f"Start Address: {hex(function_start)}")
        print(f"End Address: {hex(function_end)}")
        print("-" * 40)

if __name__ == "__main__":
    main()
