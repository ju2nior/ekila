from typing import Literal
from typing import Optional
from typing import TypedDict


class CinetPayCallbackData(TypedDict):
    cpm_site_id: str
    signature: str
    cpm_trans_id: str
    cpm_custom: str
    cpm_payment_date: str
    cpm_amount: str
    cpm_currency: str
    cpm_payid: str
    cpm_payment_time: str
    cpm_error_message: str
    cpm_result: Literal["00", "17", "51", "400"]
    payment_method: str
    cpm_phone_prefixe: str
    cel_phone_num: str
    cpm_country: str
    cpm_sender_id: Optional[str]
    cpm_token: Optional[str]
    cpm_ipn_ack: Optional[str]
    cpm_status: Literal["ACCEPTED", "REFUSED", "CANCELLED", "PENDING"]
