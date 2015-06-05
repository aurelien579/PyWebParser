from config import Config
from core import Parser

if __name__ == '__main__':
    config = Config('Config.xml')
    parser = Parser(config)
    result = parser.parse('http://www.t411.io/torrents/buddy-guy-the-real-deal-live-1996-flac-blues')
    
    print(result)