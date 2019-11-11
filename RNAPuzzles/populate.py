from rnapuzzles.models import *

import csv
import os
# NewsModel
with open("data/News.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        created = NewsModel(
            title=row[0],
            description=row[1],
        )
        created.save()
