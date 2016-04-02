# DreamScrape

Json data set of dream reports, scraped from [DreamBank](http://dreambank.net).

DreamBank is a neat collection of nearly 30,000 dream reports, but its data is not easy to consume. So I scraped most of the data and formatted it as json and stuck it up in this repo.

There's something profoundly depressing about 30,000 dreams – one for every day of your life – fitting into a little under 30MB (only 9.1MB gzipped!)

## Data
Dream data is stored in the `dreams/` directory. Data is broken into collections. Each dream collection looks like this:

```
dreams/jeff.json
{
    "dreamer": "jeff", 
    "description": "Jeff: a lucid dreamer", 
    "dreams": [
        {
            "number": "071", 
            "head": "07/12/2000", 
            "content": "I'm going to a party at Laura's house. I'm wearing a costume, half penguin (my bottom half) and my top half was probably a wizard costume (which I do have physically) because in the dream I think I referred to myself as \"the penguin wizard\". A lot of people laughed at my costume (not at me!). Then I am ..."
        },
        ...
}
```

## Script
`extract.py` is the scraping script. It's super simple, and just downloads all the dreams for the collections listed in the `DREAMERS` dict to the `dreams` directory.

Requires: [requests](http://docs.python-requests.org/en/master/#) and [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/).