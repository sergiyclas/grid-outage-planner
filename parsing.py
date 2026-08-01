import json
import xml.etree.ElementTree as ET


def parser_current(path: str, COUNT_HOURS, CURRENT_HOUR, CURRENT_DAY):
    with open(path, 'r') as file:
        data = json.load(file)
        needed_data = {}
        for i in range(1):
            hour = str(CURRENT_HOUR + i) + ':00'
            needed_data[CURRENT_HOUR + i] = data[CURRENT_DAY][hour]

    return needed_data


def parser_historical(path: str, COUNT_HOURS, CURRENT_HOUR, CURRENT_DAY):
    CURRENT_DAY = '2023' + CURRENT_DAY[4:]
    with open(path, 'r') as file:
        data = json.load(file)
        needed_data = {}
        for i in range(COUNT_HOURS):
            hour = str(CURRENT_HOUR + i) + ':00'
            needed_data[CURRENT_HOUR + i] = data[CURRENT_DAY][hour]

    return needed_data


def parser_weather(path: str, COUNT_HOURS, CURRENT_HOUR, CURRENT_DAY):
    with open(path, 'r') as file:
        data = json.load(file)
        needed_data = {}
        for i in range(COUNT_HOURS):
            hour = str(CURRENT_HOUR + i) + ':00'
            needed_data[CURRENT_HOUR + i] = data[CURRENT_DAY][hour]

    return needed_data


def parse_sim(path):
    tree = ET.parse(path)
    root = tree.getroot()

    transformer_to_substation = {}
    consumer_to_transformer = {}
    generator_to_transformer = {}

    def extract_id_from_ref(ref):
        return ref.split('#')[-1] if ref else None

    for transformer in root.findall('.//Transformer'):
        transformer_id = transformer.get('id')
        connections = transformer.find('Connections')
        if connections:
            for connection in connections.findall('Connection'):
                to_id = connection.get('to')
                if to_id and to_id.startswith('substation_'):
                    transformer_to_substation[transformer_id] = to_id

    for consumer in root.findall('.//Consumer'):
        consumer_id = consumer.get("id")
        connections = consumer.find("Connections")
        if connections:
            for connection in connections.findall("Connection"):
                to_id = connection.get('to')
                if to_id and to_id.startswith('transformer_'):
                    consumer_to_transformer[consumer_id] = to_id

    for generator in root.findall('.//Ses'):
        generator_id = generator.get("id")
        connections = generator.find("Connections")
        if connections:
            for connection in connections.findall("Connection"):
                to_id = connection.get('to')
                if to_id and to_id.startswith('transformer_'):
                    generator_to_transformer[generator_id] = to_id

    for generator in root.findall('.//Wes'):
        generator_id = generator.get("id")
        connections = generator.find("Connections")
        if connections:
            for connection in connections.findall("Connection"):
                to_id = connection.get('to')
                if to_id and to_id.startswith('transformer_'):
                    generator_to_transformer[generator_id] = to_id
    return transformer_to_substation, consumer_to_transformer, generator_to_transformer
