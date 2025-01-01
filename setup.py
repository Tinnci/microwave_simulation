from setuptools import setup
from setuptools_rust import RustExtension

setup(
    name="microwave_simulation",
    version="0.1.0",
    packages=["src"],
    rust_extensions=[RustExtension("microwave_gui", "gui_rust/Cargo.toml", debug=False)],
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy"
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
    zip_safe=False
)