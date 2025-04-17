
import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import tempfile

st.title("Gerador de PDF de Ultrassonografia")
st.write("Faça upload de até 40 imagens de ultrassom (.jpg ou .png). Elas serão organizadas automaticamente, 8 por página, em um PDF final.")

uploaded_files = st.file_uploader("Upload das imagens", type=["jpg", "png"], accept_multiple_files=True)

if uploaded_files:
    temp_dir = tempfile.mkdtemp()
    image_paths = []
    
    for uploaded_file in uploaded_files:
        image_path = os.path.join(temp_dir, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        image_paths.append(image_path)

    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=10)
            self.add_page()

        def add_images(self, image_paths):
            images_per_page = 8
            positions = [(x, y) for y in [10, 80, 150, 220] for x in [10, 110]]
            for idx, img_path in enumerate(image_paths):
                if idx % images_per_page == 0 and idx != 0:
                    self.add_page()
                pos = positions[idx % images_per_page]
                self.image(img_path, x=pos[0], y=pos[1], w=90, h=60)

    pdf = PDF()
    pdf.add_images(image_paths)

    output_path = os.path.join(temp_dir, "relatorio-ultrassom.pdf")
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        st.download_button("Baixar PDF", f, file_name="relatorio-ultrassom.pdf")
