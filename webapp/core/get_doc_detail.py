import re
import pysnooper
from flask import current_app

def extract_vessel_voyage(vessel, voyage):
    doNothing = False
    voyage_regex = re.compile(r'((V.)?[A-Z]*\d{3,5}(W|E|N|S))')
    # Split Vessel and Voyage
    if vessel is not None and vessel == voyage:
        if len(re.findall(voyage_regex, vessel)) > 0:
            voyage = re.findall(voyage_regex, vessel)[0][0]  # Group 1st
            vessel = vessel.replace(voyage, '').replace('\n', ' ')
    elif vessel != voyage and voyage is not None:
        voyage = re.findall(voyage_regex, voyage)[0][0]

    if vessel is not None:
        vessel = re.sub(r'(\s+|\W+)', ' ', vessel)
        if len(vessel) > 0 and vessel[-1].isalnum() is not True:
            vessel = vessel[:-1]
    else:
        doNothing = True

    return doNothing, vessel, voyage


def hs_code_process(si):
    """ Get HS CODE in Description of Goods or BL Types from SI-Detail,
        extract and return hs_code and desctiption
    """
    hs_code = re.sub(r'\W+', '', si.get('hs_code', ''))
    descrip = re.sub(r'\W+', '', si.get('description_of_goods', ''))
    bl_type = re.sub(r'\W+', '', si.get('bl_type', ''))
    hs_codes = []
    if hs_code != '' and hs_code in descrip:
        hs_raw = si.pop('hs_code')
        for raw_line in hs_raw.split('\n'):
            line = re.sub(r'\W+', '', raw_line).upper()
            if 'HSCODE' in line:
                remain = line.replace('HSCODE', '').replace('\n', '')
                remain = re.sub(r'[A-Z]+', '', remain)
                if remain.isdigit() and len(remain) > 4:
                    hs_codes.append(remain)
                else:
                    # CODE in line below
                    hs_line_no = hs_raw.split('\n').index(raw_line)
                    for hs_line in hs_raw.split('\n')[hs_line_no + 1:]:
                        if len(re.findall(r'[a-zA-Z]+', hs_line)) < 1:
                            for hs_code in re.findall(r'\d+', hs_line):
                                hs_codes.append(hs_code)
                        else:
                            break

        bl_type = si.get('bl_type', '')

    elif hs_code != '' and hs_code in bl_type:
        hs_raw = si.pop('hs_code')
        for raw_info in hs_raw.split('/'):
            info = re.sub(r'\W+', '', raw_info).upper()
            if 'HSCODE' in info:
                hs_code = info.replace('HSCODE', '').replace('\n', '')
                hs_code = re.sub(r'[A-Z]+', '', hs_code)
                hs_codes.append(hs_code)
                break
        bl_type = hs_raw.split('/')[0]

    else:
        hs_code = re.sub(r'[^\d]+', '', hs_code)
        hs_codes.append(hs_code)
        bl_type = si.get('bl_type', '')

    return hs_codes, bl_type


def clean_marks(si):
    """ Clear marks away from Cont_No and Seal_No,
        extract and return Total Marks and clean Cont_detail
    """
    marks_in_conts, marks_in_bkg = None, None
    conts_detail, total_mark = None, None
    doNothing = False
    conts_detail = re.sub(r'\W+', '', si.get('containers_detail', ''))
    total_marks = re.sub(r'\W+', '', si.get('total_mark', ''))
    bkg_no = re.sub(r'\W+', '', si.get('bkg_no', ''))

    if conts_detail == total_marks and total_marks != '':
        raws = si['total_mark']
        for raw_line in raws.split('\n'):
            line = re.sub(r'\W+', '', raw_line).upper()
            if 'MARK' in line:
                marks_in_conts = raw_line
                break

        if marks_in_conts is not None:
            conts_detail = raws.split(marks_in_conts)[0]
            total_mark = raws.split(marks_in_conts)[1]
            bkg_no = si.get('bkg_no', '')
        else:
            doNothing = True

    elif bkg_no == total_marks and total_marks != '':
        raws = si['total_mark']
        for raw_line in raws.split('\n'):
            line = re.sub(r'\W+', '', raw_line).upper()
            if 'BOOKINGNO' in line:
                bkg_no = line.replace('BOOKINGNO', '')
                if len(bkg_no) == 12 and bkg_no.isalnum():
                    marks_in_bkg = raw_line
                    break
        if marks_in_bkg is not None:
            total_mark = raws.split(marks_in_bkg)[0]
            conts_detail = si.get('containers_detail', '')
        else:
            doNothing = True
    else:
        doNothing = True

    return doNothing, conts_detail, total_mark, bkg_no


def extract_bkg_no(bkg_no, so_number):
    if isinstance(bkg_no, str):
        bkg_no += '\n' + so_number
        bkg_no = re.findall(re.compile(r'([a-zA-Z]{4}\d{8})'), bkg_no)
        if len(bkg_no) > 0:
            return bkg_no[0]
        else:
            return ''
    else:
        return bkg_no


def clean_content_from(descrip, contents):
    # descrip_slim = re.sub(r'\W+', '', descrip)
    descrip_lines = descrip.split('\n')
    for raw_content in contents.split('\n'):
        content_slim = re.sub(r'\W+', '', raw_content)
        for raw_descrip in descrip_lines:
            descrip_slim = re.sub(r'\W+', '', raw_descrip)
            if content_slim in descrip_slim:
                descrip = descrip.replace(
                    descrip_lines[descrip_lines.index(raw_descrip)], '')

    return re.sub(r'[\n]+', '\n', descrip)


