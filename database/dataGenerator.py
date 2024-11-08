import database.model as md
from datetime import datetime, timedelta
import random

if __name__ == "__main__":
    end = datetime.now()
    start = end - timedelta(weeks=1)

    current_time = end

    while current_time > start:
        gasses = {1: random.randint (0, 2000), 2: random.randint (0, 2000), 3: random.randint (0, 2000)}
        md.insert_gasses (gasses, current_time)

        current_time -= timedelta(minutes=1)