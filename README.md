# European Soccer Match Prediction Pipeline with Database API and XGBoost
## Overview
- Ingests European soccer database from Kagglehub API.
- Probes data structure and integrity with validation checks, metadata viewing, and exploratory data analysis (EDA).
- Uses joins and feature engineering/aggregation to prepare compact, useful, and interpretable features for modeling.
- Preprocesses data, trains and tunes XGBoost, and achieves above-baseline accuracy on unseen data with balanced overall performance.
- Visualizes and interprets sample decision trees, demonstrating model and feature quality.

This project provides a versatile, re-usable, and educational template for well-rounded data science and engineering workflows incorporating API ingestion, SQL and Python integration, data preprocessing, and model tuning and benchmarking.

## Components, Structure, and Results
### Supplementary Files
- `config.py`: Centralized variables and configuration elements for imports, used to ensure stability and portability across notebooks and operating systems.
- `utils.py`: Modular helper functions pulled into separate script to maintain streamlined workflows in the notebooks.
- `pyproject.toml` & `uv.lock`: Files associated with use of uv dependency manager.
- `__init__.py`: Enables importing variables and functions from its directory (including utils and config)

### Data
This project uses Kaggle's European Soccer Database ("hugomathien/soccer"), a popular choice for EDA, data engineering, and machine learning projects. The relational database contains the tables Country, League, Player, Player Attributes, Team Attributes, and Match, including over 25,000 real match records and team and player attributes sourced from FIFA.

### Model
The model used is the XGBoost Classifier with parameters max_depth = 5, learning_rate = 0.05, and gamma = 5. XGBoost was chosen for its predictive power, resilience to noise and outliers, ability to handle real-world feature interactions, algorithmic advantages over random forests, and clear interpretability. In combination with balanced class weights to promote draw detection (minority class), the grid-search-optimized parameters contribute to an ideal balance of overall performance (recall, precision, and accuracy across classes) while limiting overfitting and maintaining meaningful feature splits and generalizability.

### Match Prediction Results and Interpretation
0: Draw. 1: Home win. 2: Away win.

```
Train:
               precision    recall  f1-score   support

           0       0.33      0.36      0.35      3140
           1       0.65      0.57      0.60      5716
           2       0.49      0.56      0.52      3559

    accuracy                           0.51     12415
   macro avg       0.49      0.49      0.49     12415
weighted avg       0.52      0.51      0.52     12415

Test:
               precision    recall  f1-score   support

           0       0.28      0.32      0.30      1035
           1       0.61      0.54      0.57      1845
           2       0.47      0.49      0.48      1259

    accuracy                           0.47      4139
   macro avg       0.46      0.45      0.45      4139
weighted avg       0.49      0.47      0.48      4139
```

The 47% overall accuracy on unseen data is a reasonable baseline result for three-way sports outcome prediction, and it exceeds the roughly 45.7% home win rate. This is a reflection of meaningful features and a slight but successful incremental increase in predictive utility, especially considering the advantages of detecting all classes (draws and away wins as well) over naive majority-class prediction.

```
Class percentage breakdown:
Outcome
H    0.456748
A    0.291047
D    0.252205
Name: count, dtype: float64
```

## Usage and Setup
  
  - Requirements
    - Python version >= 3.11
    - uv (dependency management package)
    - Kaggle account and initial authentication steps (if not done already)
  - Clone repository
    - `git clone https://github.com/gwilli95/soccer_eda_ml`
  - Kaggle authentication
    - User authentication for use of the Kagglehub package is more automatic than with the Kaggle package. However, it still requires downloading a `kaggle.json` file with authentication information and moving it into a folder called `.kaggle`, if not done already. Comprehensive instructions for authentication and setup are found in the Kagglehub documentation (see the README from https://github.com/Kaggle/kagglehub).
- Install uv if needed and sync dependencies
    - Run `pip install uv`
    - Run `uv sync`
  - Mac users:
    - When attempting to sync dependencies using uv, particularly if the repository is cloned into an iCloud folder, you may encounter a Python version error in the terminal:

    `file pyproject.toml`
    ```
    pyproject.toml: cannot open 'pyproject.toml' (No such file or directory)
    ```
  
    `uv sync`

    ```
    × No solution found when resolving dependencies for split (markers: python_full_version == '3.8.*'):
    ╰─▶ Because the requested Python version (>=3.8) does not satisfy Python>=3.9 and pandas>=2.3.1 depends on Python>=3.9, we can
        conclude that pandas>=2.3.1 cannot be used.
        And because only the following versions of pandas are available:
            pandas<=2.3.1
            pandas==2.3.2
        and your project depends on pandas>=2.3.1, we can conclude that your project's requirements are unsatisfiable.
    ```

    - This may be due to an issue where the project files appear in Finder or VS Code but are not yet fully downloaded and recognized by the terminal, causing the terminal not to recognize the Python version constraints specified in the `pyproject.toml` file. The easiest solution is to copy the full contents of the `pyproject.toml` file, delete the file, create a new file titled `pyproject.toml` in the same location, paste the contents, and save it. This creates a new local file recognized by the terminal, and running `uv sync` again should download the dependencies as intended.