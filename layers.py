class layer(object):
    def __init__(self, input_shape, output_shape, name):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.name = name
    
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
        
class Dense(layer):
    def __init__(self, input_shape, output_shape, name='Dense'):
        super(Dense, self).__init__(input_shape, output_shape, name)
    
    def __str__(self):
        return('{}:\n'.format(self.name) + super(Dense, self).__str__())

class Conv1D(layer):
    def __init__(self, input_shape, number_of_filters, kernel_size, name='Conv1D'):
        if isinstance(input_shape, tuple):
            output_shape = (input_shape[0] - kernel_size + 1, number_of_filters)
        else:
            output_shape = (input_shape - kernel_size + 1, number_of_filters)
        
        super(Conv1D, self).__init__(input_shape, output_shape, name)
    
