import logging, fileinput

# CONSTANTS
MESSAGE_TYPES = {'ADD': 'A', 'EXECUTE': 'E', 'TRADE': 'P', 'CANCEL': 'X'}
LOGGING_FILE = 'process_pitch_data.log'

# logging Config, might have an issue with logger creating your file locally. It should create the log file in the same directory that the script is launched from
logging.basicConfig(filename=LOGGING_FILE, filemode='w',level=logging.INFO)

# Message class
class Message:
    def __init__(self, message: str):
        # attempts to parse message string, if not sets error flag
        try:
            # should be type A,E,P,X
            self.order_type = message[9]
            
            # should be a base36 id to represent order
            self.order_id = message[10:21]
            
            # checks if message is add or execute, if so create symbol object attribute
            if self.order_type == MESSAGE_TYPES['ADD'] or self.order_type == MESSAGE_TYPES['TRADE']:
                self.symbol = str(message[29:34]).strip()
                
            # set error flag to false if message is able to be parsed
            self.error = False
        except:
            # set error flag to true if message can not be parsed
            self.error = True

# book class that reads messages         
class Book:    
    def __init__(self):
        
        #create dict to hold orders
        self.order_book = {}
        
        # create dict to hold transaction count per symbol
        self.count = {}
    
    # method that returns array of keys sorted by value 
    def sort_count(self):
        return sorted(book.count, key=book.count.get, reverse=True)
    
    # method to read messages and creates objects based off type 
    def process_message(self, line: str):
        
        # strip message to just text and create Message object
        message = Message(line.rstrip())
        
        # checks Message error flag, if Message object was able to parse message string
        if message.error:
            # log error message to process_pitch_data.log
            logging.error('ERROR PARSING MESSAGE: {}'.format(line))
        else:
            
            # check if message is type ADD, if so add the order to book's order dict
            if message.order_type == MESSAGE_TYPES['ADD']:
                self.order_book[message.order_id] = message
            
            # check if message is type EXECUTE, if so read symbol from order in book's order dict and add a transaction to books count dict. Error sends message order id to log
            elif message.order_type == MESSAGE_TYPES['EXECUTE']:
                try:
                    obj = self.order_book[message.order_id]
                    self.count[obj.symbol] = self.count.get(obj.symbol, 0) + 1
                except:
                    # log error message to process_pitch_data.log
                    logging.error('EXECUTE: cannot find order id {}'.format(message.order_id))
            
            # check if message is type TRADE, if so add a transaction to books count dict. Error sends message order id to log
            elif message.order_type == MESSAGE_TYPES['TRADE']:
                try:
                    self.count[message.symbol] = self.count.get(message.symbol, 0) + 1
                except:
                    # log error message to process_pitch_data.log
                    logging.error('TRADE cannot process trade {}'.format(message.order_id))
            
            # check if message is type CANCEL, if so remove order from book's order dict. Error sends message order id to log
            elif message.order_type == MESSAGE_TYPES['CANCEL']:
                try:
                    self.order_book.pop(message.order_id)
                except:
                    # log error message to process_pitch_data.log
                    logging.error('CANCEL: cannot find order id {}'.format(message.order_id))
            
            # every other message type is ignored
            else:
                # log's info message to process_pitch_data.log
                logging.info('MESSAGE TYPE IGNORED')

# set to run as script      
if __name__ == "__main__":
    # create instance of Book object
    book = Book()

    # read input from file passed to stdin
    for line in fileinput.input():
        # for each line process message
        book.process_message(line)

    # call book sort method to return sorted array of symbols, for each symbol print symbol and number of trades or executes ran against it
    for symbol in book.sort_count():
        print('{} \t {}'.format(symbol, book.count[symbol]))