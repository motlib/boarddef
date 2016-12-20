
import yaml
from jinja2 import Environment, Template, FileSystemLoader


def load_yaml(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f)

    return data


def update_pins(data):
    for conn in data['board']['connectors'].values():
        if not 'pins' in conn.keys():
            continue
        
        for pin in conn['pins'].values():
            print(pin)
            pin['position'] = [
                int(conn['dimension'][0]) + (2.54 * int(pin['offset'][0])),
                int(conn['dimension'][1]) + 2.54 * int(pin['offset'][1]),
            ]
                
def main():
    filename = 'opi_zero.yaml'

    data = load_yaml(filename)
    update_pins(data)

    env = Environment(loader=FileSystemLoader('.'))

    t = env.get_template('template.html')

    svg = t.render(board=data['board'])

    with open('test.html', 'w') as f:
        f.write(svg)
    
if __name__ == '__main__':
    main()
