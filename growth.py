import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title="Growth", layout="wide")

#custom css

st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

#title("Growth")
st.title("Datasweeper Starlink Integrater")
st.write("Convert your files between CSV and Excel formats")
uploaded_file = st.file_uploader("Upload your file in CSV or Excel format", type=["csv", "xlsx"], accept_multiple_files=True)

#convert file
if uploaded_file :
    for file in uploaded_file:
        file_extension = os.path.splitext(file.name)[-1].lower()
        try:
            if file_extension == ".csv":
                df = pd.read_csv(file)
            elif file_extension == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Invalid file format: {file_extension}")
                continue
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            continue

        #Display info about the file
        st.write(f"File name: {file.name}")
        st.write(f"File size: {file.size/1024} KB")

        #file details
        st.write(f"Preview the head of dataframe")
        st.write(df.head())

        #data cleaning project
        st.subheader("Data Cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicate from the {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(f"Duplicate removed")
            with col2:
                if st.button(f"Fill missing values for the {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(f"Missing values has been filled")

        st.subheader("Select the columns to convert")
        columns = st.multiselect(f"Chose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualizations for {file.name}"):
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:,:2])
            else:
                st.write("No numeric columns available for visualization")

        # Conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key={file.name})
        if st.button(f"Convert to {file.name}"):
            #Convert the file in csv format
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension,".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_extension,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #download button
            st.download_button(
                label=f"Download {file_name} as {conversion_type}", 
                data=buffer, 
                file_name=file_name, 
                mime=mime_type
            )

st.success("All files processed successfully")