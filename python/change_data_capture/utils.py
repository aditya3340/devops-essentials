import json
import datetime
import re

COL_VALUE_PATTERN = re.compile(r"(\w+)\[.*?\]:\s*(.+?)(?=\s\w+\[|$)", re.IGNORECASE)


def parse_row_data(data_string):
    row_data = {}

    # Iterate over all matches found in the data string
    for match in COL_VALUE_PATTERN.finditer(data_string):
        col_name = match.group(1).lower()
        # The captured value (Group 2) is stripped of leading/trailing spaces/quotes in the logic below
        raw_value = match.group(2).strip()

        # --- Value Type Conversion and Cleanup ---
        if raw_value.lower() == "null":
            value = None
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            # Strip single quotes from string/timestamp values
            value = raw_value.strip("'")
        else:
            # Attempt to convert to number types
            try:
                # Check for float first (handles integers too)
                if "." in raw_value:
                    value = float(raw_value)
                else:
                    value = int(raw_value)
            except ValueError:
                value = raw_value  # Fallback to string

        row_data[col_name] = value

    return row_data


def consume(message):
    """
    Parses the raw replication message payload and converts it into a JSON object.
    """
    payload = message.payload.strip()

    # Initialize the structured event object
    event = {
        "timestamp": datetime.datetime.now().isoformat(),
        "lsn": str(message.data_start),
        "type": "TRANSACTION_CONTROL",
    }

    if payload.startswith("BEGIN"):
        event["transaction_id"] = payload.split()[1]
        event["action"] = "BEGIN"

    elif payload.startswith("COMMIT"):
        event["transaction_id"] = payload.split()[1]
        event["action"] = "COMMIT"

    elif payload.startswith("table"):
        header_parts = payload.split(": ", 2)

        if len(header_parts) < 3:
            # Should not happen for a valid data change message, but included for robustness
            event["type"] = "UNPARSABLE_MESSAGE"
            event["payload_raw"] = payload
            json_output = json.dumps(event, indent=2)
            print(json_output)
            print("-" * 60)
            return

        # Part 1: Contains the table name (e.g., 'table public.products')
        table_name_match = re.match(r"table\s+(\w+\.\w+)", header_parts[0])
        table_name = table_name_match.group(1) if table_name_match else "unknown.table"

        # Part 2: Contains the operation (e.g., 'INSERT', 'UPDATE', 'DELETE')
        operation = header_parts[1].upper()

        # Part 3: Contains the actual data string (e.g., 'id[integer]:7 name[...]:'Test2'...')
        data_string = header_parts[2]

        # Process the structured row data
        structured_data = parse_row_data(data_string)

        event["type"] = "DATA_CHANGE"
        event["table"] = table_name
        event["action"] = operation
        event["data"] = structured_data
        # Clean up event keys
        if "payload" in event:
            del event["payload"]

    # Output the structured event as a JSON string
    json_output = json.dumps(event, indent=2)
    print(json_output)
    print("-" * 60)
