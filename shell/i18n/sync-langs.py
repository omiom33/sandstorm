#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script synchronizes TAPi18n string jsons from en into other languages.
# The target language json file (ex. zh-TW.i18n.json) will have the same keys as source language,
# and untranslated strings will be copied with a prefix *_
# You can do this anytime source language is updated, the script will keep translated strings.

from io import open
import json
import sys
from collections import OrderedDict

inter_add = False;

def main():
    if len(sys.argv) is 1:
        print('Usage: "python sync-langs.py en zh-TW". The first language has higher json order priority. If the first language is en, it can be omitted.')
    elif len(sys.argv) is 2:
        first = 'en'
        second = sys.argv[1]
    else:
        first = sys.argv[1]
        second = sys.argv[2]
    with open(f'{first}.i18n.json', 'r') as f1:
        f2 = open(f'{second}.i18n.json', 'r')
        j1 = json.loads(f1.read(), object_pairs_hook=OrderedDict)
        j2 = json.loads(f2.read(),  object_pairs_hook=OrderedDict)
    f2.close()

    r2raw = comp_dict(j1, j2)
    r1 = comp_dict(j2, j1)
    r2 = align_dict(j1, r2raw)

    with open(f'{second}.i18n.json', 'w', encoding='utf-8') as out:
        out.write(json.dumps(r2, indent=2, ensure_ascii=False, separators=(',', ': ')))

    if inter_add:
        with open(f'{first}.i18n.json', 'w', encoding='utf-8') as out:
            out.write(json.dumps(r1, indent=2, ensure_ascii=False, separators=(',', ': ')))

    print('Done.')

def comp_dict(base, comp):
    result = OrderedDict(comp) if inter_add else OrderedDict()
    for key, value in base.items():
        if key in comp:
            if type(comp[key]) != type(value):
                print(f'Type mismatch!! Key={key}; {type(comp[key])} {type(value)}')
            result[key] = (
                comp_dict(value, comp[key])
                if type(value) is OrderedDict
                else comp[key]
            )

        elif type(value) is OrderedDict:
            result[key] = comp_dict(value, OrderedDict())
        elif sys.version_info[0] == 2:
            result[key] = f"*_{unicode(value)}"
        else:
            result[key] = f"*_{str(value)}"
    return result

def align_dict(base, target):
    result = OrderedDict()
    for key in base:
        if type(base[key]) is OrderedDict:
            result[key] = align_dict(base[key], target[key])
        else:
            result[key] = target[key]
    return result

main()
