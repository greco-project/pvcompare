import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pvcompare",
    version="0.0.4dev",
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
            os.path.join("perosi", "*.exe"),
            os.path.join("perosi", "*.dat"),
            os.path.join("perosi", "Solar", "*.dat"),
            os.path.join("perosi", "Albedo", "*.dat"),
            os.path.join("perosi", "data", "CHEN_2020_EQE_curve_pero_corrected.csv"),
            os.path.join("perosi", "data", "CHEN_2020_EQE_curve_si_corrected.csv"),
        ]
    },
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    zip_safe=False,  # todo
    python_requires=">=3.5, <4",
    install_requires=[
        "pvlib",
        "demandlib",
        "feedinlib == v0.1.0rc2",
        "numpy >= 1.12.0,  < 1.17",
        "pandas >= 0.18.1, < 0.25",
        "oemof.thermal >= 0.0.3",
        "scipy",
        "maya~=0.6.1",
        "workalendar < 7.0.0",
        "multi_vector_simulator==0.5.5",
        "cpvlib @ git+https://github.com/isi-ies-group/cpvlib.git@2020-11#egg=cpvlib-0",
        "mock>=3.0.5",
        "plotly==4.14.2",
        "seaborn",
        "Pyomo==5.7.2",
        "psutil>=5.7.0",  # package for MVS plots
        "kaleido>=0.0.2",  # package for MVS plots
    ],
    extras_require={
        "dev": ["pytest==5.3.5", "black==19.10b0", "coverage", "coveralls",],
        "docs": ["sphinx_rtd_theme", "Sphinx>=1.4.3"],
    },
)
