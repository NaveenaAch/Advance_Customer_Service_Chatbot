# remit_api.py

import requests
import json
import re


def calculate_remit_amount(receive_country, payment_method, send_currency, collect_amount, receive_currency,
                           receive_amount, send_country):
    """
    Calls the remit calculator API to calculate the remit amount.
    """
    url = "https://jp.cityremit.global/web-api/config/v1/public/calculator/calculate"

    # Payload based on the provided structure
    payload = {
        "receive_country": receive_country,
        "payment_method": payment_method,
        "send_currency": send_currency,
        "collect_amount": collect_amount,
        "receive_currency": receive_currency,
        "receive_amount": receive_amount,
        "send_country": send_country
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()


        return data

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None


def extract_remit_parameters(query):
    """
    Extracts remit parameters from the user query.
    """
    # Default values (can be adjusted based on your use case)
    parameters = {
        "receive_country": "NP",  # Nepal
        "payment_method": "Bank Deposit",  # Default payment method
        "send_currency": "JPY",  # Japanese Yen
        "collect_amount": "1000",  # Default send amount
        "receive_currency": "NPR",  # Nepalese Rupee
        "receive_amount": "440",  # Default receive amount
        "send_country": "JP"  # Japan
    }

    # Extract send amount (e.g., "send 1000 JPY")
    send_amount_match = re.search(r"send (\d+)", query)
    if send_amount_match:
        parameters["collect_amount"] = send_amount_match.group(1)

    # Extract send currency (e.g., "send 1000 JPY" or "from JPY")
    send_currency_match = re.search(r"(JPY|USD|EUR|BDT|NPR|other currency codes) ?", query)
    if send_currency_match:
        parameters["send_currency"] = send_currency_match.group(1)

    # Extract receive currency (e.g., "to NPR" or "to BDT")
    receive_currency_match = re.search(r"to (\w{3})", query)
    if receive_currency_match:
        parameters["receive_currency"] = receive_currency_match.group(1)

    # Check for different payment methods mentioned in the query
    if "Bank Transfer" in query:
        parameters["payment_method"] = "Bank Transfer"
    elif "Cash Pickup" in query:
        parameters["payment_method"] = "Cash Pickup"
    elif "Mobile Money" in query:
        parameters["payment_method"] = "Mobile Money"

    return parameters