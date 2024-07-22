# Packet Trace Parser

This assignment is a bit of a warmup, reviewing basic Python string processing
operations. It also exposes you to some fundamental data processing challenges.
Additionally, you get a chance to play with real network data which will help
you acclimate to some of the terms and data we will use going forward in this
class.

You should record a packet trace using wireshark

## Requirements

Use the given print function calls in the starter code to print the following
information about your packet trace:

1. The number of unique ip addresses (you might try using a python set)
2. The names of all unique protocols observed in the trace
    - These should be comma-separated with no spaces.
3. The total number of packets captured in the trace (as an int)
    - This should be `> 1000`.
3. The total number of bytes captured in the trace (as an int)
4. The average number of bytes per packet (as an int)
5. The median number of bytes per packet (as an int)

## Recommended Steps

I would encourage you to try and determine these steps on your own based on the
requirements listed above. But if you get stuck, you are absolutely welcome to
take inspiration from these recommendations.

0. Use wireshark to capture the network traffic on your machine. **This trace
   should contain at least 1000 packets.** Stop the capture and export the
   packet trace as a csv file. The name of this file does not have to be
   anything specific.
1. Read and return the lines of the file in the `read_trace` function. Do not
   add any extra parsing in this function. Simply return the raw lines of the
   files as a list of string. (You might want to print them out as you go to
   help familiarize yourself with the data.)
2. Extract the values from each line in the `main` function. (again, printing is
   your friend here)
    - Don't forget to ignore the first line (the header). You are not allowed to
      simply delete this line from the file (imagine if you have thousands of
      such files, would you want to delete this line from each one?)
    - Don't forget that everything in a csv is a string, so convert the values
      as needed.
3. Record any information that you'll need to fulfill the requirements listed
   above.
4. Perform the necessary calculations to fulfill the requirements listed above.
5. Fill in your results into the provided print function calls.
