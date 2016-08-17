import pytest

from bokeh.models import FuncTickFormatter, Slider

flexx = pytest.importorskip("flexx")

def test_functickformatter_from_py_func_no_args():

    def convert_to_minutes():
        return tick * 60 # noqa

    formatter = FuncTickFormatter.from_py_func(convert_to_minutes)
    js_code = flexx.pyscript.py2js(convert_to_minutes, 'formatter')

    function_wrapper = formatter.code.replace(js_code, '')

    assert function_wrapper == "formatter();\n"

def test_functickformatter_from_py_func_with_args():

    slider = Slider()

    def convert_to_minutes(x=slider):
        return tick * 60 # noqa

    formatter = FuncTickFormatter.from_py_func(convert_to_minutes)
    js_code = flexx.pyscript.py2js(convert_to_minutes, 'formatter')

    function_wrapper = formatter.code.replace(js_code, '')

    assert function_wrapper == "formatter(x);\n"
    assert formatter.args['x'] is slider

def test_functickformatter_bad_pyfunc_formats():
    def has_positional_arg(x):
        return None
    with pytest.raises(ValueError):
        FuncTickFormatter.from_py_func(has_positional_arg)

    def has_positional_arg_with_kwargs(y, x=5):
        return None
    with pytest.raises(ValueError):
        FuncTickFormatter.from_py_func(has_positional_arg_with_kwargs)

    def has_non_Model_keyword_argument(x=10):
        return None
    with pytest.raises(ValueError):
        FuncTickFormatter.from_py_func(has_non_Model_keyword_argument)

def test_functickformatter_from_coffeescript_no_arg():
    code = "square = (x) -> x * x; return square(tick)"
    formatter = FuncTickFormatter.from_coffeescript(code=code)
    assert formatter.args == {}
    assert formatter.code == ""
