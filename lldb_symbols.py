import argparse
import json
import re

triple = 'arm64e-apple-ios17.5.0'
uuid = '6273B14D-2BFC-3178-B28A-8721E2C2419E'

def parse_section(data, parts):
    size = int(f"0x{parts[1][:-1]}", 16)
    name = parts[2]
    section = {}
    section['name'] = name
    section['size'] = size

    data['sections'].append(section)

def parse_function_address(data, parts):
    symtype = parts[0].split(':')[0].lstrip('0')
    address = f"0x{parts[0].split(':')[1]}"
    symbol_name = parts[1]
    if symtype == '10':
        symbol = {}
        symbol['name'] = symbol_name
        symbol['type'] = 'code'
        symbol['address'] = int(address, 16)

        data['symbols'].append(symbol)

def parse_linker_map(data, file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.rstrip().split()
                if len(parts) > 2:
                    if len(parts[0].split(':')) > 1:
                        if not parts[1][-1] == 'H':
                            parse_function_address(data, parts)
                elif len(parts) > 0:
                    if len(parts[0].split(':')) > 1:
                        parse_function_address(data, parts)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def parse_sections(data, file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split('\t')
                name = parts[0]
                start = int(f"0x{parts[1]}", 16)
                end = int(f"0x{parts[2]}", 16)

                section = {}
                section['name'] = name
                section['address'] = start
                section['size'] = (end - start)
                section['type'] = 'code'

                data['sections'].append(section)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_decompiler_output(linker_map_path, sections_path, output_path):
    data = {}
    data['triple'] = triple
    data['uuid'] = uuid
    data['symbols'] = []
    data['sections'] = []
    parse_linker_map(data, linker_map_path)
    parse_sections(data, sections_path)
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a file line by line and output to a JSON file.")
    parser.add_argument("linker_map", help="The path to the linker map file to be parsed.")
    parser.add_argument("sections", help="The path to the sections file to be parsed.")
    parser.add_argument("output", help="The path to the output JSON file.")
    
    args = parser.parse_args()
    parse_decompiler_output(args.linker_map, args.sections, args.output)
