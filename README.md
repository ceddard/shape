# Shape's Hard Skill Test - Machine Learning Engineer

## Project Description

This project is a solution for Shape's technical skill challenge for Machine Learning Engineers. The goal is to refactor the script `job_test_challenge.py` into a more modular codebase, implementing best practices, comprehensive documentation, and preparing it for a production release. The solution is designed to handle large data volumes, such as gigabyte-sized tables in a data lake.

## Project Structure

The project is organized as follows:
```
shape/
├── artifacts/
│   ├── model.pkl
│   └── pipeline.jsonc
├── data/
│   └── dataset.parquet
├── logs/
│   └── metrics.json
├── src/
│   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── json.py
│   │   └── postgres.py
│   ├── engine/
│   │   ├── __init__.py
│   │   └── spark_engine.py
│   ├── exceptions.py
│   ├── loader/
│   │   ├── __init__.py
│   │   └── load.py
│   ├── logger/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── schema.py
│   ├── main.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   ├── pipeline.py
│   │   ├── steps/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py
│   │   │   ├── sklearn.py
│   │   │   └── sparkml.py (unfinished)
│   │   └── strategies/
│   │       ├── __init__.py
│   │       ├── schemas.py
│   │       ├── sklearn_pipeline.py
│   │       └── sparkml_pipeline.py
│   ├── settings.py
│   ├── traceability/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── dvc.py
│   │   │   ├── mlflow.py
│   │   │   ├── weights_biases.py
│   │   └── traceability_creator.py
│   │   └── traceability_recorder.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py (unfinished)
├── .gitignore
├── CHALLENGE.md
├── LICENSE
├── Pipfile
└── setup.py
```

## Environment Setup

### Requirements

- Python 3.13
- Pipenv

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/shape.git
   cd shape
   ```

2. Install the dependencies:

   ```sh
   pipenv install
   pipenv install --dev
   ```

3. Activate the virtual environment:

   ```sh
   pipenv shell
   ```

## Usage

### Running the Pipeline

To run the pipeline, execute the command:

```sh
python src/main.py
```

### Code Structure Overview

- **main.py**: The main entry point of the project.
- **pipeline**: Contains the pipeline logic, including strategies and steps.
- **traceability**: Implements traceability using various services such as MLflow.
- **logger**: Implements logging using Kafka.
- **database**: Contains logic for saving data to PostgreSQL and JSON files.
- **engine**: Configures Spark for large-scale data processing.
- **loader**: Loads the data and the model.
- **utils.py**: Contains utility functions.

## Detailed Explanation

### main.py Structure

The `main.py` file is the main entry point for the application. Its responsibilities include:

- **Logger Configuration**: Sets up the logger to capture information during pipeline execution.
- **Spark Initialization**: Uses the `SparkEngine` class to obtain a Spark session for large-scale data processing.
- **Data Loading**: Uses the `DataLoader` class to load data from the `dataset.parquet` file.
- **Pipeline Creation**: Uses the `PipelineBuilder` class to construct the data processing and machine learning pipeline.
- **Pipeline Execution**: Fits the model to the loaded data and generates predictions using the pipeline.
- **Model and Prediction Saving**: Uses `DataLoader` to save the trained model and predictions to files.
- **Traceability Creation**: Uses the `TraceabilityCreator` class to create traceability records for the model, data, and predictions.
  
The `main` function is invoked when the script is run directly. Future enhancements may allow triggering the execution through a custom pipeline template (e.g., via a YAML configuration), controlled by Jenkins, Airflow, or a scheduled job.

### Pipeline Logic

The `pipeline` component contains the core business logic:

1. **pipeline.py**:
   - Defines the `PipelineHandler` class, responsible for data loading, pipeline creation, and data transformation.
   - Uses the `Load` class to load data and models.
   - Uses the `PipelineBuilder` to assemble the pipeline based on the provided specifications.
   - Processes data, applies transformations, and generates predictions while also calculating relevant metrics.

2. **builder.py**:
   - Defines the `PipelineBuilder` class that reads pipeline specifications from a JSON file and creates a pipeline strategy 
   (either `SklearnPipelineStrategy` or `SparkMLPipelineStrategy`) based on the specified framework (scikit-learn or SparkML).

3. **strategies/**:
   - Contains pipeline strategies for different frameworks.
   - **schemas.py**: Defines the abstract `PipelineStrategy` class as the base for all pipeline strategies.
   - **sklearn_pipeline.py**: Implements the pipeline strategy for scikit-learn.
   - **sparkml_pipeline.py**: Implements the pipeline strategy for SparkML (unfinished due to deadline constraints).

4. **steps/**:
   - Contains pipeline steps for different frameworks.
   - **schemas.py**: Defines the abstract `StepStrategy` class as the base for individual pipeline step implementations.
   - **sklearn.py**: Implements scikit-learn pipeline steps such as `ReduceDimStrategy`, `QTransfStrategy`, `PolyFeatureStrategy`, and `StdScalerStrategy`.
   - **sparkml.py**: Implements SparkML pipeline steps such as `ReduceDimStrategy`, `QTransfStrategy`, `PolyFeatureStrategy`, and `StdScalerStrategy`.

These components work together to create a scalable data processing and machine learning pipeline that can be configured using various strategies for different frameworks.

## Technologies Used

- **Python 3.13**: The main programming language.
- **Pandas**: Data manipulation and analysis library.
- **NumPy**: Numeric computation library.
  
  Note: Both Pandas and NumPy have limited scalability for big data scenarios. Alternatives like DASK might be more suitable for large-scale data processing.
  
- **MLflow**: Platform to manage the machine learning lifecycle.
- **PySpark**: Python interface for Apache Spark.
- **Scikit-learn**: Machine learning library (with potential future integration of SparkML).
- **Kafka**: Distributed messaging system used for logging.
- **PostgreSQL**: Relational database.
- **Pipenv**: Virtual environment and dependency management.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Contact

Carlos Eduardo Soares - [cadu_gold@hotmail.com](mailto:cadu_gold@hotmail.com)

Project Link: [https://github.com/ceddard/shape/tree/main](https://github.com/ceddard/shape/tree/main)