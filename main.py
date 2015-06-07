from core import Parser, Config

if __name__ == '__main__':
	config = Config('Config.xml')
	parser = Parser(config)
	t = parser.parse('http://www.t411.io/torrents/beethoven-derniers-quatuors--cordes-borodin-quartet-flac')

	print(t.name)
