# DreamScrape

Json data set of dream reports, scraped from [DreamBank](http://dreambank.net).

DreamBank is a neat collection of nearly 30,000 dream reports, but its data is not easy to consume. So I scraped most of the data and formatted it as json and stuck it up in this repo.

There's something profoundly depressing about 30,000 dreams – one for every day of your life – fitting into a little under 30MB (only 9.1MB gzipped!)

## Data
Dream data is stored in the `dreams/` directory. Data is broken into collections. Each dream collection looks like this:

```
dreams/alta.json
{
    "dreamer": "alta", 
    "description": "Alta: a detailed dreamer", 
    "dreams": [
        {
            "head": "1957", 
            "content": "The one at the Meads's house, where it's bigger inside than out; there's a European village just inside, with a cobblestone street and a Pied-Piper sort of man with curly hair, he can do things like juggle - I go up the back stairs [there aren't any in the real house] and then down the other side [since there's a second set, immediately] then down a short empty hallway that turns a corner, where I find a tiny room...a young woman with shoulder-length blonde hair in a pageboy is there, cooking at a stove that almost fills the room...she's nice to me. Now outside, I'm waiting for my aunt to pick me up - she arrives in a little round convertible and we go for a drive, not very far - we cross a little bridge over a creek, then double back and she drops me off at the house again. Inside (?) I sit with a couple of people, playing with a string of blue balloons."
        },
        ...
}
```

## Script
`extract.py` is the scraping script. It's super simple, and just downloads all the dreams for the collections listed in the `DREAMERS` dict to the `dreams` directory.

Requires: [requests](http://docs.python-requests.org/en/master/#) and [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/).