# TestRigor Test Cases - Version Control

This repository provides automated version control for TestRigor test cases. Test cases are automatically fetched from the TestRigor API and saved in a readable format, allowing you to track changes over time using Git.

## 📁 Repository Structure

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

## 🚀 Setup Instructions

### 1. Configure GitHub Secrets

You need to add two secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

   - **Name**: `TESTRIGOR_AUTH_TOKEN`
   - **Value**: Your TestRigor auth token (e.g., `72e109d0-cd1c-4b32-b2df-1c11a8d56c24`)

   - **Name**: `TESTRIGOR_APP_ID`
   - **Value**: Your TestRigor app ID (e.g., `Hz3YmGnhiYqR3qhc7`)

### 2. Run the Workflow

#### Manual Trigger (Recommended for first run)

1. Go to the **Actions** tab in your GitHub repository
2. Click on **Fetch Test Cases** workflow
3. Click **Run workflow** button
4. Select the branch (usually `main`)
5. Click **Run workflow**

#### Automatic Schedule

The workflow is configured to run automatically:
- **Daily at midnight UTC** (you can modify the schedule in `.github/workflows/fetch-testcases.yml`)

## 📖 How It Works

1. **Fetch**: The workflow calls the TestRigor API using curl with your credentials
2. **Parse**: A Python script processes the JSON response
3. **Format**: Test cases are saved as individual Markdown files in `test-cases/`
4. **Commit**: Changes are automatically committed to the repository
5. **Track**: Git history tracks all changes to your test cases over time

## 📋 Viewing Test Cases

### Index File

Open [`test-cases/INDEX.md`](./test-cases/INDEX.md) for a summary of all test cases with:
- Status (enabled/disabled)
- UUID and filename
- Creation date
- Number of steps

### Individual Test Cases

Each test case is saved as `test-cases/[uuid].md` with:
- **Metadata**: UUID, status, creation/modification dates, author info
- **Test Steps**: The actual test steps in a readable format
- **Labels**: Any associated labels

## 📊 Version Control Benefits

### View History

See how test cases have changed over time:

```bash
# View all commits related to test cases
git log --oneline test-cases/

# View changes in a specific test case
git log -p test-cases/304762b6-7e2f-40bc-8e1e-9abf0a6eb67f.md

# Compare test cases between two dates
git diff @{2024-01-01} @{2024-02-01} test-cases/
```

### Track Changes

- **Additions**: New test cases appear as new files
- **Modifications**: Changes to steps or metadata show in diffs
- **Deletions**: Removed test cases are tracked in history
- **Authors**: See who created/modified each test case

### Rollback

Restore previous versions if needed:

```bash
# View a test case from a specific commit
git show abc123:test-cases/[uuid].md

# Restore a deleted test case
git checkout abc123 -- test-cases/[uuid].md
```

## 🛠️ Customization

### Change Fetch Frequency

Edit `.github/workflows/fetch-testcases.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 9 * * 1'    # Every Monday at 9 AM UTC
```

### Modify Output Format

Edit `scripts/format_testcases.py` to customize:
- Markdown formatting
- Metadata display
- File naming conventions
- Index generation

### Filter Test Cases

Add filtering logic in `format_testcases.py`:

```python
# Example: Only save enabled test cases
test_cases = [tc for tc in test_cases if not tc.get('disabled')]
```

## 🔧 Local Testing

Test the workflow locally:

```bash
# Set environment variables
$env:AUTH_TOKEN="your-auth-token"
$env:APP_ID="your-app-id"

# Fetch test cases
curl -X GET -H "auth-token: $env:AUTH_TOKEN" "https://api2.testrigor.com/api/v1/apps/$env:APP_ID/test_cases" -o test-cases-response.json

# Format test cases
python scripts/format_testcases.py

# Check the output
ls test-cases/
```

## 📝 Example Output

Each test case file looks like this:

```markdown
# Test1: Usecase1

## Metadata

- **UUID**: `af204b86-f45d-44c6-8a9f-0d6c1315477d`
- **Status**: ✅ Enabled
- **Created**: 2025-11-06 11:35:40 UTC
- **Created By**: Drishtant Singh Sengar (drishtant.singh@testrigor.com)
- **Modified**: 2025-11-06 12:48:27 UTC
- **Modified By**: Drishtant Singh Sengar (drishtant.singh@testrigor.com)

## Test Steps

```
wait 1 sec
wait 1 sec
...
```
```

## 🤝 Contributing

Feel free to enhance this workflow:
- Add notifications (Slack, email)
- Generate HTML reports
- Add test case statistics
- Integrate with other tools

## 📄 License

This is your personal test case version control system. Modify as needed!

---

**Questions?** Check the [GitHub Actions documentation](https://docs.github.com/en/actions) or [TestRigor API docs](https://testrigor.com/api-docs).
