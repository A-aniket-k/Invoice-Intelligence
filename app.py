import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from inference.ai_extractor import extract_invoice_data
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# Page Configuration
st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="🤖",
    layout="wide"
)

# Header Section
st.markdown("""
# Vendor Invoice Intelligence Portal
### AI-Driven Freight Cost Prediction & Invoice Risk Flagging
""")

st.divider()

# Sidebar Navigation
st.sidebar.title("Model Selection")
selected_model = st.sidebar.radio(
    "Choose Prediction Module",
    ["Freight Cost Prediction", "Invoice Manual Approval Flag"]
)

st.sidebar.markdown("""
**Business Impact**
- Improved cost forecasting
- Reduced invoice fraud & anomalies
- Faster finance operations
""")

# ==========================================
# ⚡ AUTOMATED INTELLIGENT PROCESSING BLOCK
# ==========================================
st.subheader("⚡ Automated Intelligent Processing")
uploaded_file = st.file_uploader("Upload an Invoice Document (PDF, PNG, JPG) or Batch Spreadsheet (CSV, XLSX)", type=["pdf", "png", "jpg", "csv", "xlsx"])

# Create standard fallback session states for single forms
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "qty": 1200, "dollars": 18500.0, "flag_qty": 50, 
        "flag_dollars": 352.95, "freight": 1.73, "item_qty": 162, "item_dollars": 2476.0
    }

if uploaded_file is not None:
    file_name = uploaded_file.name.lower()
    
    # --- BATCH SPREADSHEET PATH ---
    if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
        st.info("📊 Spreadsheet detected. Processing full batch predictions...")
        
        if file_name.endswith('.csv'):
            df_batch = pd.read_csv(uploaded_file)
        else:
            df_batch = pd.read_excel(uploaded_file)
            
        with st.spinner("Running batch machine learning models..."):
            try:
                # 1. Generate Freight Cost Predictions
                q_col = next((c for c in df_batch.columns if 'qty' in c.lower() or 'quantity' in c.lower()), 'Quantity')
                d_col = next((c for c in df_batch.columns if 'dollar' in c.lower()), 'Dollars')
                
                freight_input = {
                    "Quantity": df_batch[q_col].tolist(),
                    "Dollars": df_batch[d_col].tolist()
                }
                freight_preds = predict_freight_cost(freight_input)['Predicted_Freight']
                df_batch["Predicted_Freight_Cost"] = np.round(freight_preds, 2)
                
                # 2. Generate Manual Approval Flags
                flag_input = {
                    "invoice_quantity": df_batch.get("Quantity", df_batch.get("invoice_quantity", [0]*len(df_batch))).tolist(),
                    "invoice_dollars": df_batch.get("Invoice Dollars", df_batch.get("invoice_dollars", [0.0]*len(df_batch))).tolist(),
                    "Freight": df_batch.get("Freight Cost", df_batch.get("Freight", [0.0]*len(df_batch))).tolist(),
                    "total_item_quantity": df_batch.get("Total Item Quantity", df_batch.get("total_item_quantity", [0]*len(df_batch))).tolist(),
                    "total_item_dollars": df_batch.get("Total Item Dollars", df_batch.get("total_item_dollars", [0.0]*len(df_batch))).tolist()
                }
                flag_preds = predict_invoice_flag(flag_input)['Predicted_Flag']
                df_batch["AI_Risk_Assessment"] = ["⚠️ MANUAL APPROVAL" if f == 1 else "✅ SAFE (Auto-Approve)" for f in flag_preds]

                st.success(f"Successfully evaluated all {len(df_batch)} rows!")
                
                # Dynamically set visible columns based on chosen navigation option
                if selected_model == "Freight Cost Prediction":
                    ordered_columns = [
                        "Quantity", "Invoice Dollars", "Freight Cost", 
                        "Total Item Quantity", "Total Item Dollars", "Predicted_Freight_Cost"
                    ]
                else:  # Invoice Manual Approval Flag selected
                    ordered_columns = [
                        "Quantity", "Invoice Dollars", "Freight Cost", 
                        "Total Item Quantity", "Total Item Dollars", "Predicted_Freight_Cost", "AI_Risk_Assessment"
                    ]
                
                # Keep only valid existing columns
                final_cols = [c for c in ordered_columns if c in df_batch.columns]
                df_batch_display = df_batch[final_cols]

                # Show the dynamic clean data window
                st.dataframe(df_batch_display, use_container_width=True)
                
                # Provide full operational download containing all data metrics
                csv_output = df_batch_display.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Comprehensive Analytics Results CSV",
                    data=csv_output,
                    file_name="comprehensive_batch_predictions.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error executing batch generation: {e}. Check your spreadsheet column configurations.")
                
    # --- SINGLE DOCUMENT FILE PATH (AI VISION) ---
    else:
        with st.spinner("AI Agent is scanning document image metrics..."):
            extracted_metrics = extract_invoice_data(uploaded_file)
            if extracted_metrics:
                st.success("Single invoice text extracted successfully via AI Vision!")
                st.session_state.form_data["qty"] = int(extracted_metrics.get("invoice_quantity", 0))
                st.session_state.form_data["dollars"] = float(extracted_metrics.get("invoice_dollars", 0.0))
                st.session_state.form_data["flag_qty"] = int(extracted_metrics.get("invoice_quantity", 0))
                st.session_state.form_data["flag_dollars"] = float(extracted_metrics.get("invoice_dollars", 0.0))
                st.session_state.form_data["freight"] = float(extracted_metrics.get("Freight", 0.0))
                st.session_state.form_data["item_qty"] = int(extracted_metrics.get("total_item_quantity", 0))
                st.session_state.form_data["item_dollars"] = float(extracted_metrics.get("total_item_dollars", 0.0))

