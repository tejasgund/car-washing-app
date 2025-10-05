from config import database
from messenger import  send_message
def generate_bill_message(bill_no):
    conn = database()
    cursor = conn.cursor()  # returns tuples

    # --- Fetch customer and bill info using bill_no ---
    cursor.execute("""
    SELECT b.id, c.name, c.mobile, b.bill_no, b.vehicle_number, b.vehicle_type,
           b.total_amount, b.payment_mode, b.created_at
    FROM bills b
    INNER JOIN customers c ON b.customer_id = c.id
    WHERE b.bill_no = %s
    """, (bill_no,))

    bill_info = cursor.fetchone()
    if not bill_info:
        cursor.close()
        conn.close()
        return None, None  # Bill not found

    bill_id = bill_info[0]  # bills.id

    # --- Fetch all services for this bill ---
    cursor.execute("""
    SELECT service_name, service_price
    FROM bill_services
    WHERE bill_id = %s
    """, (bill_id,))

    services = cursor.fetchall()

    # --- Format services list ---
    services_text = ""
    for s in services:
        services_text += f"- {s[0]}: ₹{s[1]}\n"  # s[0]=service_name, s[1]=service_price

    # --- Create WhatsApp message ---
    msg = f"""
🚗✨ नमस्ते {bill_info[1]}!

आपल्या वाहनासाठी बिल तपशील:

🧾 बिल क्र.: {bill_info[3]}
🚘 वाहन क्रमांक: {bill_info[4]}
🚗 वाहन प्रकार: {bill_info[5]}
🕒 बिल दिनांक: {bill_info[8].strftime('%d-%m-%Y %H:%M')}

💳 पेमेंट मोड: {bill_info[7]}

🛠️ सेवांचा तपशील:
{services_text}
💰 एकूण रक्कम: ₹{bill_info[6]}

🙏 सह्याद्री वॉशिंग सेंटर मध्ये आपले स्वागत आहे!
"""

    cursor.close()
    conn.close()

    return msg, bill_info[2]  # mobile number


# --- Example usage ---
message_text, customer_number = generate_bill_message(1004)
print("Number:", customer_number)
print("Message:\n", message_text)
if customer_number != None and message_text != None:
    send_message(customer_number, message_text)

