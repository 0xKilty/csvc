import argparse
import codecs
import logging
import coloredlogs
from compress import SVFileCompressor
from decompress import SVFileDecompressor

def main(args):    
    if args.delimiter != ",":
        logger.info(f"Using delimiter '{args.delimiter}'")
    
    if args.compress:
        if not args.output_file:
            args.output_file = args.compress + ".svc"
        compressor = SVFileCompressor(args.compress, args.delimiter, args.output_file)
        compressor.compress()
    else:
        decompressor = SVFileDecompressor(args.decompress)
        decompressor.decompress()

def single_char(s):
    s = codecs.decode(s, "unicode_escape")
    if len(s) != 1:
        raise argparse.ArgumentTypeError(f"Delimiter must be a single character, got '{s}'")
    return s

if __name__ == "__main__":
    
    
    # Handle args
    parser = argparse.ArgumentParser(description="File compressor for seperated values files")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--delimiter", type=single_char, default=",", help="Delimiter for seperated value file [default: '%(default)s']")
    
    parser.add_argument(
        "-o", 
        "--output-file",
        required=False,
        metavar="<filename>", 
        help="Output to a file [default: '%(default)s']"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", "--compress", metavar="<filename>", help="Compress a file")
    group.add_argument("-d", "--decompress", metavar="<filename>", help="Decompress a file")

    args = parser.parse_args()
    
    # Handle logging
    logger = logging.getLogger("csvc")
    
    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.CRITICAL + 10
        
    coloredlogs.install(level=level, logger=logger, fmt="%(asctime)s [%(levelname)s] %(message)s")

    main(args)