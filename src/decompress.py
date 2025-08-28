import logging

from header import Header

logger = logging.getLogger("csvc")

class SVFileDecompressor:
    def __init__(self, filename):
        self.filename = filename
    
    def decompress(self):
        logger.info(f"Starting decompression for '{self.filename}'")
        
        fp = open(self.filename, 'rb')
        
        logger.info(f"Reading header")
        header = Header.read_header(fp)
        
        
        fp.close()
        