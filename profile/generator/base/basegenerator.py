class basegenerator:
    """
    Random map generator interface.
    """
    
    def generate(self, directory = None):
        """
        Generates a Random OSM Map. 
        If directory is specified, the generated map will be saved in the specified directory,
        otherwise it will be returned as string.
        
        generated(directory = None) -> None or map
        
        @type directory: string
        @param directory: absolute directory path.
        
        @rtype: None if directory is specified, otherwise string
        @return: None if directory is specified, otherwise the generated OSM Map.
        """
        raise NotImplementedError("generate: You should have implemented this method!")