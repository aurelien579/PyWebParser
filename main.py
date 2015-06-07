from core import Parser, Config

if __name__ == '__main__':
	config = Config('Config.xml')
	parser = Parser(config)
	t = parser.parse('http://www.imdb.com/title/tt2312718/?ref_=nm_flmg_act_6')

	for genre in t.genres:
		print(genre.name)
