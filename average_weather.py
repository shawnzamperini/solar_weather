from space_weather_tracker import SpaceWeatherTracker


print("-----------------------------------")
print("Space Weather Tracker")
print("-----------------------------------")
year, month, day = input("Date to get space weather for, " + \
                         "separated by commas (year, month, day): ").split(',')
year = int(year); month = int(month); day = int(day)

tracker = SpaceWeatherTracker(year, month, day)
try:
    tracker.get_Kp()
    print('\nKp')
    print('  Minimum: {:.2f}'.format(tracker.kp_stats['min']))
    print('  Maximum: {:.2f}'.format(tracker.kp_stats['max']))
    print('  Average: {:.2f}'.format(tracker.kp_stats['mean']))
except Exception as e:
    print("  Error: Could not get Kp.")
    print("  " + str(e))
try:
    tracker.get_pflux()
    print('\nProton Flux')
    print('  >10 MeV:  {:.2f}'.format(tracker.pflux_stats['>10 MeV']))
    print('  >50 MeV:  {:.2f}'.format(tracker.pflux_stats['>50 MeV']))
    print('  >100 MeV: {:.2f}'.format(tracker.pflux_stats['>100 MeV']))
except Exception as e:
    print("Error: Could not get proton flux.")
    print("  " + str(e))
try:
    tracker.get_xray()
    print('\nX-ray Flux')
    print('  0.5-4.0 A: {:.2}'.format(tracker.xray_stats['0.5-4.0 A']))
    print('  1.0-8.0 A: {:.2}'.format(tracker.xray_stats['1.0-8.0 A']))
except Exception as e:
    print("Error: Could not get X-ray flux.")
    print("  " + str(e))
