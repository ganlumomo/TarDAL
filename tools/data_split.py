import json
import logging
from functools import reduce
from pathlib import Path
import numpy as np


def scenario_counter(src):
    # read scenario from json file
    src = Path(src)
    scenarios = json.load(open(src, 'r'))
    # output as tree format
    logging.debug(f'total scenarios: {len(scenarios)}')
    tot_t_frame, tot_v_frame = 0, 0
    for scenario in scenarios:
        t_frame, v_frame = 0, 0
        frame_buf = []
        # count frame
        for scene in scenario['scene']:
            frame = 0
            for fr in scene['range']:
                frame += fr['max'] - fr['min'] + 1
            frame_buf.append(f' | -- {scene["name"]} (frame: {frame}, mode: {scene["mode"]})')
            if scene['mode'] == 'train':
                t_frame += frame
            else:
                v_frame += frame
        # output
        logging.debug(f'-- {scenario["name"]} (scenes: {len(scenario["scene"])}, train: {t_frame}, val: {v_frame})')
        _ = [logging.debug(x) for x in frame_buf]
        tot_t_frame += t_frame
        tot_v_frame += v_frame
    logging.debug(f'total train frame: {tot_t_frame}, total val frame: {tot_v_frame}')


def generate_meta(root):
    root = Path(root)
    # read scenario from json file
    train_frame, val_frame, test_frame = [], [], []
    scenarios = json.load((root / 'meta' / 'scenario.json').open('r'))
    trains = json.load((root / 'meta' / 'instances_train2014.json').open('r'))
    tests = json.load((root / 'meta' / 'instances_val2014.json').open('r'))
    # count train val
    for train in trains['images']:
        frame = int(train['file_name'][:-4])
        if np.random.uniform(0.0, 1.0) < 0.8:
            train_frame.append(frame)
        else:
            val_frame.append(frame)
    for test in tests['images']:
        frame = int(test['file_name'][:-4])
        test_frame.append(frame)
    # sort by index
    train_frame.sort()
    val_frame.sort()
    test_frame.sort()
    # write to file
    (root / 'meta' / 'train.txt').write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}\n' for x in train_frame]))
    (root / 'meta' / 'val.txt').write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}\n' for x in val_frame]))
    (root / 'meta' / 'test.txt').write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}\n' for x in test_frame]))

    # count frame
    for scenario in scenarios:
        print(scenario['name'])
        sub_train_frame, sub_val_frame, sub_test_frame = [], [], []
        for scene in scenario['scene']:
            for fr in scene['range']:
                frames = list(range(fr['min'], fr['max'] + 1))
                # if scene['mode'] == 'train':
                #     t_frame += frame
                # else:
                #     v_frame += frame
                for frame in frames:
                    if frame in train_frame:
                        sub_train_frame.append(frame)
                    elif frame in val_frame:
                        sub_val_frame.append(frame)
                    elif frame in test_frame:
                        sub_test_frame.append(frame)
        # sort by index
        sub_train_frame.sort()
        sub_val_frame.sort()
        sub_test_frame.sort()
        # write to file
        train_txt = scenario['name'] + '_train.txt'
        val_txt = scenario['name'] + '_val.txt'
        test_txt = scenario['name'] + '_test.txt'
        (root / 'meta' / train_txt).write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}\n' for x in sub_train_frame]))
        (root / 'meta' / val_txt).write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}\n' for x in sub_val_frame]))
        (root / 'meta' / test_txt).write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}\n' for x in sub_test_frame]))
    # total frame
    logging.info(f'total train frame: {len(train_frame)}, total val frame: {len(val_frame)}, total test frame: {len(test_frame)}')


if __name__ == '__main__':
    # scenario_counter('/home/carson/data/m3fd/meta/scenario.json')
    generate_meta('/home/carson/data/m3fd')
