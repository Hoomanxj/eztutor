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
    print("pages", pages)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
        # Initialize probability distribution
    distribution = {}
    all_pages = corpus.keys()
    linked_pages = corpus[page]
    
    if not linked_pages:
        # If no outgoing links, treat it as linking to all pages
        linked_pages = all_pages

    for page in all_pages:
        # Start with the probability from the damping factor
        distribution[page] = (1 - damping_factor) / len(all_pages)
        
        # Add the probability from the linked pages
        if page in linked_pages:
            distribution[page] += damping_factor / len(linked_pages)
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rand_page = random.choice(list(corpus.keys()))

    visit_count = dict()
    for _ in range(n):
        probs = transition_model(corpus, rand_page, damping_factor)
        rand_page = random.choices(list(probs.keys()), weights=probs.values(), k=1)[0]

        if rand_page in visit_count:
            visit_count[rand_page] += 1
        else:
            visit_count[rand_page] = 1

    for key, value in visit_count.items():

        visit_count[key] = value / n

    return visit_count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    TOLERANCE = 0.001
    # Initialize all pages with a uniform PageRank value
    num_pages = len(corpus)
    ranks = {page: 1 / num_pages for page in corpus}

    # Iterate until convergence
    while True:
        new_ranks = {}
        for page in corpus:
            rank_sum = 0
            for other_page in corpus:
                if page in corpus[other_page]:
                    # Other page links to the current page
                    rank_sum += ranks[other_page] / len(corpus[other_page])
            
            # Apply damping factor and the uniform distribution
            new_ranks[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum

        # Check for convergence
        max_diff = max(abs(new_ranks[page] - ranks[page]) for page in corpus)
        if max_diff < TOLERANCE:
            break

        # Update ranks for the next iteration
        ranks = new_ranks

    return ranks


if __name__ == "__main__":
    main()
