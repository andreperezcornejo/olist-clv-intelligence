from fastapi import FastAPI, HTTPException
import pandas as pd
import dill

app = FastAPI(
    title="Olist Customer Intelligence API",
    description="Predictive API for Customer Lifetime Value and Retention Metrics",
    version="1.0.0"
)

# Variables globales para persistencia
models = {}
db = None

@app.on_event("startup")
async def startup_event():
    """Carga de modelos y base de datos al iniciar el servidor."""
    global db, models
    try:
        # Cargamos el modelo BG/NBD serializado
        with open('bgf_model.pkl', 'rb') as f:
            models['bgf'] = dill.load(f)
        
        # Cargamos el feature store (CSV generado en el notebook)
        db = pd.read_csv('olist_rfm_summary.csv', index_col='customer_id')
        print("INFO: Service artifacts loaded successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to initialize service: {e}")

@app.get("/api/v1/predict/{customer_id}")
async def get_customer_prediction(customer_id: str):
    """
    Entrega el CLV y la probabilidad de retención de un cliente específico.
    """
    target_id = customer_id.strip()

    if db is None or target_id not in db.index:
        raise HTTPException(
            status_code=404, 
            detail=f"Customer ID '{target_id}' not found in the database."
        )

    try:
        customer_data = db.loc[target_id]
        
        # Lógica de Negocio: Normalización de valores y estética de texto
        clv_final = max(0.0, float(customer_data['clv_12m']))
        purchases_final = max(0.0, float(customer_data.get('predicted_purchases_30d', 0)))
        
        return {
            "metadata": {
                "customer_id": target_id,
                "location": {
                    "state": str(customer_data['state']).upper(),
                    "city": str(customer_data['city']).title()
                }
            },
            "predictions": {
                "clv_12m": round(clv_final, 2),
                "prob_alive": round(float(customer_data['prob_alive']), 4),
                "expected_purchases_30d": round(purchases_final, 2)
            }
        }
    except Exception as e:
        print(f"Error en predicción para {target_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

# Bloque para ejecutar la API directamente con: python nombre_del_archivo.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)