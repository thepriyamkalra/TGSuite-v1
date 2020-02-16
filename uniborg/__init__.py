# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .uniborg import *
import os
import re
z=os.popen("pip  --version")
sr=z.read()
x = re.search(r"(\d+)\.(\d+)\.(\d+)", sr)
initpipversion=x.group(1)
if int(initpipversion) < 20:
	os.system("pip install  --upgrade pip")
else:
	print("already upgraded version")
