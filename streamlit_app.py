#Input the relevant libraries
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Define the Streamlit app
def app():
    # Display the DataFrame with formatting
    st.title("Generate Dataset with Features and Classes")
    st.write(
        """This app generates  dataset with balanced classes 
        and informative features to facilitate exploration and analysis."""
        )

    if st.button('Start'):
        # Data generation with balanced classes and informative features
        np.random.seed(42)  # For reproducibility
        num_samples = 100
        feature1 = np.random.normal(5, 2, size=num_samples)
        feature2 = np.random.normal(7, 3, size=num_samples)

        # Create informative classes based on features
        threshold = 8
        classes = (feature1 + 2 * feature2) > threshold
        labels = ['Class A' if label else 'Class B' for label in classes]

        # Combine features and labels into a DataFrame
        data = pd.DataFrame({
            'Feature 1': feature1,
            'Feature 2': feature2,
            'Class': labels,
        })

        st.dataframe(data.style.set_properties(
            caption="Dataset Preview",
            align="center",
            index_label="#",
        ))

        df = pd.DataFrame(data)

        # Create a histogram of class frequencies
        st.header("Class Distribution")
        class_counts = df["class"].value_counts().sort_index(ascending=False)
        st.bar_chart(class_counts)

        # Optionally, create a scatter plot if features are available
        if "feature1" in df.columns and "feature2" in df.columns:
            st.header("Scatter Plot by Class")
            colors = st.color_picker("Choose class colors", ["#ff0000", "#00ff00", "#0000ff"])
            for i, class_name in enumerate(class_counts.index):
                df_class = df[df["class"] == class_name]
                st.scatter(df_class["feature1"], df_class["feature2"], label=class_name, color=colors[i])
            st.legend()

        # Display other informative elements
        st.header("Data Information")
        st.write(df.describe())  # Include data summary

        # Add interactivity and customization options based on user feedback
        st.sidebar.header("Customization")
        if st.sidebar.checkbox("Include data summary?"):
            st.write(df.describe())
        if st.sidebar.checkbox("Enable feature scatter plot?"):
            st.header("Scatter Plot by Class")
            colors = st.sidebar.color_picker("Choose class colors", ["#ff0000", "#00ff00", "#0000ff"])
            for i, class_name in enumerate(class_counts.index):
                df_class = df[df["class"] == class_name]
                st.scatter(df_class["feature1"], df_class["feature2"], label=class_name, color=colors[i])
            st.legend()

        # Add download button with enhanced error handling and feedback
        csv_file = BytesIO()
        data.to_csv(csv_file, index=False)
        csv_file.seek(0)

        download_button = st.download_button(
            label="Download CSV",
            data=csv_file,
            file_name="dataset.csv",
            mime="text/csv",
            on_click=None,  # Disable immediate download on page load
        )

        if download_button:
            try:
                st.success("Download successful!")
            except Exception as e:
                st.error(f"Download failed: {e}")

        st.write("You can now explore and analyze this dataset for various purposes.")
    
#run the app
if __name__ == "__main__":
    app()
