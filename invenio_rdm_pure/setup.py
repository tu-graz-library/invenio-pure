from datetime import date
import os

dirpath = os.path.dirname(os.path.abspath(__file__))

# data_setup_path = f"{dirpath}/data_setup"
data_setup_path = "../june/data_setup"

pure_uuid_length = 36

# Pure REST API references
pure_rest_api_url = open(f"{data_setup_path}/pure_rest_api_url.txt", "r").readline()
pure_api_key = open(f"{data_setup_path}/pure_api_key.txt", "r").readline()
pure_password = open(f"{data_setup_path}/pure_password.txt", "r").readline()
pure_username = open(f"{data_setup_path}/pure_username.txt", "r").readline()

# Pure import
pure_import_path = "templates/invenio_rdm_pure/temporary_files"
pure_import_file = f"{dirpath}/{pure_import_path}/pure_import.xml"

# RDM user pure_admin
pure_rdm_user_file = f"{data_setup_path}/rdmUser_pureEmail.txt"
pure_rdm_password_file = f"{data_setup_path}/rdmUser_purePassword.txt"

# RDM
rdm_host_url = open(f"{data_setup_path}/rdm_host_url.txt", "r").readline()
token_rdm = open(f"{data_setup_path}/rdm_token.txt", "r").readline()
rdm_records_url = f"{rdm_host_url}api/records/"
push_dist_sec = 0.8  # Time gap between RDM push requests
wait_429 = 900  # Too many requests sent to the server (waits 15 minutes)

# LOG FILES
days_keep_log = 30  # Deletes log files after x days
lines_successful_changes = 90  # Reduce the number of lines in successful_changes.txt

# Percentage of updated items to considere the upload task successful
upload_percent_accept = 90

# OTHER
iso6393_file_name = f"{dirpath}/source/iso6393.json"
pure_uuid_length = 36

# EMAIL
email_receiver = open(f"{data_setup_path}/email_receiver.txt", "r").readline()
email_sender = open(f"{data_setup_path}/email_sender.txt", "r").readline()
email_sender_password = open(
    f"{data_setup_path}/email_sender_password.txt", "r"
).readline()
email_smtp_server = "smtp.gmail.com"
email_smtp_port = 587
email_subject = "Delete Pure file"
email_message = (
    """Subject: """ + email_subject + """Please remove from pure uuid {} the file {}."""
)

# RESTRICTIONS
possible_record_restrictions = ["groups", "owners", "ip_range", "ip_single"]

# VERSIONING
versioning_running = False

# ACCESS RIGHTS
accessright_pure_to_rdm = {
    "Open": "open",
    "Embargoed": "embargoed",
    "Restricted": "restricted",
    "Closed": "closed",
    "Unknown": "closed",
    "Indeterminate": "closed",
    "None": "closed",
}

# DATABASE
database_uri = {
    "db_host": f"{data_setup_path}/db_host.txt",
    "db_name": f"{data_setup_path}/db_name.txt",
    "db_user": f"{data_setup_path}/db_user.txt",
    "db_password": f"{data_setup_path}/db_password.txt",
}


# REPORT LOGS
reports_full_path = f"{dirpath}/reports/"
base_path = f"{reports_full_path}{date.today()}"
log_files_name = {
    "groups": f"{base_path}_groups.log",
    "owners": f"{base_path}_owners.log",
    "pages": f"{base_path}_pages.log",
    "console": f"{base_path}_console.log",
    "changes": f"{base_path}_changes.log",
}

# DATA FILES NAME
base_path = f"{dirpath}/data"
data_files_name = {
    "successful_changes": f"{base_path}/successful_changes.txt",
    "user_ids_match": f"{base_path}/user_ids_match.txt",
    "all_rdm_records": f"{base_path}/all_rdm_records.txt",
    "rdm_record_owners": f"{base_path}/rdm_record_owners.txt",
    "transfer_uuid_list": f"{base_path}/to_transmit.txt",
    "delete_recid_list": f"{base_path}/to_delete.txt",
}

# TEMPORARY FILES (used to keep truck of the data received and transmitted)
base_path = f"{dirpath}/data/temporary_files"
temporary_files_name = {
    "base_path": f"{base_path}",
    "get_pure_metadata": f"{base_path}/get_pure_metadata.json",
    "get_rdm_metadata": f"{base_path}/get_rdm_metadata.json",
    "post_rdm_response": f"{base_path}/post_rdm_response.json",
    "post_rdm_metadata": f"{base_path}/post_rdm_metadata.json",
}
