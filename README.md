# backTCP Python Template

This is a template code for the backTCP course lab of « Computer Networking » in fall 2019 of USTC.

## Instructions

You should read this document and all comments in `backTCP.py` file, and then fill out code segments marked as `TODO` in `backTCP.py`. There's no need to change any other file but you're free to if you want.

Note that all binary data are assumes to be of the type `bytes` in this program.

It's recommended that you write this program on Python 3.6 or newer. Any issue caused by an incompatible Python version (namely, Python 3.5 or lower) will be disregarded.

### Testing & Running

The curremt version of the code contains a minimal proof of concept. You can verify that it sends and receives a file *unreliably* using the following commands:

```shell
# Generate a file for input
dd if=/dev/urandom of=output.bin bs=64k count=1 status=none

# Start a server and listen for connection
python3 recv.py output.bin

# Open another terminal and run
python3 send.py input.bin

# Compare the results
cmp input.bin output.bin
```

It will generate an `output.bin` that's identical to `input.bin`. This verifies that the code template is correct.

---

After you've filled out all required code parts, you can run the same commands against a test channel to verify your implementation.

You should consult the man page or use `--help` if you want to know which command does what.

## Regulations

If you submit your lab based on this template, you must retain the origin notice located at the end of this README document.
Other than that, the code in this repository is licensed under the MIT license.
The original author holds no liability for this repository.

> ### Origin Disclosure
>
> The backTCP-python code template is created by [iBug](https://github.com/iBug)
