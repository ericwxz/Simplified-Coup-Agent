TestCoup:
	echo "#!/bin/bash" > TestCoup
	echo "python3 tester.py \"\$$@\"" >> TestCoup
	chmod u+x TestCoup