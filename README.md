# times-text-exploration

## Prerequisites

- Python 3.8 or above.

## How to use our program

1. Run `pip install -r requirements.txt`.
2. Unzip the LA times dataset to the `dataset` folder. The path of the first file should look like (relatively to the Git root): `dataset/010189`.
3. Run the script `a_fixfiles.py`. It will duplicate the files. Please do not run it twice. If you did so, please remove all files which end by `.xml.xml`.
4. You can now run scripts from the `src` folder. Please look at the command-line arguments for details.

## Scripts

- `main_build_and_save_if.py`: generates an Inverted File. By default it is in-memory only.
- `main_requests.py`: performs requests on an on-disk Inverted File. Beware of some detail when using several terms in your request.
- `tool_test_score_coef.py`: performs some simple tests and analysis. It is not very user-friendly.
