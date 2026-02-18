from pr_insight_engine.diff.diff_parser import GitDiffParser


def run_phase1_test():
    parser = GitDiffParser(".")
    diffs = parser.parse()

    if not diffs:
        print("No uncommitted changes detected.")
        return

    print("\nChanged Files Detected:\n")

    for d in diffs:
        print("FILE:", d.file_path)
        print("Added:", len(d.added_lines))
        print("Deleted:", len(d.deleted_lines))
        print("-" * 40)


if __name__ == "__main__":
    run_phase1_test()

print("diff test")
