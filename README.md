# TestRigor Test Cases - Version Control

This repository provides automated version control for TestRigor test cases. Test cases are automatically fetched from the TestRigor API and saved in a readable format, allowing you to track changes over time using Git.

##  Repository Structure

```
tR-TestCaseVC/
├── .github/
│   └── workflows/
│       └── fetch-testcases.yml    # GitHub Actions workflow
├── scripts/
│   └── format_testcases.py        # Python script to format test cases
├── test-cases/                     # Test cases storage (auto-generated)
│   ├── INDEX.md                   # Summary of all test cases
│   └── [uuid].md                  # Individual test case files
└── README.md                      # This file
```
