# HTTP fuzzer project

An HTTP fuzzer using the [kitty](https://github.com/cisco-sas/kitty) framework.

Start the fuzzer using

    python fuzzer.py

The fuzzer will begin fuzzing the tagret host/port defined in the file and start
a web server on [localhost:8081](http://localhost:8081) to show progress and
results.
