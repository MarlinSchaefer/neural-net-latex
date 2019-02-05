class layer(object):
    def __init__(self, input_shape, output_shape, name, _layer_type=None):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.name = name
        self._layer_type = _layer_type
    
    def __str__(self):
        s = ''
        for i in range(1, self.output_shape+1):
            if not i == self.output_shape:
                s += (str(i) + '\n')
            else:
                s += str(i)
        return(s)
    
    def set_name(self, new_name):
        self.name = new_name
    
    def get_type(self):
        return(self._layer_type)
        
class Dense(layer):
    def __init__(self, output_shape, input_shape=None, name='Dense'):
        super(Dense, self).__init__(input_shape, output_shape, name, _layer_type='Dense')
    
    def __str__(self):
        return('{}:\n'.format(self.name) + super(Dense, self).__str__())
    
    def update_shapes(self):
        return
    
    #Needs to be structured:
    #%Layer name
    #(<Code>, Node name)
    #<Empty Line>
    def get_latex_lines(self, PrevNeuronName, ShowMaxTop, ShowMaxBottom, NeuronSpacing, LayerSpacing, MaxDepth):
        from network import get_vertical_skip
        #Create nodes
        nodes = []
        nodes.append(('%%{}\n'.format(self.name), None))
        
        #In- and output-shapes are assumed to be 1 dimensional
        #Decide where the cut is
        #BUG: The input_shape should actually be output shape
        if ShowMaxTop + ShowMaxBottom >= self.input_shape:
            neuronsBefore = list(range(self.input_shape))
            neuronsAfter = []
        else:
            neuronsBefore = list(range(ShowMaxTop))
            neuronsAfter = list(range(self.input_shape - ShowMaxBottom, self.input_shape))
        
        #Create neurons before cut
        #BUG: If Layer sizes don't match the neuron on the smaller layer are still at the same height as the previous layer.
        for idx, node in enumerate(neuronsBefore):
            prev_name = PrevNeuronName if idx == 0 else (self.name + '_' + str(neuronsBefore[idx-1]))
            node_name = self.name + '_' + str(node)
            if idx == 0:
                if not prev_name == None:
                    nodes.append(('\\node[Dense] (' + node_name + ') [' + 'right=' + LayerSpacing + ' of ' + prev_name + '] {};\n', node_name))
                else:
                    nodes.append(('\\node[Dense] (' + node_name + ') {};\n', node_name))
            else:
                nodes.append(('\\node[Dense] (' + node_name + ') [' + 'below=' + NeuronSpacing + ' of ' + prev_name + '] {};\n', node_name))
        
        #Check if cut exists
        if len(neuronsAfter) > 0:
            n, name = get_vertical_skip(self.name + '_vskip', nodes[-1][1], NeuronSpacing) 
            nodes += n
            for idx, node in enumerate(neuronsAfter):
                node_name = self.name + '_' + str(node)
                prev_name = name if idx == 0 else nodes[-1][1]
                nodes.append(('\\node[Dense] (' + node_name + ') [' + 'below=' + NeuronSpacing + ' of ' + prev_name + '] {};\n', node_name))
        
        nodes.append(('\n', None))
        
        #All the drawing of lines
        draw = []
        node_list = []
        for node in nodes:
            if not node[1] == None:
                node_list.append(node[1])
        
        for i in range(min([ShowMaxTop + ShowMaxBottom, self.output_shape])):
            curr_draw = []
            for node in node_list:
                curr_draw.append(('\\draw (' + node + '.east) -- (', '.west);\n'))
            draw.append(curr_draw)
        
        return((nodes, draw))

class Conv1D(layer):
    def __init__(self, number_of_filters, kernel_size, input_shape=None, name='Conv1D'):
        if input_shape == None:
            output_shape == None
        elif isinstance(input_shape, tuple):
            output_shape = (input_shape[0] - kernel_size + 1, number_of_filters)
        else:
            output_shape = (input_shape - kernel_size + 1, number_of_filters)
        
        super(Conv1D, self).__init__(input_shape, output_shape, name, _layer_type='Conv1D')
        self.number_of_filters = number_of_filters
        self.kernel_size = kernel_size
    
    def update_shapes(self):
        if self.input_shape == None:
            self.output_shape == None
        elif isinstance(self.input_shape, tuple):
            self.output_shape = (self.input_shape[0] - self.kernel_size + 1, self.number_of_filters)
        else:
            self.output_shape = (self.input_shape - self.kernel_size + 1, self.number_of_filters)
    
    def get_latex_lines(PrevNeuronName, ShowMaxTop, ShowMaxBottom, NeuronSpacing, MaxDepth):
        raise NotImplementedError('get_latex_lines is not implemented in %s' % (self.get_type()))
        return
