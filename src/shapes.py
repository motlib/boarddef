

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
        return "{cname}({tag}) [{x}:{y} +{width} +{height}]".format(
            cname=self.__class__.__name__, tag=self.tag,
            x=self.x, y=self.y,
            width=self.width, height=self.height)

    
class Pin(Shape):
    '''Pin connector'''
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)

        self.net = data.get('net', '')


class Connector(Shape):
    pin_grids = {
        'std254': [2.54, 2.54],
        'pad254': [2.54, 2.54],
    }

    def __init__(self):
        self.pins = []

        
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)
        
        self.pin_type = data.get('pin_type', None)
        if self.pin_type != None:
            self.pin_grid = self.pin_grids[self.pin_type]

        self._createPins(data)

        
    def _createPins(self, data):
        '''Calculate the coordinates for each single pin.'''

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

        
class Chip(Shape):
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)

        
        
