import re
from flask import current_app
import pysnooper
def extract_seal_number_v2(lines):
    """Return list of Seal Number from `lines`"""
    seals = []
    seal_regexes = get_seal_no_regex(lines)

    if len(seal_regexes) > 0:
        # TODO: Only catch 1st format of SEAL NO?
        seal_regex = re.compile(seal_regexes[0])
        seals = re.findall(seal_regex, lines)
    return seals

def extract_seal_number(lines, conts_no):
    """Return list of Seal Number from `lines`"""

    seals = []
    seal_regexes = get_seal_no_regex(lines)

    if len(seal_regexes) > 0:
        # TODO: Only catch 1st format of SEAL NO?
        seal_regex = re.compile(seal_regexes[0])
        seals = re.findall(seal_regex, lines)

    else:
        # TODO: Only for case: 'VN 123456, None RegEx return'
        for line in lines.split('\n'):
            if len(line) > 6:
                for cont_no in conts_no:
                    if cont_no in line:
                        non_number = line.replace(cont_no, '')
                        spliter = non_number[0]
                        for char in non_number[1:]:
                            if char != spliter and not char.isalnum():
                                seals = [non_number[1:].replace(char, '')]

    return seals


def get_seal_no_regex(lines):
    """ Get lines of number and seals from annotation
        return seal number regex for SI template
    """
    # Break all lines to Digit - Alpha - Non-word groups
    normalize_chars_group = [
        convert_char_group(line)
        for line in lines.split('\n')
        if len(line) > 6
    ]

    # Break all groups to Alpha - Digit with length > 6
    alphaDigit_groups = [
        words
        for chars_group in orderedSet(normalize_chars_group)
        for words in chars_group.split('N')
        if len(words) > 6 and 'a' in words and 'd' in words
    ]

    # Compile to RegEx syntax
    seal_regexes = [
        convert_regex(char_group_compress(alphaDigit))
        for alphaDigit in orderedSet(alphaDigit_groups)
        if convert_regex(char_group_compress(alphaDigit)) is not None
    ]

    # Usually return 1 result, sometimes catch something like this '1234CNT'
    return seal_regexes


def convert_char_group(strings):
    """ Get strings and convert to char group:
            [A-Z]   > 'a'
            [0-9]   > 'd'
            /-_+=., > 'N'
        ABCD.1234:"ABCD" > 'aaaaNddddNNaaaaN'
    """
    chars_group = ''
    for char in strings:
        if char.isalpha() and char.isupper():
            chars_group += 'a'
        elif char.isdigit():
            chars_group += 'd'
        else:
            chars_group += 'N'
    return chars_group


def char_group_compress(re_simply):
    """ Compress from aabbbaa > a2b3a2
        return [{'a': 2}, {'b': 3}, {'a': 2}]
    """
    grouped = [re_simply[0]]
    pos = 0
    for i in range(len(re_simply) - 1):
        if re_simply[i] == re_simply[i + 1]:
            grouped[pos] += re_simply[i + 1]
        else:
            grouped.append(re_simply[i + 1])
            pos += 1
    return [{group[0]: len(group)} for group in grouped]


def convert_regex(regex_dict):
    """ Get regex compress in dict type to extract
        Return RegEx in string type
    """
    cont_number_regex = [{'a': 4}, {'d': 7}]
    if regex_dict != cont_number_regex:
        regex_comp = ''
        for re_group in regex_dict:
            no_of_char = str([*re_group.values()][0])
            if [*re_group.keys()][0] == 'a':
                regex_comp += r'[A-Z]' + '{' + no_of_char + '}'
            else:
                regex_comp += r'[\d]' + '{' + no_of_char + '}'
    else:
        regex_comp = None
    return regex_comp


def orderedSet(input_list):
    """ Get List input
        Return List of unique element with same order as input
    """
    unorder_dict = {}
    for i, val in enumerate(input_list):
        unorder_dict[val] = unorder_dict.get(val, i)
    return sorted(unorder_dict, key=unorder_dict.get)

def is_number(value):
    if value.isdigit():
        return True
    num_format = re.compile("^[\-]?[0-9][0-9]*\.?[0-9]+$")
    isnumber = re.match(num_format,value)
    return isnumber

