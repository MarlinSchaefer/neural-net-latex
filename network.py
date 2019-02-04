import layers as l
import sys
import os

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
        """Add a layer to the network.
        
        Arguments
        ---------
        layer : class
            A layer.layers object with all necessary parameters set.
        """
        #Check if layer is supported
        if not isinstance(layer, l.layer):
            raise TypeError('Not a supported layer.')
            sys.exit(1)
        
        if len(self.layers) == 0 and layer.input_shape == None:
            raise TypeError("Input shape of the first layer must not be 'None'.")
            sys.exit(1)
        
        #Adjust the counting of layer types
        layer_type = layer.get_type()
        if layer_type in self.layer_counter:
            self.layer_counter[layer_type] += 1
        else:
            self.layer_counter[layer_type] = 1
        
        #Set unique name
        if layer.name == layer_type:
            layer.set_name(layer_type + '_' + str(self.layer_counter[layer_type]))
        else:
            tmp_counter = 1
            for existing in self.layers:
                if existing.name == layer.name:
                    tmp_counter += 1
            if not tmp_counter == 1:
                layer.set_name(layer.name + '_' + str(counter))
        
        #Fix layer input_shape
        if layer.input_shape == None:
            layer.input_shape = self.layers[-1].output_shape
            layer.update_shapes()
        
        #Add layer to network
        self.layers.append(layer)
    
    #TODO: Make this more sufisticated, i.e. customizable
    def get_first_lines(self):
        ret = []
        ret.append('\\begin{figure}\n')
        ret.append('\\begin{tikzpicture}[\n')
        ret.append('Dense/.style={circle, draw=black, very thick, minimum size=2cm},\n')
        ret.append('Conv1D/.style={circle, draw=black, very thick, minimum size=2cm},\n')
        ret.append(']\n')
        ret.append('\n')
        return(ret)
    
    def get_last_lines(self):
        ret = []
        ret.append('\\end{tikzpicture}\n')
        ret.append('\\end{figure}\n')
    
    def get_latex_lines(self, **kwargs):
        first_lines = self.get_first_lines()
        last_lines = self.get_last_lines()
        raise NotImplementedError('This function does not yet work.')
        sys.exit(1)
        
        core = []
        
        if kwargs['ShowMaxFront'] + kwargs['ShowMaxEnd'] >= len(self.layers):
            layers_front = self.layers
            layers_end = []
        else
            layers_front = self.layers[kwargs['ShowMaxFront']]
            layers_end = self.layers[kwargs['ShowMaxEnd']]
        
        for layer in layers_before:
            core += layer.get_latex_lines(kwargs['ShowMaxTop'], kwargs['ShowMaxBottom'], kwargs['NeuronSpacing'], kwargs['MaxDepth'])
        
        if not len(layers_end) == 0:
            #TODO: Need two vertical lines with dots in between like to indicate network has more layers in between and to terminate lines.:
            #   |     |
            #   | ··· |
            #   |     |
            core += #Latex Code for the above
            for layer in layers_end:
                core += layer.get_latex_lines(kwargs['ShowMaxTop'], kwargs['ShowMaxBottom'], kwargs['NeuronSpacing'], kwargs['MaxDepth'])
        
        return(first_lines + core + last_lines)
    
    def to_latex(self, file_name, **kwargs):
        opt_arg = {}
        opt_arg['ShowMaxTop'] = 3
        opt_arg['ShowMaxBottom'] = 3
        opt_arg['MaxDepth'] = 2
        opt_arg['ShowMaxFront'] = 3
        opt_arg['ShowMaxEnd'] = 3
        opt_arg['LayerSpacing'] = '3cm'
        opt_arg['NeuronSpacing'] = '1cm'
        
        for k, v in kwargs:
            if k in opt_arg:
                opt_arg[k] = v
            else:
                raise AttributeError("'to_latex' does not have an option '%s'" % str(key))
                sys.exit(1)
        
        lines = self.get_latex_lines(self, **opt_arg)
        
        if not os.path.isfile(file_name):
            with open(file_name, 'w') as FILE:
                FILE.writelines(lines)
        else:
            print('Could not create file, as it already existed.\nRemove the file from the current directory and try again.')
