import wikipedia
import random
import logging

logger = logging.getLogger(__name__)


def wiki_text(query):
    """
    Get text from Wikipedia
    """
    wiki_titles = wikipedia.search(query, results=10)
    if not wiki_titles:
        logger.error("No pages found for '{}'. Using random.".format(query))
        return(wiki_random())
    # if it returns a disambiguation page, then pick a link at random...
    idx = 0
    while idx < len(wiki_titles) - 1 and wiki_titles[idx].find("disambiguation") >= 0:
        idx += 1

    # Problem: summary() sometimes fails. So need a clause
    # that returns *something* - random page?
    wiki_title = wiki_titles[idx]
    try:
        try:
            text = wikipedia.summary(wiki_title)
        except wikipedia.exceptions.DisambiguationError as err:
            logger.info("Hit disambiguation page {}".format(wiki_title))
            disambig_count = len(err.options)
            if disambig_count == 0:
                random_page = wikipedia.random(1)
                logger.info("No links from disambiguation page {}; using random page instead {}".format(wiki_title, random_page))
                text = wikipedia.summary(random_page)
            else:
                links = [x for x in err.options if x.find("disambiguation") < 0]
                random_page = links[random.randint(0, len(links) - 1)]
                text = wikipedia.summary(random_page)
    except:
        text = wiki_random()
    return(text)


def wiki_random():
    random_page = wikipedia.random(1)
    text = wikipedia.page(random_page).content  # don't assume summary exists!
    return(text)
