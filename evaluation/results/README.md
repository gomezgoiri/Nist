##How Interpreting the simulation results?

The execution of KDF function will print on the serial monitor something like this:

1,1,1,256,6467 - if you are checking the free memory available

or

0,1,1,256,872 - if you are checking the millisecs since the Arduino board began running the current program.

The meaning of this information is:
* 1) Type of analysis executed between memory or timing. It will be: '1' for Memory / '0' for Timing.
* 2) Point in the code in which the KDF function is invoked. It will be: '1' before to execute the KDF / '0' after the execution.
* 3) Type of PRF function used. It will be: '1' if you have used HMAC_SHA1 / '0' if you have used HMAC_SHA256.
* 4) Number of bits for the derived key generated by KDF function.
* 5) It is the value of: free ram (MB) if you have executed a Memory simulation / time (millisec) since the Arduino board began running the current program if you have executed a Timing simulation.

Look the mega_adk directory for more examples.