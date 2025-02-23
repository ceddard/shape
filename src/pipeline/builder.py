import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer, StandardScaler

class PipelineContext:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_pipeline(self) -> Pipeline:
        with open(self.file_path, 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        
        pipeline_spec = json.loads(str_json)
        steps = pipeline_spec["steps"]
        
        pipeline_steps = []
        
        if "reduce_dim" in steps:
            pipeline_steps.append(('reduce_dim', PolynomialFeatures(**steps["reduce_dim"]["PolynomialFeatures"])))
        
        if "qtransf" in steps:
            if "n_quantiles" in steps["qtransf"]["QuantileTransformer"]:
                n_quantiles = min(steps["qtransf"]["QuantileTransformer"]["n_quantiles"], 295)
                pipeline_steps.append(('qtransf', QuantileTransformer(n_quantiles=n_quantiles, **steps["qtransf"]["QuantileTransformer"])))
            else:
                pipeline_steps.append(('qtransf', QuantileTransformer(**steps["qtransf"]["QuantileTransformer"])))
        
        if "poly_feature" in steps:
            pipeline_steps.append(('poly_feature', PolynomialFeatures(**steps["poly_feature"]["PolynomialFeatures"])))
        
        if "stdscaler" in steps:
            pipeline_steps.append(('stdscaler', StandardScaler(**steps["stdscaler"]["StandardScaler"])))
        
        return Pipeline(pipeline_steps)
