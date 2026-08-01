import json
import os
import random
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import numpy as np


def generate_sun_air_pressure():
    os.makedirs('data/', exist_ok=True)

    data = {}
    start_date = datetime.now()
    end_date = start_date + timedelta(days=10)
    current_date = start_date
    while current_date < end_date:
        hour = 0
        date_str = current_date.strftime('%Y-%m-%d')
        data[date_str] = dict()
        mean = 12  # Година піку (середина дня)
        std_dev = 3  # Стандартне відхилення
        peak = 1
        ses_output = peak * np.exp(-0.5 * ((np.array(hour) - mean) / std_dev) ** 2)

        wind_speed = 5 + 3 * np.sin((np.array(hour) - 9) * np.pi / 12) ** 2
        wes_output = np.where(wind_speed < 3, 0, np.where(wind_speed > 15, 5, (wind_speed - 3) * 0.5))
        # print(ses_output)
        while hour <= 24:
            data[date_str][f'{hour}:00'] = {
                "SES": {f"ses_{i}": round(random.uniform(0.01 if ses_output <= 1 else ses_output - 1,
                                                         1 if ses_output <= 1 else ses_output + 1), 2) for i
                        in
                        range(1, 19)},
                "WES": {f"wes_{i}": round(random.uniform(0.01 if wes_output <= 1 else wes_output - 1,
                                                         1 if wes_output <= 1 else wes_output + 1), 2) for i
                        in range(1, 13)}
            }
            hour += 1
        current_date += timedelta(hours=1)

    number = current_date.strftime('%d_%H_%M_%S')
    with open('data/predict_weather.json', 'w') as f:
        json.dump(data, f, indent=4)


def generate_current():
    os.makedirs('data/', exist_ok=True)

    data = {}
    start_date = datetime.now()
    end_date = start_date + timedelta(days=10)
    current_date = start_date
    date_str = current_date.strftime('%Y-%m-%d')
    hour = int(start_date.strftime('%H'))
    data[date_str] = dict()
    data[date_str][f'{hour}:00'] = {
        "CONSUMERS": {f"consumer_{i}": round(random.uniform(0.25, 1), 2) for i in range(1, 52)},
        "SES": {f"ses_{i}": round(
            random.uniform(0.01 if hour <= 12 else hour / 24 - 0.5, hour / 24 + 0.5 if hour <= 12 else hour / 24 + 0.5),
            2) for i in range(1, 19)},
        "WES": {f"wes_{i}": round(random.uniform(0.25, 2.5), 2) for i in range(1, 13)},
    }

    number = start_date.strftime('%d_%H_%M_%S')
    with open('data/current.json', 'w') as f:
        json.dump(data, f, indent=4)


def generate_historical():
    os.makedirs('data/', exist_ok=True)

    data = {}
    start_date = datetime.now()
    end_date = start_date + timedelta(days=10)
    current_date = start_date
    while current_date < end_date:
        hour = 0
        date_str = current_date.strftime('2023-%m-%d')
        data[date_str] = dict()
        while hour <= 24:
            data[date_str][f'{hour}:00'] = {
                "CONSUMERS": {f"consumer_{i}": round(random.uniform(0.25, 1), 2) for i in range(1, 52)},
                "SES": {f"ses_{i}": round(
                    random.uniform(0.01 if hour <= 12 else hour / 24 - 0.5,
                                   hour / 24 + 0.5 if hour <= 12 else hour / 24 + 0.5),
                    2) for i in range(1, 19)},
                "WES": {f"wes_{i}": round(random.uniform(0.25, 2.5), 2) for i in range(1, 13)},

            }
            hour += 1
        current_date += timedelta(hours=1)
    #
    number = start_date.strftime('%d_%H_%M_%S')
    with open('data/historical.json', 'w') as f:
        json.dump(data, f, indent=4)


def generate_tth():
    os.makedirs('data/', exist_ok=True)

    stations = {}
    start_date = datetime.now()

    for i in range(1, 10):
        stations[f'transformer_{i}'] = {
            'limit': random.randint(10, 30),
        }

    number = start_date.strftime('%d_%H_%M_%S')
    with open('data/tth.json', 'w') as f:
        json.dump(stations, f, indent=4)


