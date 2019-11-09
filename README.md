# backTCP Python Template

This is a template code for the backTCP course lab of « Computer Networking » in fall 2019 of USTC.

## Instructions

You should read this document and all comments in `backTCP.py` file, and then fill out code segments marked as `TODO` in `backTCP.py`. There's no need to change any other file but you're free to if you want.

Note that all binary data are assumed to be of the type `bytes` in this program.

It's recommended that you write this program on Python 3.6 or newer. Any issue caused by an incompatible Python version (namely, Python 3.5 or lower) will be disregarded.

### Testing & Running

The current version of the code contains a minimal proof of concept. You can verify that it sends and receives a file *unreliably* using the following commands:

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

There's a simple test channel implementation in `testch.py`. You should run the programs in this order:

- Start the receiver (pay attention to the address and port)
- Start the test channel. Use `-a` and `-p` options to give information (namely, address and port) about the receiver to the test channel. You can also specify the address and port to listen for the sender using `-A` and `-P` options.
- Finally, start the sender. Note that the default port for the sender is the same as that of the receiver, so you'll probably want to change (at least) the port using the `-p` option.

If you started those programs properly, packets coming out from the sender will be randomly manipulated by the test channel before going into the receiver. As of the current version of the test channel, packets will randomly encounter one of the following disorders:

- Nothing happens, packets pass through as normal
- A packet is dropped (unless it's a retransmitted packet, which will never be dropped - this is consistent with the lab specification)
- Two packets are swapped
- Three packets are shuffled and up to one of them may be duplicated or dropped (still, retransmitted packets won't be dropped, but may be shuffled or duplicated)

You should consult the man page or use `--help` if you want to know which command does what.

## Regulations

If you submit your lab based on this template, you must retain the origin notice located at the end of this README document.
Other than that, the code in this repository is licensed under the MIT license.
The original author holds no liability for this repository.

> ### Origin Disclosure
>
> The backTCP-python code template is created by [iBug](https://github.com/iBug)
