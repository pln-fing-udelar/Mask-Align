#!/usr/bin/env python
import itertools
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


# See https://stackoverflow.com/a/5434936/1165181
def pairwise(iterable: Iterable[T]) -> Iterable[tuple[T, T]]:
    """s -> (s0, s1), (s1, s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def main() -> None:
    with open("output3.txt", encoding="utf-8") as file:
        token_scores_and_gt = (line.rstrip().split(maxsplit=2) for line in file)
        token_scores_and_gt = ((float(score_str), is_part_of_the_answer_str == "True")
                               for _, score_str, is_part_of_the_answer_str in token_scores_and_gt)
        token_scores_and_gt = sorted(token_scores_and_gt, key=lambda e: e[0])

    num_true = sum(is_part_of_the_answer for _, is_part_of_the_answer in token_scores_and_gt)

    num_true_so_far = 0
    num_false_so_far = 0
    num_tokens_so_far = 0

    max_acc = 0
    best_threshold = 0

    for (score1, is_part_of_the_answer1), (score2, _) in pairwise(token_scores_and_gt):
        num_tokens_so_far += 1

        if is_part_of_the_answer1:
            num_true_so_far += 1
        else:
            num_false_so_far += 1

        acc = (num_false_so_far + num_true - num_true_so_far) / len(token_scores_and_gt)

        if acc > max_acc:
            max_acc = acc
            best_threshold = (score1 + score2) / 2

    print("The best threshold is:", best_threshold)
    print("The token-level accuracy of this threshold is (on the same data):", max_acc)


if __name__ == "__main__":
    main()
