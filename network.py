import layers as l
import sys

class network(object):
    def __init__(self, layers=None, constructor=None):
        self.layer_counter = {}
        
        if layers == None:
            self.layers = []
        elif type(layers) == list:
            for layer in layers:
                if not isinstance(layer, l.layer):
                    self.layer_exception()
            self.layers = layers
            self.generate_layer_counter()
        else:
            self.layer_exception()
        
        if not constructor == None:
            self.layers = []
            self.construct_network(constructor)
    
    def generate_layer_counter(self):
        self.layer_counter = {}
        for layer in self.layers:
            curr_name = type(layer).__name__
            if curr_name in self.layer_count:
                self.layer_count[curr_name] += 1
            else:
                self.layer_count[curr_name] = 1
    
    def layer_exception(self):
        raise TypeError('The layers provided need to be a list of layer objects.')
        sys.exit(1)
    
    def constructor_exception(self):
        raise TypeError('The constructor needs to be a list containing tuples (ouput_shape, layer_name), where the layer name is supported in the module layers. [For the first entry you need (input_shape, output_shape, layer_name)]')
        sys.exit(1)
    
    """
    TODO
    def construct_network(self, c):
        #Sanity check the constructor
        if not isinstance(c, list):
            self.constructor_exception()
        
        #Filter possible layers
        standards = ['__builtins__', '__doc__', '__file__', '__name__', '__package__', 'layer']
        possibilities = []
        for name in dir(l):
            if not name in standards:
                possibilities.append(name)
        
        for idx, layer in enumerate(c):
            if not (isinstance(layer, tuple) and len(layer) == (3 if idx == 0 else 2) and (layer[2] if idx == 0 else layer[1]) in possibilities):
                self.constructor_exception()
            else:
                layer_name = layer[2] if idx == 0 else layer[1]
                output_shape = layer[1] if idx == 0 else layer[0]
                input_shape = layer[0] if idx == 0 else self.layers[idx-1].output_shape
                
                if layer_name in self.layer_counter:
                    self.layer_counter[layer_name] += 1
                else:
                    self.layer_counter[layer_name] = 1
                
                s = 'self.layers.append(l.' + layer_name + '(' + str(input_shape) + ',' + str(output_shape) + ',name="' + layer_name + '_' + str(self.layer_counter[layer_name]) + '"))'
                
                exec(s)
    """
    
    def add(self, layer):
        #Check if layer is supported
        if not isinstance(layer, l.layer):
            raise TypeError('Not a supported layer.')
        
        #Adjust the counting of layer types
        layer_type = type(layer).__name__
        if layer_type in self.layer_counter:
            self.layer_counter[layer_type] += 1
        else:
            self.layer_counter[layer_type] = 1
        
        #Set unique name
        if layer.name == layer_type:
            layer.set_name(layer_type + '_' + str(self.layer_counter[layer_type]))
        else:
            tmp_counter = 0
            for existing in self.layers:
                if existing.name == layer.name:
                    counter += 1
            if not counter == 0:
                layer.set_name(layer.name + '_' + str(counter))
        
        #Add layer to network
        self.layers.append(layer)
