#!/usr/bin/env python

import os
import sys
import json
from pprint import pprint
import xml.etree.ElementTree as ET


def read_dep_xml(fname='builddepinfo.xml'):
    tree = ET.parse(fname)
    root = tree.getroot()
    bucket = {}
    sub_to_main_map = {}
    for child in root:
        src_name = child.attrib.get('name')
        bucket[src_name] = {'pkgdep': [], 'subpkg': []}
        for pkgdep in child.findall('pkgdep'):
            bucket[src_name]['pkgdep'].append(pkgdep.text)
        for subpkg in child.findall('subpkg'):
            bucket[src_name]['subpkg'].append(subpkg.text)
            sub_to_main_map[subpkg.text] = src_name
        if src_name not in bucket[src_name]['subpkg']:
            bucket[src_name]['subpkg'].append(src_name)
        if src_name not in sub_to_main_map:
            sub_to_main_map[src_name] = src_name
    print('Total packages: {}'.format(len(bucket.keys())))
    return bucket, sub_to_main_map

def make_adj_list(bucket, sub_to_main_map):
    packages = sorted(bucket.keys())
    deps = {}
    rdeps = {}
    for x in range(len(packages)):
        deps[x] = []
        rdeps[x] = []

    # Replace sub packages to main package and remove duplicate
    for pkg_id, pkg_name in enumerate(packages):
        for dep in bucket[pkg_name].get('pkgdep'):
            if dep not in sub_to_main_map:
                continue
            dep_id = packages.index(sub_to_main_map[dep])
            if pkg_id not in deps[dep_id]:
                deps[dep_id].append(pkg_id)
            rdeps[pkg_id].append(dep_id)

    return packages, deps, rdeps

bucket, sub_to_main_map = read_dep_xml()
packages, adj_list, adj_rev_list = make_adj_list(bucket, sub_to_main_map)


def find_full_link(pkg_name):

    pid = packages.index(pkg_name)
    to_visit = [pid]
    visited = [[], []]

    ##############################
    # Find forward/backward deps #
    ##############################
    def find_links(pid, forward=0):
        answer = []
        queue = [pid]
        while len(queue) > 0:
            to_check = queue.pop(0)
            if to_check in visited[forward]:
                continue
            visited[forward].append(to_check)
            if to_check not in to_visit:
                to_visit.append(to_check)
            if packages[to_check] not in answer:
                answer.append(packages[to_check])
            if forward == 0:
                for i in adj_list[to_check]:
                    queue.append(i)
            elif forward == 1:
                for i in adj_rev_list[to_check]:
                    queue.append(i)
        return answer

    answer = []
    while len(to_visit) > 0:
        cid = to_visit.pop(0)
        answer.extend(find_links(cid, 0))
        answer.extend(find_links(cid, 1))
        answer = list(set(answer))

    return answer

for i in packages:
    print("{} => {}".format(i, len(find_full_link(i))))

sys.exit(0)

def queue_topo_sort(adj_list):
    queue = []
    in_degree = [0] * len(adj_list)
    answer = []

    for i in range(len(adj_list)):
        for j in range(len(adj_list)):
            temp = adj_list[j]
            for k in range(len(temp)):
                if temp[k] == i:
                    in_degree[i] += 1

    for i in range(len(in_degree)):
        if in_degree[i] == 0:
            queue.append(i)

    while queue:
        answer.append(queue)

        new_arr = []
        for i in queue:
            for j in range(len(adj_list[i])):
                idx = adj_list[i][j]
                in_degree[idx] -= 1
                if in_degree[idx] == 0:
                    new_arr.append(idx)

        queue = new_arr

    for idx, item in enumerate(answer):
        print("\n\nLevel {} =================".format(idx))
        print([packages[x] for x in item])

queue_topo_sort(adj_list)
