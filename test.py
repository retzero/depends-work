#!/usr/bin/env python

import json
import xml.etree.ElementTree as ET

tree = ET.parse('builddepinfo.xml')
root = tree.getroot()

bucket = {}
sub_to_main_map = {}

def add_from(src_name, k):
    if k not in sub_to_main_map:
        sub_to_main_map[k] = {}
    sub_to_main_map[k]['main'] = src_name
    if 'from' not in sub_to_main_map[k]:
        sub_to_main_map[k]['from'] = []
    for _pd in bucket[src_name]['pkgdep']:
        if _pd not in sub_to_main_map[k]['from']:
            sub_to_main_map[k]['from'].append(_pd)

def add_to(src_name, k):
    if k not in sub_to_main_map:
        sub_to_main_map[k] = {}
    if 'to' not in sub_to_main_map[k]:
        sub_to_main_map[k]['to'] = []
    sub_to_main_map[k]['to'].append(src_name)

for child in root:
    src_name = child.attrib.get('name')
    bucket[src_name] = {'pkgdep': [], 'subpkg': []}

    for pkgdep in child.findall('pkgdep'):
        bucket[src_name]['pkgdep'].append(pkgdep.text)
        add_to(src_name, pkgdep.text)

    for subpkg in child.findall('subpkg'):
        bucket[src_name]['subpkg'].append(subpkg.text)
        add_from(src_name, subpkg.text)

    if len(bucket[src_name]['subpkg']) <= 0:
        bucket[src_name]['subpkg'].append(src_name)
        add_from(src_name, subpkg.text)


print(len(bucket.keys()))
print(len(sub_to_main_map.keys()))

check = 'sgml-common'

print(bucket[check])
print(sub_to_main_map[check])

def find_right(pkg):
    tos = []
    for pkg in bucket[check]['subpkg']:
        n = sub_to_main_map[pkg]['name']

check_list = []
while(1) {

}
