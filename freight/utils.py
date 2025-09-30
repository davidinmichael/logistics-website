import random
import string


def generate_tracking_number(length=10):
    """Generate a random alphanumeric uppercase tracking number."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))

def generate_waybill_number(length=10):
    """Generate a random alphanumeric uppercase tracking number."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))

def generate_purchase_order(length=10):
    """Generate a random alphanumeric uppercase tracking number."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))
