
import logging
import yaml
from jinja2 import Environment, Template, PackageLoader
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
                    float(conn['dimension'][0]) + (2.54 * float(pin['offset'][0])),
                    float(conn['dimension'][1]) + 2.54 * float(pin['offset'][1]),
                ]

    def check_dim(self, dim, dmin, dmax):
        dext = [dim[0] + dim[2], dim[1] + dim[3]]
        
        if dim[0] < dmin[0]:
            dmin[0] = dim[0]
        if dim[1] < dmin[1]:
            dmin[1] = dim[1]

        if dext[0] > dmax[0]:
            dmax[0] = dext[0]
        if dext[1] > dmax[1]:
            dmax[1] = dext[1]
            

    def find_overall_dimensions(self, data):
        dmin = [0, 0]
        dmax = [0, 0]

        self.check_dim(data['board']['pcb']['dimension'], dmin, dmax)

        for lst in ('connectors', 'ics'):
            for obj in data['board'][lst].values():
                self.check_dim(obj['dimension'], dmin, dmax)
        
        logging.info('Board bounding box: {0} {1}'.format(dmin, dmax))

        return [dmin[0], dmin[1], dmax[0] - dmin[0], dmax[1] - dmin[1]]

    
    def set_viewport(self, data):
        dims = self.find_overall_dimensions(data)

        dist = 0
        
        data['board']['viewport'] = [
            dims[0] - dist,
            dims[1] - dist,
            dims[2] + dist,
            dims[3] + dist
        ]
        
        
    def generate(self):
        filename = self.args.board

        data = self.load_yaml(filename)
        self.update_pins(data)

        self.set_viewport(data)

        env = Environment(loader=PackageLoader('boarddef', 'templates'))

        t = env.get_template('template.html')

        svg = t.render(board=data['board'])

        if self.args.output == '-':
            print(svg)
        else:
            with open(self.args.output, 'w') as f:
                f.write(svg)

        
if __name__ == '__main__':
    BoardDefGen().run()
