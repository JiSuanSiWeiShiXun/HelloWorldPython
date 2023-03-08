# coding=utf-8
import pathlib

if __name__ == "__main__":
    path = pathlib.Path("./assert.pyc")
    try:
        assert path.exists(), f"source file {path.name} doesn't exists"
    except AssertionError as e:
        print(type(e))