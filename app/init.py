# Don't edit
__author__ = "Joseph Anderson"
__copyright__ = "Copyright 2023"
__license__ = "INTERNAL"
__version__ = "0.0.1"
__maintainer__ = __author__
__email__ = "ienjoycoding4u@gmail.com"
__status__ = "alpha"


from fastapi import FastAPI
from app.__internal import bootstrap

app = FastAPI(
    title="MVP",
    description="MVP",
    version="-".join([__version__, __status__]),
    root_path="/",
)

bootstrap(app)