from setuptools import setup, find_packages
from setuptools_rust import RustExtension

setup(
    name="microwave_simulation",
    version="0.1.0",
    packages=find_packages(),
    rust_extensions=[
        RustExtension(
            "microwave_gui",
            "gui_rust/Cargo.toml",
            debug=False,
            py_limited_api=False
        )
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "scikit-rf",
        "setuptools_rust"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "ruff",
            "mypy"
        ]
    },
    zip_safe=False,
    python_requires=">=3.8"
)