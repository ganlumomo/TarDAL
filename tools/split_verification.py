import json
import logging
from functools import reduce
from pathlib import Path


def read_split(root):
    root = Path(root)
    # read split from json file
    trains = json.load((root / 'm3fd-train.json').open('r'))
    vals = json.load((root / 'm3fd-val.json').open('r'))
    tests = json.load((root / 'm3fd-test.json').open('r'))
    print('\n ------ overall ------ ')
    categories_counter(trains, vals, tests)

    challenge_trains = json.load((root / 'm3fd-challenge-train.json').open('r'))
    challenge_vals = json.load((root / 'm3fd-challenge-val.json').open('r'))
    challenge_tests = json.load((root / 'm3fd-challenge-test.json').open('r'))
    print('\n ------ challenge ------ ')
    categories_counter(challenge_trains, challenge_vals, challenge_tests)
        
    daytime_trains = json.load((root / 'm3fd-daytime-train.json').open('r'))
    daytime_vals = json.load((root / 'm3fd-daytime-val.json').open('r'))
    daytime_tests = json.load((root / 'm3fd-daytime-test.json').open('r'))
    print('\n ------ daytime ------ ')
    categories_counter(daytime_trains, daytime_vals, daytime_tests)

    night_trains = json.load((root / 'm3fd-night-train.json').open('r'))
    night_vals = json.load((root / 'm3fd-night-val.json').open('r'))
    night_tests = json.load((root / 'm3fd-night-test.json').open('r'))
    print('\n ------ night ------ ')
    categories_counter(night_trains, night_vals, night_tests)

    overcast_trains = json.load((root / 'm3fd-overcast-train.json').open('r'))
    overcast_vals = json.load((root / 'm3fd-overcast-val.json').open('r'))
    overcast_tests = json.load((root / 'm3fd-overcast-test.json').open('r'))
    print('\n ------ overcast ------ ')
    categories_counter(overcast_trains, overcast_vals, overcast_tests)


def categories_counter(trains, vals, tests):
    print('\nTrain')
    for cat in trains['categories']:
        count = 0
        for ann in trains['annotations']:
            if ann['category_id'] == cat['id']:
                count += 1
        print(cat['name'], ": ", count)
    print('\nVal')
    for cat in vals['categories']:
        count = 0
        for ann in vals['annotations']:
            if ann['category_id'] == cat['id']:
                count += 1
        print(cat['name'], ": ", count)
    print('\nTest')
    for cat in tests['categories']:
        count = 0
        for ann in tests['annotations']:
            if ann['category_id'] == cat['id']:
                count += 1
        print(cat['name'], ": ", count)


if __name__ == '__main__':
    # scenario_counter('/home/carson/data/m3fd/meta/scenario.json')
    read_split('/home/carson/data/m3fd/meta')