def is_container_weight(value):
    value = re.sub('[^A-Za-z]+', '', value)
    value = value.strip()
    for unit in current_app.config['CONTRAINER_WEIGHT']:
        if unit == value.upper():
            return True
    return False


def is_container_measurement(value):
    value = re.sub('[^A-Za-z]+', '', value)
    value = value.strip()
    for unit in current_app.config['CONTRAINER_CBM']:
        if unit == value.upper():
            return True
    return False


def is_container_type(value):
    for unit in current_app.config['CONTRAINER_TYPES']:
        if unit in value.upper():
            return True
    return False


def is_char_splitter(c):
    if c in current_app.config['CHARATERS_SPLIT_MARK']:
        return True
    return False


def extract_contaner_no(prev_part_value, value):
    text = ''
    if prev_part_value != None:
        text = prev_part_value + value
    else:
        text = value
    try:
        pattern = re.compile(r'([A-Z]{4}[\d]{7})$')  # Example: 2121 Abc |2121 (Abc)
        list_value = re.findall(pattern, text.strip())
        if len(list_value) > 0:
            return list_value[0]
        return None
    except re.error:
        return None


def extract_seal_no( prev_value, value, special_char):
    
    comp_value = value
    if special_char == ' ' and prev_value != None:
        comp_value = prev_value + value
    seals = extract_seal_number_v2(comp_value)
    if len(seals) > 0:
        return seals[0]
    return None

def extract_packet_value(prev_part_value, value):
    text = ''
    if prev_part_value != None:
        text = prev_part_value + value
    else:
        text = value
    try:
        pattern = re.compile(r'^[0-9]+.+[a-zA-Z][a-zA-Z][a-zA-Z][\)]?')  # Example: 2121 Abc |2121 (Abc)
        list_value = re.findall(pattern, text.strip())
        if len(list_value) > 0:
            return list_value[0]
        return None
    except re.error:
        return None

def extract_value(prev_part_value, value):
    text = ''
    if prev_part_value is not None:
        text = prev_part_value + value
    else:
        text = value
    try:
        # Example: 2121 Abc |2121 (Abc)
        pattern = re.compile(r'[0-9]+.+[a-zA-Z][\)]?')
        list_value = re.findall(pattern, text.strip())
        if len(list_value) > 0:
            return list_value[0]
        return None
    except re.error:
        return None


def extract_total_cont_type(prev_part_value, value):
    text = ''
    if prev_part_value is not None:
        text = prev_part_value + value
    else:
        text = value
    # Example: 12X34 DC
    try:
        pattern = re.compile(r'[0-9]x[0-9][0-9]+.+[a-zA-Z][\)]?')    
        list_value = re.findall(pattern, text.lower())
        if len(list_value) > 0:
            return True, list_value[0]
        return False, None
    except re.error:
        return False, None


def num_total_cont_type(value):
    # Example: 12X34 DC
    try:
        pattern = re.compile(r'[0-9]x[0-9][0-9]+.+[a-zA-Z][\)]?')  
        list_value = re.findall(pattern, value.lower())
        if len(list_value) > 0:
            arr = list_value[0].split('x')
            num =  int(arr[0])
            return num
        return 0
    except re.error:
        print('error')
        return 0

# Example:
#   NYKU8433449 /MOL050271N: 12 PKG  => [NYKU8433449, MOL050271N, 12 PKG ]
def split_to_get_parts(text):
    parts = []
    strBuffer = ''
    beginSpecialChar = True
    isFindSpecialChar = False
    lst_special_char = []
    for c in text:
        # Check case: (1180CTN/12570.61KG/ 58.990CBM)
        if is_char_splitter(c):
            # if len(strBuffer) > 0:
            #     if beginSpecialChar:
            #         parts += strBuffer.split('(')
            #         isFindSpecialChar = True
            #     else:
            parts.append(strBuffer)
            lst_special_char.append(c)
            strBuffer = ''
        else:
            strBuffer += c
    if len(strBuffer) > 0:
        parts.append(strBuffer)
    return parts, lst_special_char


def extract_container_type(value):
    if value is None:
        return ''
    value = value.replace("'", "").replace("´", "").upper()
    arr = value.split('X')
    if len(arr) > 0:
        return arr[-1]
    return ''

def append_conts(lst, dict_conts, lst_cont_type):
    if 'container_type' not in dict_conts and len(lst_cont_type) > 0:
        dict_conts['container_type'] = lst_cont_type[0]
        lst_cont_type.pop(0)
    lst.append(dict_conts)
    return lst

