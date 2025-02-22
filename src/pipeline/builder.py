import json
from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer, StandardScaler
from sklearn.pipeline import Pipeline

def pipeline_builder(file_path: str) -> Pipeline:
    with open(file_path, 'r') as f:
        str_json = '\n'.join(f.readlines()[3:])
    
    pipeline_spec = json.loads(str_json)
    steps = pipeline_spec["steps"]

    pipeline_steps = []
    
    if "reduce_dim" in steps:
        pipeline_steps.append(('reduce_dim', PolynomialFeatures(**steps["reduce_dim"]["PolynomialFeatures"])))
    
    if "qtransf" in steps:
        pipeline_steps.append(('qtransf', QuantileTransformer(**steps["qtransf"]["QuantileTransformer"])))
    
    if "poly_feature" in steps:
        pipeline_steps.append(('poly_feature', PolynomialFeatures(**steps["poly_feature"]["PolynomialFeatures"])))
    
    if "stdscaler" in steps:
        pipeline_steps.append(('stdscaler', StandardScaler(**steps["stdscaler"]["StandardScaler"])))
    
    return Pipeline(pipeline_steps)
