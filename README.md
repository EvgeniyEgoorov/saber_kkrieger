# Get game statistic
## Kkrieger

[Download](http://www.ag.ru/games/kkrieger/demos#)
and unpack the archive.

Alternative [link](http://web.archive.org/web/20110717024227/http://www.theprodukkt.com/kkrieger#20).

In case of problems with launching the application, set the compatibility mode with Windows XP (Service Pack 2), DX9 is required.


## FRAPS
It's an universal Windows application that can be used for FPS measuring. [Download](https://fraps.com/download.php) and install.

- [x] Choose FPS at Benchmark Settings


## Scenario

- kkrieger launch
- Taking a screenshot of how the game loaded onto the stage
- Start removing statistics
- Moving the character forward to the first obstacle / moving forward (optional, but will be an advantage)
- Stop removing statistics
- Taking a screenshot, at the end of the test
- Closing kkrieger
- Saving the result to the selected folder
- Recording in a separate file the average number of FPS per session


## Requirements
```
pipenv install
```

## Config
- Set absolute path to FRAPS directory 
- Set absolute path to benchmark folder
- If you have chaged the Benchmarking Hotkey, change it as well in config.ini (f11 by default)


## Run Script
```
pipenv run python <script>.py <path\to\kkrieger> [-o <path\to\output>]
```