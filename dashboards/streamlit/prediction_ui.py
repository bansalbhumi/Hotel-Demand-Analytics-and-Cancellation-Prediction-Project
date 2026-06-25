import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
import os
import sys

# Add src to path to import CancellationPredictor
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.inference import CancellationPredictor

@st.cache_resource
def load_predictor():
    return CancellationPredictor()

def render_prediction_page():
    st.header("Cancellation Risk Prediction")
    st.markdown("Enter booking details to predict the likelihood of cancellation and understand the key driving factors.")
    
    predictor = load_predictor()
    
    with st.form("prediction_form"):
        st.subheader("Booking Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            deposit_type = st.selectbox("Deposit Type", ["No Deposit", "Non Refund", "Refundable"])
            country = st.text_input("Country (e.g., PRT, GBR, FRA)", value="PRT")
            market_segment = st.selectbox("Market Segment", ["Online TA", "Offline TA/TO", "Groups", "Direct", "Corporate", "Aviation", "Complementary"])
            customer_type = st.selectbox("Customer Type", ["Transient", "Transient-Party", "Contract", "Group"])
            
        with col2:
            lead_time = st.number_input("Lead Time (days)", min_value=0, max_value=700, value=50)
            
            # Determine lead_time_bucket
            if lead_time <= 30:
                lead_time_bucket = "0-30"
            elif lead_time <= 90:
                lead_time_bucket = "31-90"
            elif lead_time <= 180:
                lead_time_bucket = "91-180"
            else:
                lead_time_bucket = "181-400" # simplification
                
            season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Autumn"])
            total_special_requests = st.number_input("Total Special Requests", min_value=0, max_value=5, value=0)
            previous_cancellations = st.number_input("Previous Cancellations", min_value=0, max_value=30, value=0)
            
        with col3:
            total_nights = st.number_input("Total Nights", min_value=1, max_value=30, value=3)
            total_guests = st.number_input("Total Guests", min_value=1, max_value=20, value=2)
            
            prior_cancel_flag = 1 if previous_cancellations > 0 else 0
            
        submit_button = st.form_submit_button(label="Predict Cancellation Risk")
        
    if submit_button:
        input_data = pd.DataFrame([{
            'deposit_type': deposit_type,
            'country': country,
            'market_segment': market_segment,
            'customer_type': customer_type,
            'lead_time_bucket': lead_time_bucket,
            'season': season,
            'lead_time': lead_time,
            'total_of_special_requests': total_special_requests,
            'previous_cancellations': previous_cancellations,
            'total_nights': total_nights,
            'total_guests': total_guests,
            'prior_cancel_flag': prior_cancel_flag
        }])
        
        # Make prediction
        prob = predictor.predict_proba(input_data)[0]
        
        st.divider()
        st.subheader("Prediction Results")
        
        prob_pct = prob * 100
        # Clamp between 0.1% and 99.9% to account for model uncertainty
        prob_pct = max(0.1, min(prob_pct, 99.9))
        
        if prob_pct > 60:
            st.error(f"High Risk of Cancellation: {prob_pct:.1f}%")
        elif prob_pct > 30:
            st.warning(f"Moderate Risk of Cancellation: {prob_pct:.1f}%")
        else:
            if prob_pct < 0.2:
                st.success(f"Low Risk of Cancellation: <0.1%")
            else:
                st.success(f"Low Risk of Cancellation: {prob_pct:.1f}%")
            
        # Model Explainability using SHAP
        st.subheader("Why this prediction?")
        try:
            # We need to transform the data using the pipeline's preprocessor first
            # The Random Forest is inside a pipeline, so we get the preprocessor and the classifier
            preprocessor = predictor.pipeline.named_steps['preprocessor']
            model = predictor.pipeline.named_steps['classifier']
            
            X_transformed = preprocessor.transform(input_data)
            
            # Use TreeExplainer for Random Forest
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_transformed)
            
            # For classification, shap_values might be a list (one for each class), we want class 1 (Cancellation)
            if isinstance(shap_values, list):
                sv = shap_values[1][0] # class 1, first instance
            else:
                sv = shap_values[0] # first instance
            
            # Get feature names from preprocessor
            feature_names = preprocessor.get_feature_names_out()
            
            # Create a simple matplotlib plot for feature importance
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot top 5 features
            sv_abs = [abs(val) for val in sv]
            top_indices = sorted(range(len(sv_abs)), key=lambda i: sv_abs[i], reverse=True)[:5]
            
            top_features = [feature_names[i] for i in top_indices]
            top_shap = [sv[i] for i in top_indices]
            
            colors = ['red' if val > 0 else 'green' for val in top_shap]
            
            ax.barh(top_features, top_shap, color=colors)
            ax.set_xlabel('SHAP Value (Impact on Prediction)')
            ax.set_title('Top 5 Driving Factors for this Prediction')
            
            # Add text indicating direction
            st.markdown("- **Red bars** increase the likelihood of cancellation.\n- **Green bars** decrease the likelihood.")
            st.pyplot(fig)
            
        except Exception as e:
            st.warning(f"Could not generate explanation plot. Ensure SHAP is installed properly and model supports it. Error: {str(e)}")
