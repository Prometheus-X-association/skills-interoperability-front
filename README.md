# arianneDemo

This repository is the support for Mindmatcher's "Ariane Workshops" which took place in Q4 2023.
There are 3 demos for human-computer interfaces:
- "Onthology Matching Tool", that allows users (such as startups and academia) to align their onthology to Ariane Pivot Onthology.
- "Framework Matching Tool", that allows users to align their referential to standard Framework such as ROME and ESCO.
- "Training Enhancing Tool", that allows users to "enrich" their trainings and courses with skills and skill blocks from standard frameworks such as ROME, ESCO and RNCP.

To run the program :
- run $docker build --pull --rm -f "dockerfile" -t ariane:latest "." :
- then go to the URL specified in the logs (should be 127.0.0.1:8080)

This container can be deployed on any host, given relevant port adjustements

