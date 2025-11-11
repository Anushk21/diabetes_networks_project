# Basic import tests to verify environment and files
def test_imports():
    import flask, pandas, numpy, sklearn, joblib
    assert True

def test_files_exist():
    import os
    assert os.path.exists("data/diabetes_sample.csv")
