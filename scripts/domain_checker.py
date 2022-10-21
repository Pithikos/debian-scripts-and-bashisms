import sys
import math
# import whois
import argparse

parser = argparse.ArgumentParser(description="Bulk check for domains")
parser.add_argument('--generate', type=str, help='Generate domains from given list of words')
parser.add_argument('--filter', type=str, help='Only keep domains containing a specific word (helpful with --generate)')
parser.add_argument('--group-results', type=int, help='Split results in groups', default=None)
args = parser.parse_args()


def generate_words(wordlist):
    words_start = set()
    words_end = set()
    words_mid = set()
    for word in wordlist:
        if word.startswith("-"):
            words_end.add(word.strip("-"))
        elif word.endswith("-"):
            words_start.add(word.strip("-"))
        else:
            words_mid.add(word)

    # Make combinations accordingly
    final_words = set()
    for s in words_start:
        for e in words_end:
            final_words.add(s+e)
        for m in words_mid:
            final_words.add(s+m)
    for m in words_mid:
        for e in words_end:
            final_words.add(m+e)
    for m1 in words_mid:
        for m2 in words_mid:
            if m1 != m2:
                final_words.add(m1+m2)
    final_words = list(sorted(final_words))

    return final_words


if __name__ == "__main__":
    if args.generate:
        wordlist = args.generate.split(",")

        # Generate words
        results = generate_words(wordlist)

        # Filter results
        if args.filter:
            filtered_results = []
            filterlist = args.filter.split(",")
            for f in filterlist:
                for r in results:
                    if f in r:
                        filtered_results.append(r)
            results = filtered_results
            
        # Group results in equal chunks (for copy/pasting into services with limits)
        if args.group_results:
            GROUP_SIZE = args.group_results
            bulk_searches = []
            for i in range(math.ceil(len(results)/GROUP_SIZE)):
                selected_words = list(results)[i*GROUP_SIZE:(i+1)*GROUP_SIZE]
                bulk_searches.append(",".join(selected_words))
            for i, group in enumerate(bulk_searches, start=1):
                print(f"\nGROUP {i}")
                print(group)
        else:
            for r in results:
                print(r)