'''boarddef is a tool to generate html documentation for SBCs
(sinble-board computers) from yaml description files.'''

import logging
import yaml
from jinja2 import Environment, Template, FileSystemLoader
from cmdlapp import CmdlApp


class Shape():
    def loadData(self, tag, data):
        self.tag = tag

        self.x = data['dimension'][0]
        self.y = data['dimension'][1]
        self.width = data['dimension'][2]
        self.height = data['dimension'][3]

        if 'name' in data:
            self.name = data['name']
        else:
            self.name = 'unknown'

    def getBBox(self):
        return (
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )

    def __str__(self):
        return "{tag} [{x}:{y} +{width} +{height}]".format(
            tag=self.tag, x=self.x, y=self.y,
            width=self.width, height=self.height)

    
class Pin(Shape):
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)

        self.net = data.get('net', '')


class Connector(Shape):
    pin_grids = {
        'std254': [2.54, 2.54],
    }
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)
        
        self.pin_type = data.get('pin_type', None)
        if self.pin_type != None:
            self.pin_grid = self.pin_grids[self.pin_type]

        self._createPins(data)

        
    def _createPins(self, data):
        '''Calculate the coordinates for each single pin.'''

        self.pins = []
        
        for p_tag, p_data in data.get('pins', {}).items():
            p_data['dimension'] = [
                self.x + (float(p_data['offset'][0]) * self.pin_grid[0]),
                self.y + (float(p_data['offset'][1]) * self.pin_grid[1]),
                self.x + (float((p_data['offset'][0]) + 1) * self.pin_grid[0]),
                self.y + (float((p_data['offset'][1]) + 1)* self.pin_grid[1]),
            ]

            pin = Pin()
            pin.loadData(p_tag, p_data)
            self.pins.append(pin)
                

class Pcb(Shape):
    def loadData(self, data):
        Shape.loadData(self, 'pcb', data)

        
class BoardDef():
    def getSvgViewBox(self):
        bbox = self.getBBox()

        return ' '.join(str(d) for d in bbox)
        
    def loadData(self, data):
        self.name = data['name']

        self.pcb = Pcb()
        self.pcb.loadData(data['pcb'])

        self.connectors = []
        for c_tag,c_data in data['connectors'].items():
            conn = Connector()
            conn.loadData(c_tag, c_data)
            self.connectors.append(conn)

            
    def getBBox(self):
        bbox = list(self.pcb.getBBox())

        for conn in self.connectors:
            self.updateBBox(bbox, conn.getBBox())

        return bbox


    def updateBBox(self, bbox, new_bbox):
        if new_bbox[0] < bbox[0]:
            bbox[0] = new_bbox[0]
            
        if new_bbox[1] < bbox[1]:
            bbox[1] = new_bbox[1]
            
        if new_bbox[2] > bbox[2]:
            bbox[2] = new_bbox[2]
            
        if new_bbox[3] > bbox[3]:
            bbox[3] = new_bbox[3]
            
            
            
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

        self.parser.add_argument(
            '-t', '--templates',
            help='Template files.',
            default='templates')

        
    def load_yaml(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f)

        return data


        
        
    def generate(self):
        filename = self.args.board

        data = self.load_yaml(filename)

        bdef = BoardDef()
        bdef.loadData(data)

        msg = 'Board bounding box: {0}'
        logging.info(msg.format(
            bdef.getBBox()))


        env = Environment(loader=FileSystemLoader(self.args.templates))

        t = env.get_template('template.html')

        svg = t.render(board=bdef)

        if self.args.output == '-':
            print(svg)
        else:
            with open(self.args.output, 'w') as f:
                f.write(svg)

        
if __name__ == '__main__':
    BoardDefGen().run()
