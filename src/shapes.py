

class Shape():
    def loadData(self, tag, data):
        self.tag = tag

        if 'dimension' in data:
            # expect rectangular shape
            self.x = data['dimension'][0]
            self.y = data['dimension'][1]
            self.width = data['dimension'][2]
            self.height = data['dimension'][3]
            self.center_x = self.x + (self.width / 2.0)
            self.center_y = self.y + (self.height / 2.0)
        elif 'position' in data:
            # expect cirular shape
            self.center_x = data['position'][0]
            self.center_y = data['position'][1]

            if 'diameter' in data:
                self.diameter = data['diameter']
                self.radius = self.diameter / 2.0
            elif 'radius' in data:
                self.radius = data['radius']
                self.diameter = self.radius * 2.0
            else:
                msg = "Need radius or diameter given in circular shape tagged '{0}'."
                raise Exception(msg.format(tag))

            self.x = self.center_x - self.radius
            self.y = self.center_y - self.radius
            self.width = self.diameter
            self.height = self.diameter

        self.name = data.get('name', tag)
        self.description = data.get('description', '')

        self.corner_radius = data.get('corner_radius', 0)

            
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

    
class Drill(Shape):
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)

        # divide by 2.0 to have radius needed for SVG generation
        self.clearance = data.get('clearance', 0) / 2.0
        
    
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

        self.pins.sort(key=lambda p:p.tag)
                

class Pcb(Shape):
    def __init__(self):
        self.drills = []
        
    def loadData(self, data):
        Shape.loadData(self, 'pcb', data)

        for d_tag, d_data in data.get('drills', {}).items():
            drill = Drill()
            drill.loadData(d_tag, d_data)
            self.drills.append(drill)

        
class Chip(Shape):
    def loadData(self, tag, data):
        Shape.loadData(self, tag, data)

        
        
