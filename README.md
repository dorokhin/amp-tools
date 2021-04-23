# Python AMP Library
[![Build Status](https://travis-ci.org/dorokhin/amp-tools.svg?branch=master)](https://travis-ci.org/dorokhin/amp-tools)
[![codecov](https://codecov.io/gh/dorokhin/amp-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/dorokhin/amp-tools)
[![PyPI version](https://badge.fury.io/py/amp-tools.svg)](https://badge.fury.io/py/amp-tools)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This library contains class what converts html to AMP.

Work in progress


### Installation
```bash
pip install amp_tools
```

### Usage example
```python
from amp_tools import TransformHtmlToAmp


html_elements = '<span class="test-class">' \
                    '<form class="form-test"></form>' \ 
                    '<img src="media/test.png" width="300" height="220">' \
                '</span>'
        
valid_amp = TransformHtmlToAmp(html_elements)()

# Return 
b'<div class="amp-text"><amp-img src="media/test.png" width="300" height="220" layout="responsive"></amp-img></div>'

```

