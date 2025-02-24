from setuptools import setup, find_packages

setup(
    name="shape-MLE-case",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "psycopg2",
        "kafka-python",
        "mlflow",
        "pyspark",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
        ],
    },
    entry_points={
        "console_scripts": [
            "shape=main:score",
        ],
    },
    include_package_data=True,
    author="Carlos Eduardo Soares",
    author_email="cadu_gold@hotmail.com",
    description="A project for shape analysis and processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shape",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="shape analysis processing machine learning",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/shape/issues",
        "Documentation": "https://github.com/yourusername/shape/wiki",
        "Source Code": "https://github.com/yourusername/shape",
    },
    python_requires=">=3.11",
)