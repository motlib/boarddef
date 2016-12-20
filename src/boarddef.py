
import yaml
from jinja2 import Environment, Template, FileSystemLoader
from cmdlapp import CmdlApp


class BoardDefGen(CmdlApp):
    def __init__(self):
        super().__init__()
        
        # Configure the CmdlApp base class
        self.configure(
            main_fct=self.generate,
            use_cfgfile=False,
            tool_name='boarddef',
            tool_version='0.0')

    
    def setup_arg_parser(self):
        CmdlApp.setup_arg_parser(self)
                
        self.parser.add_argument(
            '-b', '--board',
            help='Board definition file (yaml).',
            required=True)

        self.parser.add_argument(
            '-o', '--output',
            help='Output file.',
            default='-')
        
        
    def load_yaml(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f)

        return data


    def update_pins(self, data):
        '''Calculate the coordinates for each single pin.'''
    
        for conn in data['board']['connectors'].values():
            if not 'pins' in conn.keys():
                continue
        
            for pin in conn['pins'].values():
                pin['position'] = [
                    int(conn['dimension'][0]) + (2.54 * int(pin['offset'][0])),
                    int(conn['dimension'][1]) + 2.54 * int(pin['offset'][1]),
                ]


    def generate(self):
        filename = self.args.board

        data = self.load_yaml(filename)
        self.update_pins(data)

        env = Environment(loader=FileSystemLoader('../templates'))

        t = env.get_template('template.html')

        svg = t.render(board=data['board'])

        if self.args.output == '-':
            print(svg)
        else:
            with open(self.args.output, 'w') as f:
                f.write(svg)

        
if __name__ == '__main__':
    BoardDefGen().run()