st.divider()

# Manual Input Forms below
if selected_model == "Freight Cost Prediction":
    st.subheader("Manual Override: Freight Cost Form")
    with st.form("freight_form"):
        col1, col2 = st.columns(2)
        with col1:
            quantity = st.number_input("Quantity", min_value=1, value=st.session_state.form_data["qty"])
        with col2:
            dollars = st.number_input("Invoice Dollars", min_value=1.0, value=st.session_state.form_data["dollars"])
        submit_freight = st.form_submit_button("Predict Single Freight Cost")
        
    if submit_freight:
        input_data = {"Quantity": [quantity], "Dollars": [dollars]}
        prediction = predict_freight_cost(input_data)['Predicted_Freight']
        st.metric(label="Estimated Freight Cost", value=f"${prediction[0]:,.2f}")

else:
    st.subheader("Manual Override: Invoice Manual Approval Prediction")
    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            invoice_quantity = st.number_input("Invoice Quantity", min_value=1, value=st.session_state.form_data["flag_qty"])
            freight = st.number_input("Freight Cost", min_value=0.0, value=st.session_state.form_data["freight"])
        with col2:
            invoice_dollars = st.number_input("Invoice Dollars", min_value=1.0, value=st.session_state.form_data["flag_dollars"])
            total_item_quantity = st.number_input("Total Item Quantity", min_value=1, value=st.session_state.form_data["item_qty"])
        with col3:
            total_item_dollars = st.number_input("Total Item Dollars", min_value=1.0, value=st.session_state.form_data["item_dollars"])
        submit_flag = st.form_submit_button("Evaluate Single Invoice Risk")
        
    if submit_flag:
        input_data = {
            "invoice_quantity": [invoice_quantity], "invoice_dollars": [invoice_dollars],
            "Freight": [freight], "total_item_quantity": [total_item_quantity], "total_item_dollars": [total_item_dollars]
        }
        flag_prediction = predict_invoice_flag(input_data)['Predicted_Flag']
        if bool(flag_prediction[0]):
            st.error("⚠️ Invoice requires **MANUAL APPROVAL**")
        else:
            st.success("✅ Invoice is **SAFE for Auto-Approval**")