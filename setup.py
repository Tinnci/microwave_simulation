from setuptools import setup, find_packages
from setuptools_rust import Binding, RustExtension

setup(
    name="microwave_gui",
    version="0.1.0",
    description="微波阻抗匹配设计工具",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    rust_extensions=[
        RustExtension(
            "microwave_gui",
            path="gui_rust/Cargo.toml",
            binding=Binding.PyO3
        )
    ],
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "matplotlib>=3.7.0",
        "scikit-rf>=0.29.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "pylint>=3.0.0",
            "pytest-cov>=4.1.0",
        ]
    },
    python_requires=">=3.12",
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Rust",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)