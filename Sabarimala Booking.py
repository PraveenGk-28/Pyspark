#!/usr/bin/env python3

import requests
import time

headers = {
	'accept': 'application/json, text/plain, */*',
	'accept-language': 'en-GB,en;q=0.9',
	'cookie': '_gid=GA1.2.1195714729.1733408527; _gat_gtag_UA_151897453_1=1; _ga_8HFV0345SF=GS1.1.1733411843.2.1.1733412044.0.0.0; _ga=GA1.1.33034682.1733408527',
	'origin': 'https://sabarimalaonline.org',
	'priority': 'u=1, i',
	'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': 'macOS',
	'sec-fetch-dest': 'empty',
	'sec-fetch-mode': 'cors',
	'sec-fetch-site': 'same-origin',
	'tof-auth-token': 'ac1f521f-6c62-4a97-bcb5-6cccbf58d074',
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
	'Content-Type': 'application/json',
}

def get_slots():
	# response = requests.post("https://sabarimalaonline.org/api/eDarshan/darshanAvailability/2025-01-18/100001", headers = headers)
	response = requests.post("https://sabarimalaonline.org/api/eDarshan/darshanAvailability/2024-12-15/100001", headers = headers)
	if len(response.json()['darshanSlots']) > 0:
		return response.json()['darshanSlots']

	return None

def add_to_waitlist(slot):
	payload = {
		"bookingSelfOther": "group",
        # "darshanDate": "18-Jan-2025",
        "darshanDate": "15-Dec-2024",
        "reportingMasterId": "1",
        "channelTypeId": 100001,
        "darshanTypeId": 100001,
        "slotId": slot.get('slotId'),
        "slotName": slot.get('slotName'),
        "noOfPersons": 1,
        "ticketPriceTotal": "",
        "userId": "3157181",
        "serviceTypeId": "100001",
        "darshanBookingPilgrimList": [
            {"pilgrimMasterId": 20352192,"firstName": "KRISHNAMOORTHY","lastName": "NADESAN","dateOfBirth": "1983-05-16","mobileNumber": "9003992060","gender": "Male","idProofType": 10003,"idProofNumber": "846264530927","addressLine1": "","addressLine2": "","city": "100528","state": "124","country": "1001","pincode": "639004","image": "05122024/Pilgrim_24120516340134883967.png","newImage": None,"registrationStatus": "N","baliTharpanam": ""}
        ],
        "prasadamBookingList": []
	}

	response = requests.post("https://sabarimalaonline.org/api/tofcart/addToWishlist", json = {'darshanBookingModel': payload}, headers = headers)
	if response.status_code != 200:
		print('Add to Waitlist Status: ' + str(response.status_code))
		return None

	response = response.json()

	return response if response and 'bookingId' in response else None

def validateItems():
	response = requests.post("https://sabarimalaonline.org/api/eDarshan/validateItems", headers = headers)
	response = response.json()

	if response and 'validateCartDetailsList' in response:
		if response['proceedToPay'] == 1 and response['errorMessage'] == 'Cart is valid':
			return True

	return False

def get_cart_details():
	response = requests.post('https://sabarimalaonline.org/api/tofcart/getCartDetails', headers = headers)
	if response.status_code != 200:
		print('Cart Details Status: ' + str(response.status_code))
		return None

	response = response.json()
	print(response)

def finish_transaction(cart_id):
	response = requests.post('https://sabarimalaonline.org/api/tofcart/cartTransaction', json = {'cartId': cart_id} , headers = headers)
	if response.status_code != 200:
		print('Finish Transaction Status: ' + str(response.status_code))
		return None

	response = response.json()
	print(response)
	return True


def book_a_slot():
    slots = get_slots()

    waitlist = None
    cart_id = None
    if slots and len(slots) > 0:
    	print('Slot Available. Adding to Waitlist...')
    	waitlist = add_to_waitlist(slots[0])
    	print(waitlist)

    if waitlist:
    	cart_id = waitlist['cartId']
    	print('Added to waitlist...')
    	if validateItems():
    		print('Placing Order...')
    		if finish_transaction(cart_id):
    			print('Order Placed!!!')
    			return True

    return False

if __name__ == "__main__":
	for i in range(1000):
		book_slot_status = book_a_slot()

		print("Status " + str("{:04d}".format(i + 1)) + " : " + ("True" if book_slot_status else "False"))

		if book_slot_status:
			print('Booking Succeeded...')
			break

		time.sleep(2)

	print("Failed")






