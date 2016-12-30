'''boarddef is a tool to generate HTML documentation for SBCs
(single-board computers like Raspberry Pi, etc.) from YAML description
files.

The HTML contains embedded SVG and javascript to let you interactively
explore pin functions.

'''


import logging
import yaml
from jinja2 import Environment, Template, FileSystemLoader
from cmdlapp import CmdlApp
from shapes import Pin, Connector, Pcb, Chip


        
class BoardDef():
    def getSvgViewBox(self):
        '''Returns a string suitable to be set in the SVG viewBox property.'''
        
        bbox = self.getBBox()

        return "{0} {1} {2} {3}".format(
            bbox[0],
            bbox[1],
            bbox[2] - bbox[0],
            bbox[3] - bbox[1])
        
    
    def loadData(self, data):
        self.name = data['name']

        self.pcb = Pcb()
        self.pcb.loadData(data['pcb'])

        self.connectors = []
        for c_tag,c_data in data['connectors'].items():
            conn = Connector()
            conn.loadData(c_tag, c_data)
            self.connectors.append(conn)

        self.chips = []
        for ch_tag, ch_data in data['ics'].items():
            chip = Chip()
            chip.loadData(ch_tag, ch_data)
            self.chips.append(chip)

        self.chips.sort(key=lambda ch: ch.tag)

            
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
            tool_version='0.0',
            log_stream='stderr')

    
    def setup_arg_parser(self):
        CmdlApp.setup_arg_parser(self)
                
        self.parser.add_argument(
            'board',
            help='Board definition file (yaml).')

        self.parser.add_argument(
            '-o', '--output',
            help='Output file.',
            default='-')

        self.parser.add_argument(
            '-t', '--templates',
            help='Template files.',
            default='templates')

        
    def load_yaml(self, filename):
        '''Load the YAML file data. '''

        msg = "Loading board definition from '{filename}'."
        logging.info(msg.format(
            filename=filename))
    
        with open(filename, 'r') as f:
            data = yaml.load(f)

        return data
        
        
    def generate(self):
        filename = self.args.board

        data = self.load_yaml(filename)

        bdef = BoardDef()
        bdef.loadData(data)

        msg = 'Board bounding box: {0}'
        logging.debug(msg.format(
            bdef.getBBox()))


        msg = "Using templates from directory '{0}'."
        logging.debug(msg.format(self.args.templates))
        
        env = Environment(
            loader=FileSystemLoader(self.args.templates))

        t = env.get_template('template.html')

        svg = t.render(board=bdef)

        if self.args.output == '-':
            print(svg)
        else:
            with open(self.args.output, 'w') as f:
                f.write(svg)

            msg = "Result written to '{0}'."
            logging.info(msg.format(
                self.args.output))

        
if __name__ == '__main__':
    BoardDefGen().run()