def generate_random_cim_model():
    os.makedirs('data/', exist_ok=True)

    root = ET.Element('Network')
    main_substation = ET.SubElement(root, 'Substation', id='substationMain')
    name = ET.SubElement(main_substation, 'Name')
    name.text = 'Головна підстанція'
    substation_count = 0
    transformer_count = 0
    ses_count = 0
    wes_count = 0
    consumer_count = 0

    for i in range(3):
        substation_count += 1
        substation_id = f"substation_{substation_count}"
        substation = ET.SubElement(root, "Substations", id=substation_id)
        name = ET.SubElement(substation, 'Name')
        name.text = f'Підстанція {substation_count}'
        connections = ET.SubElement(substation, 'Connections')
        connection = ET.SubElement(connections, 'Connection', to='substationMain')

        for j in range(2):
            transformer_count += 1
            transformer_id = f'transformer_{transformer_count}'
            transformer = ET.SubElement(substation, 'Transformer', id=transformer_id)
            name = ET.SubElement(transformer, 'Name')
            name.text = f'Трансформатор {transformer_count}'
            transformers_connections = ET.SubElement(transformer, 'Connections')
            transformers_connection = ET.SubElement(transformers_connections, 'Connection', to=substation_id)

            for k in range(2):
                wes_count += 1
                wes = ET.SubElement(transformer, 'Wes', id=f'wes_{wes_count}')
                name = ET.SubElement(wes, 'Name')
                name.text = f'Wes {wes_count}'
                wes_connections = ET.SubElement(wes, 'Connections')
                wes_connection = ET.SubElement(wes_connections, 'Connection', to=transformer_id)

            for k in range(2):
                ses_count += 1
                ses = ET.SubElement(transformer, 'Ses', id=f'ses_{ses_count}')
                name = ET.SubElement(ses, 'Name')
                name.text = f'Ses {ses_count}'
                ses_connections = ET.SubElement(ses, 'Connections')
                ses_connection = ET.SubElement(ses_connections, 'Connection', to=transformer_id)

            for k in range(5):
                consumer_count += 1
                consumer = ET.SubElement(transformer, 'Consumer', id=f'consumer_{consumer_count}')
                name = ET.SubElement(consumer, 'Name')
                name.text = f'Споживач {consumer_count}'
                consumers_connections = ET.SubElement(consumer, 'Connections')
                consumers_connection = ET.SubElement(consumers_connections, 'Connection', to=transformer_id)

        for j in range(1):
            substation_count += 1
            substation_sub_id = f"substation_{substation_count}"
            substation_sub = ET.SubElement(root, "Substations", id=substation_sub_id)
            name = ET.SubElement(substation_sub, 'Name')
            name.text = f'Підстанція {substation_count}'
            connections = ET.SubElement(substation_sub, 'Connections')
            connection = ET.SubElement(connections, 'Connection', to=substation_id)

            for k in range(1):
                transformer_count += 1
                transformer_id = f'transformer_{transformer_count}'
                transformer = ET.SubElement(substation_sub, 'Transformer', id=transformer_id)
                name = ET.SubElement(transformer, 'Name')
                name.text = f'Трансформатор {transformer_count}'
                transformers_connections = ET.SubElement(transformer, 'Connections')
                transformers_connection = ET.SubElement(transformers_connections, 'Connection', to=substation_sub_id)

                for g in range(2):
                    ses_count += 1
                    ses = ET.SubElement(transformer, 'Ses', id=f'ses_{ses_count}')
                    name = ET.SubElement(ses, 'Name')
                    name.text = f'Ses {ses_count}'
                    ses_connections = ET.SubElement(ses, 'Connections')
                    ses_connection = ET.SubElement(ses_connections, 'Connection', to=transformer_id)

                for g in range(7):
                    consumer_count += 1
                    consumer = ET.SubElement(transformer, 'Consumer', id=f'consumer_{consumer_count}')
                    name = ET.SubElement(consumer, 'Name')
                    name.text = f'Споживач {consumer_count}'
                    consumers_connections = ET.SubElement(consumer, 'Connections')
                    consumers_connection = ET.SubElement(consumers_connections, 'Connection', to=transformer_id)

    output_file = 'data/cim_model.xml'
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    return root


if __name__ == '__main__':
    generate_tth()
    generate_historical()
    generate_sun_air_pressure()
    generate_random_cim_model()