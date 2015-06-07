# PyWebParser

This is a simple, config based web parser in python.

## Example
Config:
```xml
<pages>
	<page url="http://www.imdb.com/title/.*">
		<model name="ImdbMovieInfo">
			<field type="str" name="title" parser="SimpleField" xpath="//span[contains(@itemprop, 'name')]" />
			<field type="Genre" name="genres" parser="ListField" xpath="//div[contains(@class, 'infobar')]" xpath_iter="a">
				<model name="Genre">
					<field type="str" name="name" parser="SimpleField" xpath="span"/>
				</model>
			</field>
		</model>
	</page>
</pages>
```

main:
```python
config = Config('Config.xml')
parser = Parser(config)
movie = parser.parse('http://www.imdb.com/title/tt2312718/?ref_=nm_flmg_act_6')

for genre in movie.genres:
	print(genre.name)

print(movie.title)
```

result:
```
Action
Crime
Drama
Homefront
```