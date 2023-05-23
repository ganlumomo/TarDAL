import json
import logging
from functools import reduce
from pathlib import Path


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
    t_frame, v_frame = [], []
    scenarios = json.load((root / 'meta' / 'scenario.json').open('r'))
    trains = json.load((root / 'meta' / 'instances_train2014.json').open('r'))
    vals = json.load((root / 'meta' / 'instances_val2014.json').open('r'))
    # count train val
    for train in trains['images']:
        frame = int(train['file_name'][:-4])
        t_frame.append(frame)
    for val in vals['images']:
        frame = int(val['file_name'][:-4])
        v_frame.append(frame)
    # sort by index
    t_frame.sort()
    v_frame.sort()
    # write to file
    (root / 'meta' / 'train.txt').write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}.png\n' for x in t_frame]))
    (root / 'meta' / 'val.txt').write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}.png\n' for x in v_frame]))
    # count frame
    for scenario in scenarios:
        print(scenario['name'])
        tt_frame, vv_frame = [], []
        for scene in scenario['scene']:
            for fr in scene['range']:
                frames = list(range(fr['min'], fr['max'] + 1))
                # if scene['mode'] == 'train':
                #     t_frame += frame
                # else:
                #     v_frame += frame
                for frame in frames:
                    if frame in t_frame:
                        tt_frame.append(frame)
                    else:
                        vv_frame.append(frame)
        # sort by index
        tt_frame.sort()
        vv_frame.sort()                
        # write to file
        tt_txt = scenario['name'] + '_train.txt'
        vv_txt = scenario['name'] + '_val.txt'
        (root / 'meta' / tt_txt).write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}.png\n' for x in tt_frame]))
        (root / 'meta' / vv_txt).write_text(reduce(lambda i, j: i + j, [f'{str(x).zfill(5)}.png\n' for x in vv_frame]))
    # total frame
    logging.info(f'total train frame: {len(t_frame)}, total val frame: {len(v_frame)}')


if __name__ == '__main__':
    # scenario_counter('/home/carson/data/m3fd/meta/scenario.json')
    generate_meta('/home/carson/data/m3fd')
