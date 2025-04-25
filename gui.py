import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
import json
import cv2
import numpy as np

from imgToOcr import imageOcrResult
from getPhotoSign import getPhotoFromImg, getSignFromImg

st.set_page_config(page_title="OCR based loan Application Processing", layout="wide")
st.title("OCR based loan data extraction")

option = st.radio("Choose upload type:", ["Upload PDF", "Upload Images"])

page1_img = page2_img = None
photo = signature = None
ocr_data = {}

# Utility: convert OpenCV image to PIL
def convert_cv_to_pil(cv_image):
    return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

# Upload logic
if option == "Upload PDF":
    pdf_file = st.file_uploader("Upload a 2-page PDF", type=["pdf"])
    if pdf_file:
        images = convert_from_bytes(pdf_file.read(), dpi=300)
        if len(images) < 2:
            st.error("PDF must have at least 2 pages.")
        else:
            page1_img, page2_img = images[0], images[1]
            ocr_data = json.loads(imageOcrResult(page1_img, page2_img))
            photo = getPhotoFromImg(page1_img)
            signature = getSignFromImg(page2_img)

elif option == "Upload Images":
    page1 = st.file_uploader("Upload Page 1 (Image)", type=["png", "jpg", "jpeg"], key="page1")
    page2 = st.file_uploader("Upload Page 2 (Image)", type=["png", "jpg", "jpeg"], key="page2")

    if page1 and page2:
        page1_img = Image.open(page1)
        page2_img = Image.open(page2)
        ocr_data = json.loads(imageOcrResult(page1_img, page2_img))
        photo = getPhotoFromImg(page1_img)
        signature = getSignFromImg(page2_img)
    elif page1 or page2:
        st.warning("Please upload both Page 1 and Page 2.")

# Form to review/edit OCR result
if ocr_data:
    st.subheader("Application Review")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", ocr_data.get("name", ""))
        salutation = st.multiselect("Salutation", ["Mr", "Mrs", "Dr.", "Other"], ocr_data.get("salutation", []))
        dob = st.text_input("Date of Birth", ocr_data.get("dob", ""))
        marital_status = st.multiselect("Marital Status", ["Single", "Married"], ocr_data.get("marital_status", []))
        father_name = st.text_input("Father/Husband Name", ocr_data.get("father_husband_name", ""))
        nationality = st.text_input("Nationality", ocr_data.get("nationality", ""))
        category = st.multiselect("Category", ["SC", "ST", "OBC", "General"], ocr_data.get("category", []))
        id_proof = st.multiselect("Identity Proof", ["AadharCard", "PANCard", "VoteridCard"], ocr_data.get("identity_proof", []))
        aadhar = st.text_input("Aadhar Number", ocr_data.get("aadhar_number", ""))
        email = st.text_input("Email (Personal)", ocr_data.get("email", ""))

        # Extra fields if needed
        pan_no = st.text_input("PAN Number", ocr_data.get("pan_number", ""))
        voter_id = st.text_input("Voter ID Number", ocr_data.get("voter_id", ""))

    with col2:
        address_type = st.multiselect("Address Type", ["Permanent", "Correspondence"], ocr_data.get("address_type", []))
        apartment_no = st.text_input("Apartment No.", ocr_data.get("apartment_no", ""))
        street_name = st.text_input("Street Name", ocr_data.get("street_name", ""))
        landmark = st.text_input("Landmark", ocr_data.get("landmark", ""))
        city = st.text_input("City", ocr_data.get("city", ""))
        district = st.text_input("District", ocr_data.get("district", ""))
        pincode = st.text_input("Pin Code", ocr_data.get("pincode", ""))
        state = st.text_input("State", ocr_data.get("state", ""))
        country = st.text_input("Country", ocr_data.get("country", ""))
        mobile_primary = st.text_input("Mobile (Primary)", ocr_data.get("mobile_primary", ""))
        mobile_secondary = st.text_input("Mobile (Secondary)", ocr_data.get("mobile_secondary", ""))

    st.subheader("💼 Loan Details")
    loan_purpose = st.multiselect("Loan Purpose", ["Education", "Marriage", "Medical", "Other"], ocr_data.get("loan_purpose", []))
    processing_fee = st.number_input("Processing Fee", value=ocr_data.get("processing_fee", 0))
    concession = st.number_input("Concession", value=ocr_data.get("concession", 0))
    place = st.text_input("Place", ocr_data.get("place", ""))
    date = st.text_input("Application Date", ocr_data.get("date", ""))


    # Initialize session state for photo and signature
    if "photo" not in st.session_state:
        st.session_state.photo = photo
    if "signature" not in st.session_state:
        st.session_state.signature = signature

    # --------------------- PHOTO --------------------- #
    st.subheader("Photo")

    if st.session_state.photo is not None:
        st.image(convert_cv_to_pil(st.session_state.photo), caption="Photo", width=150)
        if st.button("Remove Photo"):
            st.session_state.photo = None

    if st.session_state.photo is None:
        new_photo_file = st.file_uploader("📤 Upload Photo", type=["jpg", "jpeg", "png"], key="photo_upload")
        if new_photo_file:
            st.session_state.photo = cv2.cvtColor(np.array(Image.open(new_photo_file)), cv2.COLOR_RGB2BGR)

    # --------------------- SIGNATURE --------------------- #
    st.subheader("Signature")

    if st.session_state.signature is not None:
        st.image(convert_cv_to_pil(st.session_state.signature), caption="Signature", width=150)
        if st.button("Remove Signature"):
            st.session_state.signature = None

    if st.session_state.signature is None:
        new_sign_file = st.file_uploader("📤 Upload Signature", type=["jpg", "jpeg", "png"], key="sign_upload")
        if new_sign_file:
            st.session_state.signature = cv2.cvtColor(np.array(Image.open(new_sign_file)), cv2.COLOR_RGB2BGR)

    # Final dictionary
    final_data = {
        "name": name,
        "salutation": salutation,
        "dob": dob,
        "marital_status": marital_status,
        "father_husband_name": father_name,
        "nationality": nationality,
        "category": category,
        "identity_proof": id_proof,
        "aadhar_number": aadhar,
        "pan_number": pan_no,
        "voter_id": voter_id,
        "address_type": address_type,
        "apartment_no": apartment_no,
        "street_name": street_name,
        "landmark": landmark,
        "city": city,
        "district": district,
        "pincode": pincode,
        "state": state,
        "country": country,
        "mobile_primary": mobile_primary,
        "mobile_secondary": mobile_secondary,
        "email": email,
        "loan_purpose": loan_purpose,
        "processing_fee": processing_fee,
        "concession": concession,
        "place": place,
        "date": date,
        "has_photo": photo is not None,
        "has_signature": signature is not None
    }
    
    checkbox = st.checkbox('I have carefully reviewed the application and all data is correct.')
    
    if checkbox:
        if st.button("Confirm and Submit Application"):
            st.success("Application Submitted Successfully!")

            st.json(final_data)

    else:
         st.warning('Please confirm that you have reviewed the application data before submitting.')
