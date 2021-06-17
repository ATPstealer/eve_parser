from eve_parser.parser import Parser


def run():
    parser = Parser()
    parse_json = parser.evetech_req("/universe/regions/")
    print(parse_json)