def recheck_conts_package(conts_dict, si_result):
    """ Using for VN104917 container packages inside description.
        If cont_detail_packages's empty, extract from description & inserting
    """
    print('######## BEGIN CHECKING PACKAGES ? ########')
    packages = si_result.get('packages', True)
    description = si_result.get('description_of_goods', False)
    pUnit = None
    print(packages == description)

    if packages == description:
        conts_package = []
        for unit in current_app.config['CONTAINER_PACKAGE_UNITS']:
            re_unit = re.compile(
                r'(\d+\W*(' +
                unit + r'(s|S)?\s?(\Ws\W|\WS\W)?' +
                r')\W*)|(\W*(' +
                unit + r'(s|S)?\s?(\Ws\W|\WS\W)?' +
                r')\W*\d+)')
            units_result = re.findall(re_unit, packages)

            if (
                len(units_result) == len(conts_dict)
                ) or (
                len(units_result) == len(conts_dict) + 1
            ):
                for result in units_result:
                    print(result)
                    if len(result[0]) > len(unit):
                        print('result[0]', result[0])
                        conts_package.append(
                            re.sub(r'[^\d]+', '', result[0]))
                    elif len(result[4]) > len(unit):
                        print('result[4]', result[4])
                        conts_package.append(
                            re.sub(r'[^\d]+', '', result[4]))

                if unit.isupper():
                    pUnit = unit + 'S'
                else:
                    pUnit = unit + 's'

                break

        if len(conts_package) >= len(conts_dict):
            for i, cont in enumerate(conts_dict):
                cont['packages'] = str(conts_package[i]) + ' ' + pUnit

    return conts_dict


def recheck_total_packages(conts_dict, si_result):
    """ Re-Check total packages is equal cont_packages?
    """
    print('######## HOW ABOUT TOTAL PACKAGES ########')
    need_recheck = False
    total = ''
    if len(conts_dict) > 0:
        if 'packages' in conts_dict[0]:
            total_pkgs = si_result.get('total_packages', True)
            desctip = si_result.get('description_of_goods', False)
            if total_pkgs == desctip:
                need_recheck = True

    print('need_recheck:', need_recheck)
    print("=========================conts_dict: ",conts_dict)
    if need_recheck:
        sum_packages = sum([
            int(re.sub(r'[^\d]+', '', detail.get('packages', '0')))
            for detail in conts_dict
            if floatable(detail.get('packages', '0'))
        ])

        print('sum_packages:', sum_packages)
        unit = re.sub(r'[^a-zA-Z]+', '', conts_dict[0].get('packages', ''))

        total = str(sum_packages) + ' ' + unit

    return total, need_recheck


def clean_unit_slash(raw_unit):
    return raw_unit.replace('/', '')


def totalize_measurement(conts_dict, si_model):
    """ Using for VN100944 > HANV...6400 with good container detail but no total
        If total is empty, extract from description & inserting
    """
    print('######## BEGIN CHECKING TOTAL ########')
    for cont_measure, doc_measure in [
            ['packages', 'total_packages'],
            ['container_weight', 'total_weight'],
            ['container_measurement', 'total_measurement']
    ]:
        doc_qua, doc_unit = split_quantity_unit(si_model[doc_measure])
        if not doc_qua:
            doc_qua = '0'
        if floatable(doc_qua.replace(',', '')):
            doc_qua = float(doc_qua.replace(',', ''))
        else:
            doc_qua = 0
        conts_detail = [
            split_quantity_unit(cont.get(cont_measure, '0'))
            for cont in conts_dict
        ]

        print(cont_measure, ':', conts_detail, '|', doc_qua, '-', doc_unit)

        conts_unit = list(set([
            cont_unit
            for cont_qua, cont_unit in conts_detail
        ]))
        if len(conts_unit) == 1:
            conts_sum = sum([
                float(cont_qua.replace(',', ''))
                for cont_qua, cont_unit in conts_detail
                if floatable(cont_qua.replace(',', ''))
            ])
            conts_unit = conts_unit[0]
        else:
            conts_sum = 0
            conts_unit = ''

        if conts_sum != doc_qua and conts_unit and conts_sum > 0:
            print('### Containers', cont_measure, conts_sum,
                  '=/= SI', doc_measure, doc_qua, '###')
            if doc_measure == 'total_packages':
                si_model[doc_measure] = f"{conts_sum:,.0f}" + conts_unit
            else:
                si_model[doc_measure] = f"{conts_sum:,.3f}" + conts_unit

    return si_model


def split_quantity_unit(measurement):
    """ Split `1.435,00 KGS` -> (`1.435,00`, `KGS`) """
    return (
        re.sub(r'[a-zA-Z]+', '', measurement),
        re.sub(r'[^a-zA-Z]+', '', measurement).upper(),
    )


def floatable(str):
    try:
        float(str)
    except ValueError:
        return False
    else:
        return True


def split_por_del(por_del, pod):
    """ Split POR and DEL for case VN 105604 """
    por, podel = '', ''
    to_pod = 'TO' + re.sub(r'[^a-zA-Z]+', '', pod).upper()
    if to_pod in re.sub(r'[^a-zA-Z]+', '', por_del).upper():
        print('DEL is coming')
        podel = pod
        por_del = por_del.replace(podel, '')
        if re.search(r'^\s*RE\s*\:\s*', por_del) \
                and re.search(r'\s*TO\s*$', por_del):
            print('POR is coming')
            por_del = re.sub(r'^\s*RE\s*\:\s*', '', por_del)
            por = re.sub(r'\s*TO\s*$', '', por_del)

    return por, podel
