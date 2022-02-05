# pythonskeletonsimple

A simple single-file Python boilerplate for writing simple command-line shell
scripts.

Use pythonskeletonsimple when the project uses only modules that are provided with the
standard Python installation. For more complicated projects, consider
[pythonskeleton](https://github.com/presto8/pythonskeleton) instead.

This project shows some simple approaches to writing modular code:

* Use the `argparse` module to parse command line options. Command line options
  are stored in the global variable ARGS since they will never change and it is
  inconvenient and unnecessary to pass them around. (For unit testing, ARGS can
  be set directly or the implementation can be separated from the UI processing
  code.)

* Use a `main()` function and put it near the top of the file. This allows
  readers of the code to quickly see what the script is doing. Put
  `parse_args()` near the top as well, which will serve as basic documentation
  for the script.

* Define and catch a `Fail` exception to easily handle fatal script errors.

* Implement helper functions and use a `NamedTuple` to store the results. Since
  NamedTuples are immutable, store intermediate results in a `dict` and then
  initialize the NamedTuple from the dict when returning from the helper
  function.
