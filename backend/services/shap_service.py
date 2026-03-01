import io
import base64
import matplotlib.pyplot as plt
import shap

def get_shap_waterfall_plot(model, input_df):
    # 1. Generate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(input_df)

    # 2. Create the plot without showing a popup window
    plt.figure(figsize=(8, 6))
    shap.plots.waterfall(shap_values[0], show=False)
    
    # 3. Save plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close() # Clean up memory
    
    # 4. Encode to Base64
    base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{base64_str}"