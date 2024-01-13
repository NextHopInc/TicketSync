
from new_syncro_alert import Collect_Syncro_Alert as csa
import connectwise_ticket_collection as connectwise
from connectwise_ticket import ticket_object as tik
def main(): 
    cw = connectwise.ConnectWise_Ticket_Collection(computer_name="alert[0]" , company_name="alert[1]" , unique="alert[2]",trigger="low_hd_space_trigger")
    tk = tik(ticket_data={})

    patch = tk.patch_request("  Some disks are low on space Drive C: space below 15.00  of 225.98 GB Capacity: 225.98 GB Remaining: 33.14 GB (14.66%)" ,109321 )
    cw.patch_request(patch=patch,ticket_number=109321)
main()