# bosch-automation
This project was created as part of the interview process for the Rober Bosch company.

The task of this project was to automate the most common scenario in the demo version of their mobile android application
which is used for finding charging stations for electric vehicles.

The scenario is:
- Try wrong login into the application, check that error message is shown and back to the login page.
- Successful login into the app.
- With scrolling and tapping actions into the map find the charging station and validate format of the ID of the found station. 
This was a really challenging because it required calculating the position of the map within the application based on screen coordinates. Additionally, it was necessary to create an algorithm that would use touch to navigate to the calculated coordinates and search for a station on the map. If the map was not found, the algorithm had to swipe to the right and continue searching for the station until it was found.

The project was developed using:

**Python 3.9** programming language,
**Appium** and **Pytest** frameworks.

Instructions for running the tests:

1. Make sure that android studio, appium and appium server are installed properly.

2. Open cmd and install everything from requirements.txt in venv\Scripts with command pip install -r requirements.txt.

3. Connect device or start emulator and edit desire capabilities according that in the
conftest.py file in the project.

4. Install .apk which is located in the resources folder of this project on the device or emulator.

5. Start appium server.

6. Make sure that pytest is default test runner in pycharm.

7. Right click on the test_login_and_find_station.py in tests package and run it.
