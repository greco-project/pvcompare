import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pvcompare",
    version="0.0.1dev",
    description="Evaluating pv technologies in net zero energy communities.",
    url="https://github.com/greco-project/pvcompare",
    author="Reiner Lemoine Institut",
    # author_email='sabine.haas@rl-institut.de',
    license="MIT",
    packages=["pvcompare"],
    package_data={
        "pvcompare": [
            os.path.join("data", "load_profiles", "*.csv"),
            os.path.join("data", "pv", "*.csv"),
        ]
    },
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    zip_safe=False,  # todo
    python_requires=">=3.5, <4",
    install_requires=[
        "pvlib",
        "demandlib",
        "feedinlib == v0.1.0rc2",  # travis has problems with installment todo
        "numpy >= 1.12.0,  < 1.17",
        "pandas >= 0.18.1, < 0.25",
        "oemof.thermal >= 0.0.3",
        "scipy",
        "workalendar < 7.0.0",  # todo check if needed. Problems with installing skyfield in travis tests (from workalendar 7.0.0)
        'greco_technologies @ git+https://github.com/greco-project/greco_technologies.git@dev',
        'cpvlib @ git+https://github.com/isi-ies-group/cpvlib.git',
        'mvs_eland @ git+https://github.com/rl-institut/mvs_eland.git@dev',
    ],
    extras_require={"dev": ["pytest"]},
)
