from config import database
from messenger import send_message

def generate_bill_message(bill_no):
    conn = database()
    cursor = conn.cursor()

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
        return None, None

    bill_id = bill_info[0]
    cursor.execute("""
    SELECT service_name, service_price
    FROM bill_services
    WHERE bill_id = %s
    """, (bill_id,))
    services = cursor.fetchall()

    services_text = ", ".join([f"{s[0]} ₹{s[1]}" for s in services])

    # --- सुंदर मराठी बिल संदेश ---
    msg = (
        f"🌸 नमस्कार {bill_info[1]}!\n"
        f"आपल्या भेटीसाठी मनःपूर्वक धन्यवाद 🙏\n"
        f"आपल्या वाहनासाठी सेवा पूर्ण झाली आहे. 🧼🚗\n"
        f"🧾 बिल क्रमांक: {bill_info[3]}\n"
        f"🚘 वाहन क्र.: {bill_info[4]} ({bill_info[5]})\n"
        f"🛠️ सेवा: {services_text}\n"
        f"💰 एकूण रक्कम: ₹{bill_info[6]}\n"
        f"💳 पेमेंट मोड: {bill_info[7]}\n\n"
        f"पुन्हा भेट देण्याचे आमंत्रण!\n"
        f"📍 पत्ता: Sahyadri Business Park, Gund Plot, Paranda Road, Barshi, PIN 413411\n"
        f"📞 Mo. 8177809890\n"
        f"धन्यवाद! 🌿"
    )

    cursor.close()
    conn.close()
    send_message(bill_info[2], msg)
    return msg, bill_info[2]
