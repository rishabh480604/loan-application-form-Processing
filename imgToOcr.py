from PIL import Image
import pytesseract
import re
import json

def extract_after_y(text, valid_options):
    text = text.lower()
    match = re.search(r'\by\b[^\w]*([\w.]+)', text)
    if match:
        word = match.group(1).strip(".").capitalize()
        if word in [opt.strip(".") for opt in valid_options]:
            return word if word != "Dr" else "Dr."  # ensure it matches "Dr." format
    return None

def sameLineData(label, ocr_text):
    # Look for the label, followed by value after the colon (":"), and trim extra spaces
    match = re.search(
        rf"{label}\s*:\s*([^\n]+)",  # Capture everything after ":" until the newline
        ocr_text,
        re.IGNORECASE
    )
    
    if match:
        return match.group(1).strip()  # Trim spaces from the extracted value
    return None


def imageOcrResult(img1, img2):
    def parse_selected_options(line, options):
        selected = []
        for option in options:
            pattern = f"Y\\s*{option}"
            if re.search(pattern, line, re.IGNORECASE):
                selected.append(option)
        return selected

    data = {}

    # Extract text from image 1 (page 1)
    ocr_text = pytesseract.image_to_string(img1)
    print(ocr_text)

    try:
        data["name"] = re.search(r"Name\s*:\s*(\w+)", ocr_text).group(1)
        
        salutation_line = re.search(r"Salutation:(.*)", ocr_text, re.IGNORECASE)
        if salutation_line:
            data["salutation"] = extract_after_y(salutation_line.group(1), ["Mr", "Mrs", "Dr.", "Other"])
        else:
            data["salutation"] = None
        
        data["dob"] = re.search(r"Date Of Birth\s*:\s*([0-9 ]+)", ocr_text).group(1).strip()
        data["marital_status"] = parse_selected_options(
            re.search(r"Martial Status:(.*)", ocr_text).group(1),
            ["Single", "Married"]
        )
        data["father_husband_name"] = re.search(r"Name of Father/Husband\s*:\s*(.+)", ocr_text).group(1)
        data["nationality"] = re.search(r"Nationality\s*:\s*(\w+)", ocr_text).group(1)
        data["category"] = parse_selected_options(
            re.search(r"Category:(.*)", ocr_text).group(1),
            ["SC", "ST", "OBC", "General"]
        )
        data["identity_proof"] = parse_selected_options(
            re.search(r"Identity Proof:(.*)", ocr_text).group(1),
            ["AadharCard", "PANCard", "VoteridCard"]
        )

        # Aadhaar Number (captures everything after 'AADHAR NO:' until 'Pin' or end of the line)
        aadhar_match = re.search(r"AADHAR\sNO\s*:\s*(.*?)(?=\s*PAN|\s*$)", ocr_text)
        data["aadhar_number"] = aadhar_match.group(1).strip() if aadhar_match else None

        # PAN Number (captures everything after 'PAN NO:' until 'Pin', 'VoteridCard', or end of the line)
        pan_match = re.search(r"PAN\sNO\s*:\s*(.*?)(?=\s*Pin|\s*VoteridCard|\s*$)", ocr_text)
        data["pan_number"] = pan_match.group(1).strip() if pan_match else None

        # Voter ID (captures everything after 'VoteridCard:' until 'Pin' or 'Address' or end of the line)
        voter_match = re.search(r"VoteridCard\s*:\s*(.*?)(?=\s*Pin|\s*Address|\s*$)", ocr_text)
        data["voter_id"] = voter_match.group(1).strip() if voter_match else None


        data["address_type"] = parse_selected_options(
            re.search(r"Address:(.*)", ocr_text).group(1),
            ["Permanent", "Correspondence"]
        )
        data["apartment_no"] = re.search(r"Apartment No\. or Name:\s*(.*)", ocr_text).group(1)
        data["street_name"] = re.search(r"Street Name or Area\s*:\s*(.*)", ocr_text).group(1)
        data["landmark"] = re.search(r"Landmark\s*:\s*(.*)", ocr_text).group(1)
        data["city"] = re.search(r"City\s*:\s*(.*?)\s*District", ocr_text).group(1).strip()
        data["district"] = re.search(r"District\s*:\s*(.*)Pin\s*Code", ocr_text).group(1).strip()
        data["pincode"] = re.search(r"Pin Code\s*:\s*(\d+)", ocr_text).group(1)
        data["state"] = re.search(r"State\s*:\s*(.*)Country", ocr_text).group(1).strip()
        data["country"] = re.search(r"Country\s*:\s*(.*)", ocr_text).group(1).strip()
        data["mobile_primary"] = re.search(r"Mobile \(Primary\):\s*([+\d]+)", ocr_text).group(1)
        data["mobile_secondary"] = re.search(r"Mobile\(Secondary\)\s*:\s*([+\d]+)", ocr_text).group(1)
        data["email"] = re.search(r"Email\(Personal\)\s*:\s*(.*)", ocr_text).group(1)
    except Exception as e:
        data["error_page1"] = str(e)

    # Extract text from image 2 (page 2)
    ocr_text2 = pytesseract.image_to_string(img2)

    try:
        loan_purpose_line = re.search(r"Loan Purpose:(.*)", ocr_text2)
        if loan_purpose_line:
            data["loan_purpose"] = parse_selected_options(loan_purpose_line.group(1), ["Education", "Marriage", "Medical", "Other"])

        fee_match = re.search(r"Processing Fee\s*:\s*(\d+)", ocr_text2)
        data["processing_fee"] = int(fee_match.group(1)) if fee_match else None

        concession_match = re.search(r"Concession\s*:\s*(\d+)", ocr_text2)
        data["concession"] = int(concession_match.group(1)) if concession_match else None

        place_match = re.search(r"Place\s*:\s*(.*)", ocr_text2)
        data["place"] = place_match.group(1).strip() if place_match else None

        date_match = re.search(r"Date\s*:\s*([0-9 ]+)", ocr_text2)
        data["date"] = date_match.group(1).strip() if date_match else None
    except Exception as e:
        data["error_page2"] = str(e)

    return json.dumps(data,indent=2)


# Display the structured output
# import json
# print(json.dumps(data, indent=2))

'''
# Print the extracted text
print("Extracted Text:")
print(extracted_text)
'''