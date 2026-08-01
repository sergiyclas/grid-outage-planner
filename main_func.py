import heapq
import os
from datetime import datetime

from generators import generate_current
from parsing import parse_sim, parser_current, parser_historical, parser_weather
from writer import write_output_to_file


def line_offer(COUNT_HOURS, return_details=False):
    CURRENT_TIME = datetime.now()
    CURRENT_DAY = CURRENT_TIME.strftime('%Y-%m-%d')
    CURRENT_HOUR = int(CURRENT_TIME.strftime('%H'))

    # CURRENT_TIME = '2024-08-07 12:55:44.100429'
    # CURRENT_DAY = '2024-08-07'
    # CURRENT_HOUR = 12

    generate_current()

    file_path_current = os.path.join('data', 'current.json')
    file_path_historical = os.path.join('data', 'historical.json')
    file_path_predict_weather = os.path.join('data', 'predict_weather.json')
    file_path_tth = os.path.join('data', 'tth.json')
    file_path_sim = os.path.join('data', 'cim_model.xml')

    needed_data_current = parser_current(file_path_current, COUNT_HOURS, CURRENT_HOUR, CURRENT_DAY)
    needed_data_historical = parser_historical(file_path_historical, COUNT_HOURS, CURRENT_HOUR, CURRENT_DAY)
    needed_data_predict_weather = parser_weather(file_path_predict_weather, COUNT_HOURS, CURRENT_HOUR, CURRENT_DAY)
    raw_trans_to_sub, cons_to_trans, gen_to_trans = parse_sim(file_path_sim)

    transformator_to_every = {i: [] for i in raw_trans_to_sub.keys()}

    def fuller_trans(smth_to_trans):
        for smth, transformator in smth_to_trans.items():
            transformator_to_every[transformator].append(smth)

    fuller_trans(cons_to_trans)
    fuller_trans(gen_to_trans)

    trans_to_sub = {}
    for trans_, subs_ in raw_trans_to_sub.items():
        if trans_to_sub.get(trans_, None):
            trans_to_sub[trans_].append(subs_)
        else:
            trans_to_sub[trans_] = [subs_]

    factor = {}
    for gen_or_cons in needed_data_current[CURRENT_HOUR].keys():
        for user in needed_data_current[CURRENT_HOUR][gen_or_cons]:
            factor[user] = needed_data_current[CURRENT_HOUR][gen_or_cons][user] / \
                           needed_data_historical[CURRENT_HOUR][gen_or_cons][user]

    ready_data = {}
    for adder in range(COUNT_HOURS):
        for gen_or_cons in needed_data_historical[CURRENT_HOUR + adder].keys():
            for user in needed_data_historical[CURRENT_HOUR][gen_or_cons]:
                if adder == 0:
                    ready_data[user] = {}
                    ready_data[user][CURRENT_HOUR] = needed_data_historical[CURRENT_HOUR][gen_or_cons][user]
                else:
                    ready_data[user][CURRENT_HOUR + adder] = needed_data_historical[CURRENT_HOUR + adder][gen_or_cons][
                                                                 user] * factor[user]

    transformators_data = {i: {} for i in transformator_to_every.keys()}
    for adder in range(COUNT_HOURS):
        for transformator, every in transformator_to_every.items():
            for user in every:
                if transformators_data[transformator].get(CURRENT_HOUR + adder, None):
                    if user[:3] == 'con':
                        transformators_data[transformator][CURRENT_HOUR + adder] -= ready_data[user][
                            CURRENT_HOUR + adder]
                    else:
                        transformators_data[transformator][CURRENT_HOUR + adder] += ready_data[user][
                            CURRENT_HOUR + adder]
                else:
                    if user[:3] == 'con':
                        transformators_data[transformator][CURRENT_HOUR + adder] = -1 * ready_data[user][
                            CURRENT_HOUR + adder]
                    else:
                        transformators_data[transformator][CURRENT_HOUR + adder] = ready_data[user][
                            CURRENT_HOUR + adder]

    all_priority_queues = {i: [] for i in range(CURRENT_HOUR, CURRENT_HOUR + COUNT_HOURS)}
    for adder in range(COUNT_HOURS):
        for transformator, every in transformators_data.items():
            heapq.heappush(all_priority_queues[CURRENT_HOUR + adder],
                           (transformators_data[transformator][CURRENT_HOUR + adder], trans_to_sub[transformator],
                            transformator))

    results = ''
    for i, j in all_priority_queues.items():
        results += f'\n{i} HOUR:'
        for index, (weight, subs, trans) in enumerate(j):
            if index >= 5:
                break
            results += f'\nline from {subs[0]} to {trans} = {weight}'

    valid_time = CURRENT_TIME.strftime('%Y-%m-%d-%H-%M-%S')
    os.makedirs('data', exist_ok=True)
    write_output_to_file(results, f'data/results_{valid_time}')

    if not return_details:
        return results

    return results, {
        'priority_queues': all_priority_queues,
        'raw_trans_to_sub': raw_trans_to_sub,
        'transformator_to_every': transformator_to_every,
        'first_hour': CURRENT_HOUR,
        'hours': COUNT_HOURS,
    }