# @pysnooper.snoop(depth=1)
def verified_conts(results, conts_no, str_weights, str_meas, total_weight, total_measurement ):
    verified = True
    check_total_count = True
    if len(str_weights) == 1 and len(str_meas) == 1 and str_weights[0] == total_weight and str_meas[0] == total_measurement:
        check_total_count = False

    if check_total_count and ( \
            (len(str_weights) > 0 and len(conts_no) !=  len(str_weights)) \
            or (len(str_meas) > 0 and len(conts_no) !=  len(str_meas)) ):
        verified = False
        
    lengthDetail = None
    for item in results:
        if lengthDetail == None:
            lengthDetail = len(item)
        if len(item) != lengthDetail:
            verified = False
        if 'container_no' not in item or 'seal_no' not in item:
            verified = False
            break
    return verified

# @pysnooper.snoop(depth=1)
def extract_container_detail(si_result):
    """ Get si_result['containers_detail']
        return list of new cont_detail dict
    """
    print(si_result)
    conts_num_seal = si_result['containers_detail']

    # Container
    # conts_no = re.findall(r'([A-Z]{4}[\d]{7})', conts_num_seal)

    # Seals
    # seals = extract_seal_number(conts_num_seal, conts_no)
    
    if is_number(si_result['total_packages']):
        total_packages = si_result['total_packages']
        total_packages += si_result['package_unit']
        si_result['total_packages'] = total_packages
        
    # seal_no = ''
    results = []
    dict_detail = {}
    parts, lst_special_char = split_to_get_parts(conts_num_seal)
    # Flag for break line. Exp.: G.W: 17905.55\n KGS
    prev_part_value = None
    lst_cont_type = []
    index = 0
    special_char = None
    for part_value in parts:
        if index > 0:
            special_char = lst_special_char[index - 1]
        
        if extract_contaner_no(prev_part_value, part_value) is not None:
            container_no = extract_contaner_no(prev_part_value, part_value)
            # Check exist container detail -> Create new container
            if 'container_no' in dict_detail:
                append_conts(results, dict_detail, lst_cont_type)
                dict_detail = {'container_no': container_no}
            else:
                dict_detail['container_no'] = container_no
        
        elif is_container_weight(part_value):
            container_weight = extract_value(prev_part_value, part_value)
            if container_weight is not None:
                if 'container_weight' in dict_detail:
                    append_conts(results, dict_detail, lst_cont_type)
                    dict_detail = {'container_weight': container_weight}
                else:
                    dict_detail['container_weight'] = container_weight

        elif is_container_measurement(part_value):
            container_measurement = extract_value(prev_part_value, part_value)
            if container_measurement is not None:
                if 'container_measurement' in dict_detail:
                    append_conts(results, dict_detail, lst_cont_type)
                    dict_detail = {'container_measurement': container_measurement}
                else:
                    dict_detail['container_measurement'] = container_measurement
        elif extract_seal_no(prev_part_value, part_value, special_char) != None and 'seal_no' not in dict_detail:
            seal_no = extract_seal_no(prev_part_value, part_value,  special_char)
            dict_detail['seal_no'] = seal_no
       
        elif is_container_type(part_value):
            is_total, container_type = extract_total_cont_type(prev_part_value, part_value)
            if 'container_type' in dict_detail :
                 is_total_old, container_type_old = extract_total_cont_type(None, dict_detail['container_type'])
            if is_total == False:
                container_type = extract_value(prev_part_value, part_value)
            if 'container_type' in dict_detail and  is_total ==  is_total_old:
                num_cont_type = num_total_cont_type(container_type)
                lst_cont_type = []
                append_conts(results, dict_detail, lst_cont_type)
                if num_cont_type > 1:
                    for i in range(num_cont_type - 1):
                        lst_cont_type.append(container_type)
                dict_detail = {'container_type': container_type}
            else:
                num_cont_type = num_total_cont_type(container_type)
                lst_cont_type = []
                if num_cont_type > 1:
                    for i in range(num_cont_type - 1 ):
                        lst_cont_type.append(container_type)
                # Not check exist because had case : 01X20 ́DC\nAKLU6022490/VN282080A
                dict_detail['container_type'] = container_type

        # Other case
        elif part_value != None and dict_detail != None:
            packages = extract_packet_value(prev_part_value, part_value)
            if packages != None:
                dict_detail['packages'] = packages
            else:
                if prev_part_value != None:
                    prev_part_value +=  part_value
                else:
                    prev_part_value = part_value

        if prev_part_value != None and part_value not in prev_part_value:
            prev_part_value = None
        index += 1

    # append last dict_detail
    append_conts(results, dict_detail, lst_cont_type)

    # Case: Weight & cbm = 2,077.600\n53.627\n12,130.900\n54.251
    str_weights = si_result.get('container_weight', '')
    str_meas = si_result.get('container_measurement', '')
    if len(str_weights) > 0 and str_weights == str_meas:
        arr = str_weights.split('\n')
        str_weights = ''
        str_meas = ''
        for i in range(len(arr)):
            if i % 2 == 0:
                if len(str_weights) > 0:
                    str_weights += '\n'
                str_weights += arr[i]
            else:
                if len(str_meas) > 0:
                    str_meas += '\n'
                str_meas += arr[i]

    # Verified 
    weights = []
    meas = []
    if (len(str_weights.strip()) > 0):
        weights = str_weights.strip().split('\n')
    if (len(str_meas.strip()) > 0):
        meas = str_meas.strip().split('\n')
            
    packages = si_result.get('packages', 'NOOOO').split('\n')
    is_verified = True
    # is_verified = verified_conts(results, conts_no, weights, meas,si_result['total_weight'], si_result['total_measurement'])
    # print('is_verified', is_verified)
    print(results)
    
    # case value has beak lines. Example: packets = 169\nCARTON(S)
    if len(results) == 1:
        if 'packages' not in results[0]:
            packet = si_result.get('packages', '').strip()
            if si_result['package_unit'].lower() not in packet.lower():
                packet += si_result['package_unit']
            results[0]['packages'] = packet

        if 'container_weight' not in results[0]:
            if len(str_weights) > 0 and si_result['weight_unit'].lower() not in str_weights.lower():
                str_weights += si_result['weight_unit']
            results[0]['container_weight'] = str_weights.strip()

        if 'container_measurement' not in results[0]:
            if len(str_meas) > 0 and si_result['measurement_unit'].lower()  not in str_meas.lower():
                str_meas += si_result['measurement_unit']
            results[0]['container_measurement'] = str_meas.strip()

        if 'container_type' not in results[0]:
            results[0]['container_type'] = extract_container_type(
                si_result.get('container_type', ''))

        elif 'container_type' in results[0]:
            results[0]['container_type'] = extract_container_type(
                results[0]['container_type'])

    else:
        container_types = si_result.get('container_type', 'NOOOO').split('\n')
        for i in range(len(results)):
            if 'packages' not in results[i] and len(packages) == len(results):
                packet = packages[i]
                if si_result['package_unit'].lower() not in packet.lower():
                    packet += si_result['package_unit']
                results[i]['packages'] = packet

            if 'container_weight' not in results[i] and len(weights) == len(results):
                weight = weights[i]
                if len(weight) > 0 and si_result['weight_unit'].lower() not in weight.lower():
                    weight += si_result['weight_unit']
                results[i]['container_weight'] = weight

            if 'container_measurement' not in results[i] and len(meas) == len(results):
                measurement = meas[i]
                if len(measurement) > 0 and si_result['measurement_unit'].lower()  not in measurement.upper():
                    measurement += si_result['measurement_unit']
                results[i]['container_measurement'] = measurement

            if 'container_type' not in  results[i] and len(container_types) == len(results):
                results[i]['container_type'] = extract_container_type(container_types[i])
            elif 'container_type' in  results[i]:
                results[i]['container_type'] = extract_container_type(results[i]['container_type'])
    
    # print('Contrainer detail: ',results)
    return results, is_verified


# -------- TEST --------
# if __name__ == '__main__':
#     with open('file_test.txt') as f:
#         lst = f.readlines()
#         text = ''
#         for line in lst:
#             if line in ['\n', '\r\n']:
#                 print('-------------')
#                 print('INPUT: ')
#                 print(text)
#                 output = extract_container_detail({'containers_detail':text})
#                 print('OUTPUT:')
#                 print(output)
#                 print('\n')
#                 text = ''
#             else:
#                 text += '\n'
#                 text += line.strip()
