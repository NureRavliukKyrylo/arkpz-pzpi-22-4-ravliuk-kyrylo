
def validate_date_range(data):
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not start_date or not end_date:
        raise ValueError("Missing 'start_date' or 'end_date'")

    return start_date, end_date