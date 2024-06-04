import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    The transition_model should return a dictionary representing the probability distribution over which page a random surfer would visit next, given a corpus of pages, a current page, and a damping factor.

    The function accepts three arguments: corpus, page, and damping_factor.
    The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    The page is a string representing which page the random surfer is currently on.
    The damping_factor is a floating point number representing the damping factor to be used when generating the probabilities.
    The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing the probability that a random surfer would choose that page next. The values in this returned probability distribution should sum to 1.
    With probability damping_factor, the random surfer should randomly choose one of the links from page with equal probability.
    With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
    For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, the page was "1.html", and the damping_factor was 0.85, then the output of transition_model should be {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}. This is because with probability 0.85, we choose randomly to go from page 1 to either page 2 or page 3 (so each of page 2 or page 3 has probability 0.425 to start), but every page gets an additional 0.05 because with probability 0.15 we choose randomly among all three of the pages.
    If page has no outgoing links, then transition_model should return a probability distribution that chooses randomly among all pages with equal probability. (In other words, if a page has no links, we can pretend it has links to all pages in the corpus, including itself.)
    """
    print("corpus: ", corpus)
    print("page: ", page)
    print("damping_factor: ", damping_factor)
    print("corpus[page]: ", corpus[page])

    pageProb = dict()
    for i in corpus:
        pageProb[i] = 0
    for j in corpus[page]:
        pageProb[j] = damping_factor / len(corpus[page])
    for k in corpus:
        pageProb[k] += (1 - damping_factor) / len(corpus)
    if len(corpus[page]) == 0:
        for l in corpus:
            pageProb[l] = 1 / len(corpus)
    print("pageProb: ", pageProb)
    sum = 0
    for m in pageProb:
        sum += pageProb[m]
    if sum < .999 or sum > 1.001:
        raise ValueError("sum of pageProb is not 1")
    return pageProb


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    The sample_pagerank function should accept a corpus of web pages, a damping factor, and a number of samples, and return an estimated PageRank for each page.

    The function accepts three arguments: corpus, a damping_factor, and n.
    The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    The damping_factor is a floating point number representing the damping factor to be used by the transition model.
    n is an integer representing the number of samples that should be generated to estimate PageRank values.
    The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s estimated PageRank (i.e., the proportion of all the samples that corresponded to that page). The values in this dictionary should sum to 1.
    The first sample should be generated by choosing from a page at random.
    For each of the remaining samples, the next sample should be generated from the previous sample based on the previous sample’s transition model.
    You will likely want to pass the previous sample into your transition_model function, along with the corpus and the damping_factor, to get the probabilities for the next sample.
    For example, if the transition probabilities are {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}, then 5% of the time the next sample generated should be "1.html", 47.5% of the time the next sample generated should be "2.html", and 47.5% of the time the next sample generated should be "3.html".
    You may assume that n will be at least 1.
    """
    print("corpus: ", corpus)
    print("damping_factor: ", damping_factor)
    print("n: ", n)
    sample = dict()
    tempdict = dict()
    for i in corpus:
        sample[i] = 0
    tempdict = transition_model(corpus, random.choice(list(corpus.keys())), damping_factor)
    for i in sample:
            sample[i] += tempdict[i]
    for j in range(n-1):
        tempdict = transition_model(corpus, random.choices(list(tempdict.keys()), weights=list(tempdict.values()))[0], damping_factor)
        for i in sample:
            sample[i] += tempdict[i]
    for k in sample:
        sample[k] /= n
    print("sample: ", sample)
    sum = 0
    for l in sample:
        sum += sample[l]
    if sum < .999 or sum > 1.001:
        raise ValueError("sum of sample is not 1")
    return sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
