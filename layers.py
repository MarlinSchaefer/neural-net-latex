class layer(object):
    def __init__(self, input_shape, output_shape, name, _layer_type=None):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.name = name
        self._layer_type = layer_type
    
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
    
    def get_latex_lines(ShowMaxTop, ShowMaxBottom, NeuronSpacing, MaxDepth):
        

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
    
