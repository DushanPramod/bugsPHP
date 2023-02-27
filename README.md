# bugsPHP

This repository contains PHP bug collection

The projects
---------------
bugsPHP contains 640 bugs from the following open-source projects:

| **Project name**        | **Number of bugs** |
|-------------------------|--------------------|
| doctrine--orm           |                  1 |
| doctrine--dbal          |                  1 |
| Seldaek--monolog        |                  3 |
| composer--composer      |                 28 |
| briannesbitt--Carbon    |                  6 |
| laravel--framework      |                  2 |
| egulias--EmailValidator |                  1 |
| vimeo--psalm            |                598 |
### Note
Download the test repositories file [here](https://drive.google.com/file/d/1tJo-ikMXJVNmz32qrtZrqki5DkGywvek/view?usp=sharing), and put it with main.py file
## Commands

The command-line interface includes the following commands:

* -p: Project name
* -b: Bug number
* -t: task
    * checkout: checks-out the source code
    * install: install the necessary packages
    * test: run all the test cases
    * test-changed: run only updated test files ( or run only given test file)
* -v: bug version
    * buggy: the original buggy code
    * fixed: bug fixed code with updated test cases
    * bug_with_test: buggy code with updated test cases
* -o: output path where the source code should be checkout
* -f: test file path (not required)

#### Example commands

1. Checks-out the source code for a given bug
   ```
   python3 main.py -p composer--composer -b 1 -t checkout -v fixed -o /content/tmp/
   ```
2. Install the necessary packages
   ```
   python3 main.py -p composer--composer -b 1 -t install -v fixed -o /content/tmp/
   ```
3. Run all the test cases
   ```
   python3 main.py -p composer--composer -b 1 -t test -v fixed -o /content/tmp/
   ```
4. Run only updated test files
   ```
   python3 main.py -p composer--composer -b 1 -t test-changed -v fixed -o /content/tmp/
   ```
5. Run only given test file
   ```
   python3 main.py -p composer--composer -b 1 -t test-changed -v fixed -o /content/tmp/ -f "tests/Composer/Test/Package/Version/VersionBumperTest.php"
   ```#
