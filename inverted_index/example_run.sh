#!/bin/bash
#
# Runs the pipeline example
#
# NOTE: Must be in the inverted_index directory to run the script
set -Eeuxo pipefail


./pipeline.sh example_input
diff example_output/part-00000 output/part-00000
diff example_output/part-00001 output/part-00001
diff example_output/part-00002 output/part-00002
