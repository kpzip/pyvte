# PYVTE

Python Virtual Testing Environment
The goal of this project is to allow python programs to be tested by a custom, locked-down interpreter. This allows for the theoretical conatinment of untrusted code, which can be used in application such as autograders for programming assignmetns.

## This is a work in progress
Only the very basics work right now due to pythons complex syntactic nature.
| Feature | Status |
| ------- | ------ |
| Function Declarations | :white_check_mark: Working |
| If Statements | :white_check_mark: Working |
| Return Statements | :white_check_mark: Working |
| Expression Parsing | Partially working |
| Variable declarations | Partially working |
| `elif` and `else` statements | :x: Not yet working |
| Lists & Dictionaries | :x: Not yet working |
| Classes | :x: Not yet working |
| `nonlocal` and `global` declarations | :x: Not yet working |

This is a non-exhaustive list.

## Using pyvte

Currently you can use pyvte to test python code like so:
```
python main.py <test file path> <file to test path>
```
this will run all functions with names beginning with `test` inside of \<test file path\>, with all code inside of \<file to test path\> being run inside the locked down interpreter. Note that currently you do not and should not need to import the file you are testing inside the test case file. Examples can be found in the `/src/test` folder
