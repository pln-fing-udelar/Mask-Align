#!/usr/bin/env python


def main() -> None:
    correct = 0
    total = 0

    with open("output-indexes.txt", encoding="utf-8") as pred_file, \
            open("answers_indexes.es", encoding="utf-8") as gt_file2:
        pred_file = iter(pred_file)

        next(pred_file)  # Skip the header.

        for pred_line, gt_line in zip(pred_file, gt_file2):
            pred_line = pred_line.strip()
            gt_line = gt_line.strip()

            total += 1

            if pred_line:
                pred_start_end_str = pred_line.split(':', maxsplit=1)
                pred_start, pred_end = int(pred_start_end_str[0]), int(pred_start_end_str[1]) + 1

                gt_start_end_str = gt_line.split(':', maxsplit=1)
                gt_start, gt_end = int(gt_start_end_str[0]), int(gt_start_end_str[1])

                correct += int(pred_start == gt_start and pred_end == gt_end)

    print("EM:", correct / total)


if __name__ == "__main__":
    main()
