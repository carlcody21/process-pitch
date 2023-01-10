# Process Pitch Messages

Simple script written to process pitch messages of type 'A', 'E', 'P', and 'X'. 

The script can be run by following the below outline. Pitch messages are read in to stdin by passing a file of messages when running the script.

`python process_messages.py <file of pitch messages>`

`ex: python process_messages.py pitch_example_data.txt`

The script was developed using Python 3.10.0 and only uses built in modules.

When ran a log file, `process_pitch_data.log`, is created in the directory from which the script is ran. Error and info logs are sent to the file.
