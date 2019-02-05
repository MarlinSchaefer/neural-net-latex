import layers as l
import sys
import os

def get_vertical_skip(name, prevNode, verticalSep):
    ret = []
    ret.append(('\\node[Dot] (' + str(name) + '_0) [below=' + str(verticalSep) + ' of ' + str(prevNode) + '] {};\n', None))
    ret.append(('\\node[Dot] (' + str(name) + '_1) [below=1cm of ' + str(name) + '_0] {};\n', None))
    ret.append(('\\node[Dot] (' + str(name) + '_2) [below=1cm of ' + str(name) + '_1] {};\n', None))
    return((ret, str(name) + '_2'))

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
            print("Layer counter: {}".format(self.layer_counter[layer_type]))
            self.layer_counter[layer_type] += 1
        else:
            print("Strating layer counter")
            self.layer_counter[layer_type] = 1
        
        print("Pre setting: {}".format(self.layer_counter[layer_type]))
        #Set unique name
        if layer.name == layer_type:
            print("In if")
            layer.set_name(layer_type + '_' + str(self.layer_counter[layer_type]))
        else:
            print("In else")
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
        ret.append('VLineVertrex/.style={circle, draw=black, minimum size=0pt, inner sep=0pt},\n')
        ret.append('Dot/.style={circle, draw=black, fill=black, minimum size=0.1cm, inner sep=0pt},\n')
        ret.append(']\n')
        ret.append('\n')
        return(ret)
    
    def get_last_lines(self):
        ret = []
        ret.append('\\end{tikzpicture}\n')
        ret.append('\\end{figure}\n')
        return(ret)
    
    def get_gate(self, layer_code, LayerSpacing):
        topNodeName = layer_code[-1][1][1]
        botNodeName = layer_code[-1][-2][1]
        numLayerSpacing = float(LayerSpacing[:-2])
        
        ret = []
        ret.append(('%%Gate', None))
        
        ret.append(('\\node (gateLeftTop) [right=' + str(LayerSpacing) + ' of ' + topNodeName + '] {};\n', 'gateLeftTop'))
        ret.append(('\\node (gateLeftBot) [right=' + str(LayerSpacing) + ' of ' + botNodeName + '] {};\n', 'gateLeftBot'))
        ret.append(('\\path (gateLeftTop.base) -- node (gateLeftMid) {} (gateLeftBot.base) ;\n', 'gateLeftMid'))
        
        ret.append(('\n', None))
        
        ret.append(('\\node[Dot] (gateHDotLeft) [right=' + str(LayerSpacing) + ' of gateLeftMid] {};\n', 'gateHDotLeft'))
        ret.append(('\\node[Dot] (gateHDotMid) [right=' + str(float(numLayerSpacing) / 2) + LayerSpacing[-2:] + 'cm of gateHDotLeft] {};\n', 'gateHDotMid'))
        ret.append(('\\node[Dot] (gateHDotRight) [right=' + str(float(numLayerSpacing) / 2) + LayerSpacing[-2:] + 'cm of gateHDotMid] {};\n', 'gateHDotRight'))
        
        ret.append(('\n', None))
        
        ret.append(('\\node (gateRightTop) [right=' + str(numLayerSpacing * 3) + LayerSpacing[-2:] + ' of gateLeftTop] {};\n', 'gateRightTop'))
        ret.append(('\\node (gateRightBot) [right=' + str(numLayerSpacing * 3) + LayerSpacing[-2:] + ' of gateLeftBot] {};\n', 'gateRightBot'))
        
        dr = []
        dr.append('%%Draw Gate')
        dr.append('\\draw (gateLeftTop.south) -- (gateLeftBot.north);\n')
        dr.append('\\draw (gateRightTop.south) -- (gateRightBot.north);\n')
        
        return((ret, dr))
    
    def get_latex_lines(self, **kwargs):
        first_lines = self.get_first_lines()
        last_lines = self.get_last_lines()
        #raise NotImplementedError('This function does not yet work.')
        #sys.exit(1)
        
        nodes = []
        draw = []
        
        if kwargs['ShowMaxFront'] + kwargs['ShowMaxEnd'] >= len(self.layers):
            layers_before = self.layers
            layers_end = []
        else:
            layers_before = self.layers[kwargs['ShowMaxFront']]
            layers_end = self.layers[kwargs['ShowMaxEnd']]
        
        for idx, layer in enumerate(layers_before):
            tmp_neurons, tmp_draw = layer.get_latex_lines(None if idx == 0 else (layers_before[idx-1].name + '_0'), kwargs['ShowMaxTop'], kwargs['ShowMaxBottom'], kwargs['NeuronSpacing'], kwargs['LayerSpacing'], kwargs['MaxDepth'])
            nodes.append(tmp_neurons)
            draw.append(tmp_draw)
            
        
        drawGate = []
        gate = []
        
        if not len(layers_end) == 0:
            gate, drawGate = self.get_gate(nodes, kwargs['LayerSpacing'])
            for idx, layer in enumerate(layers_end):
                tmp_neurons, tmp_draw = layer.get_latex_lines(layers_before[-1].name + '_0' if idx == 0 else (layers_end[idx-1].name + '_0'), kwargs['ShowMaxTop'], kwargs['ShowMaxBottom'], kwargs['NeuronSpacing'], kwargs['LayerSpacing'], kwargs['MaxDepth'])
                nodes.append(tmp_neurons)
                draw.append(tmp_draw)
        
        nodeCommands = []
        drawCommands = []
        for node in nodes[0]:
            nodeCommands.append(node[0])
        
        for idx, drawLayer in enumerate(draw):
            if idx < len(draw) - 1:
                output_neurons = []
                for node in nodes[idx+1]:
                    if not node[1] == None:
                        output_neurons.append(node[1])
                    nodeCommands.append(node[0])
                if len(output_neurons) == len(drawLayer):
                    #Do Stuff
                    for i, dl in enumerate(drawLayer):
                        for command in dl:
                            drawCommands.append(command[0] + output_neurons[i] + command[1])
                else:
                    raise RuntimeError('Ooops, something went wrong with the code. (network.get_latex_lines)')
                    sys.exit(1)
            
        
        core = nodeCommands + drawCommands
        
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
        
        lines = self.get_latex_lines(**opt_arg)
        
        if not os.path.isfile(file_name) or True:
            with open(file_name, 'w') as FILE:
                FILE.writelines(lines)
        else:
            print('Could not create file, as it already existed.\nRemove the file from the current directory and try again.')
