# VR Motion Analysis System (Python)

A Python virtual reality prototype that captures and analyses fencing
movements using **HTC Vive controllers** and **OpenVR**.

The project was developed as part of a final-year Computer Science
dissertation investigating whether consumer virtual reality hardware
could be repurposed to provide movement analysis and technique feedback
for weapons-based sports and martial arts.

------------------------------------------------------------------------

## Overview

The prototype records six degrees of freedom (6DoF) positional and
rotational data from two HTC Vive controllers during a fencing lunge,
compares a user's movement against an expert reference recording
(`ProData.csv`), and reports the average positional and rotational
differences.

The GUI demonstrates how the system could be extended to support
additional sports and techniques.

------------------------------------------------------------------------

## Features

-   Capture 6DoF motion data from two HTC Vive controllers.
-   Record expert reference movements.
-   Record user movements.
-   Store movement data as CSV files.
-   Compare user movements against expert data.
-   Interactive Tkinter GUI.
-   Modular project architecture.

------------------------------------------------------------------------

## Motion Capture Workflow

``` text
Expert Movement
      │
      ▼
4_ProDataRecorder.py
      │
      ▼
sample_data/ProData.csv

User Movement
      │
      ▼
6_ArtefactFinalVersion.py
      │
      ▼
data/UserData.csv
      │
      ▼
DataComparator.py
      │
      ▼
Movement Feedback
```

------------------------------------------------------------------------

## Development Evolution

  ---------------------------------------------------------------------------------
  Stage                File                          Purpose
  -------------------- ----------------------------- ------------------------------
  Hardware Testing     `controller_test.py`          Test Vive controller
                                                     communication

  Expert Recording     `4_ProDataRecorder.py`        Record expert movement

  Comparison Prototype `DataComparator.py`           Develop comparison algorithm

  Increment 1          `5_UserDataAnalysis.py`       Record and compare user data

  GUI Prototype        `Gui.py`                      Standalone interface

  Final Artefact       `6_ArtefactFinalVersion.py`   Integrated GUI, recording and
                                                     analysis
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

## Repository Improvements

Following completion of the dissertation, the repository has been
refactored to improve maintainability.

### Improvements made

-   Organised the repository into `src`, `tests`, `sample_data`, `data`
    and `docs`.
-   Replaced hard-coded CSV paths with `pathlib`.
-   Separated generated recordings from reference datasets.
-   Added `.gitkeep` for generated data.
-   Added `requirements.txt`.
-   Improved project documentation.

------------------------------------------------------------------------

## Current Limitations

-   Feedback is displayed in the terminal rather than inside the GUI.
-   Only the fencing lunge has a complete expert dataset.
-   Comparison uses a single expert recording.
-   No overall similarity score is calculated.

------------------------------------------------------------------------

## Future Improvements

-   Display feedback directly inside the GUI.
-   Calculate an overall similarity percentage.
-   Add technique-specific datasets.
-   Introduce Dynamic Time Warping for movement alignment.
-   Generate natural-language coaching feedback.
-   Visualise trajectories and movement errors.
-   Store recordings in a database instead of CSV files.

------------------------------------------------------------------------

## Author

Sean Dixon
