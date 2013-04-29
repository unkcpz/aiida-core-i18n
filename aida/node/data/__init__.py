from aida.node import Node
'''
Specifications of the Data class:
Aiida Data objects are subclasses of Node and should have 

Multiple inheritance must be suppoted, i.e. Data should have methods for querying and
be able to inherit other library objects such as ASE for structures.

Architecture note:
The code plugin is responsible for converting a raw data object produced by code
to Aiida standard object format. The data object then validates itself according to its
method. This is done independently in order to allow cross-validation of plugins.

'''

class Data(Node):
    def __init__(self,*args,**kwargs):
        self._logger = super(Data,self).logger.getChild('data')
        super(Data,self).__init__(*args, **kwargs)
        # TODO here!

    def validate(self):
        '''
        Each datatype has functionality to validate itself according to a schema or 
        a procedure (e.g. see halst/schema python schema validation)
        ''' 
        return True
        
    def add_link_from(self,src,*args,**kwargs):
        from aida.node.calculation import Calculation

        if len(self.get_inputs()) > 1:
            raise ValueError("At most one node can enter a data node")
            
        if not isinstance(src, Calculation):
            raise ValueError("Data can only point to calculations and vice versa")
        
        return super(Data,self).add_link_from(src,*args, **kwargs)


    #===========================================================================
    # def add_link_to(self,dest,*args,**kwargs):
    #     from aida.node.calculation import Calculation
    #         
    #     if not isinstance(dest,Calculation):
    #         raise ValueError("Data can only point to calculations and vice versa")
    #     
    #     return super(Data,self).add_link_to(dest,*args, **kwargs)
    #===========================================================================
    
  
    def store(self):
        #TODO
        '''
        Depending on type, data object will serialize itself into a fileset, and insert data into the db.
        This is defined in the data plugin. The API needs to be defined.
        '''
        pass
    
    
    def retrieve(self):
        #TODO
                #TODO
        '''
        Depending on type, data object will read from fileset and DB to recreate the Aiida object.
        This is defined in the data plugin.
        '''
        pass
    
    