import ba, _ba
import os
import json
import datetime
import threading


# Path to the stats file
base_path = os.path.join(_ba.env()['python_directory_user'], "stats" + os.sep)
statsfile = base_path + 'stats.json'
seasonStartDate = None

def get_season_start_date():
    global seasonStartDate
    
    # Check if the stats file exists
    if os.path.exists(statsfile):
        with open(statsfile, 'r', encoding='utf8') as f:
            try:
                jsonData = json.loads(f.read())
            except:
                f = open(statsfile + ".backup", encoding='utf-8')
                jsonData = json.load(f)
            try:
                stats = jsonData["stats"]
                seasonStartDate = datetime.datetime.strptime(
                    jsonData["startDate"], "%d-%m-%Y %H:%M:%S")
                return seasonStartDate
            except KeyError:
                print("Error: 'startDate' or 'stats' not found in JSON data.")
    else:
        print(f"Error: Stats file '{statsfile}' not found.")

def until_season_start():
    global seasonStartDate  # Ensure we are using the global variable
    
    seasonStartDate = get_season_start_date()
    
    if seasonStartDate:        
        time_until_start = seasonStartDate - datetime.datetime.now()
        remaining_days = _ba.season_ends_in_days
        remaining_seconds = time_until_start.seconds
        remaining_hours = remaining_seconds // 3600
        remaining_minutes = (remaining_seconds % 3600) // 60
        remaining_seconds = remaining_seconds % 60        
        # Determine the appropriate time units to display
        if remaining_days > 0:
            if remaining_days > 1:
                days_str = "days"
            else:
                days_str = "day"
            time_str = f"Season ends in {remaining_days} {days_str}."
            time_str += f" {remaining_hours:02}:{remaining_minutes:02}:{remaining_seconds:02}"
        elif remaining_hours > 0:
            if remaining_hours > 1:
                hours_str = "hours"
            else:
                hours_str = "hour"
            time_str = f"Season ends in {remaining_hours} {hours_str}."
            time_str += f" {remaining_minutes:02}:{remaining_seconds:02}"
        elif remaining_minutes > 0:
            if remaining_minutes > 1:
                minutes_str = "minutes"
            else:
                minutes_str = "minute"
            time_str = f"Season ends in {remaining_minutes} {minutes_str}. {remaining_seconds:02}"
        else:
            if remaining_seconds > 1:
                seconds_str = "seconds"
            else:
                seconds_str = "second"
            time_str = f"Season ends in {remaining_seconds} {seconds_str}."
        # Display the results
        return time_str
    else:
        return "Season end date is not available."


def update_season_info():
    def _update():
        time_str = until_season_start()
        ba.Timer(1, _update)
        return time_str
    
    return _update

