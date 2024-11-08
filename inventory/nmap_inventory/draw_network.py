import os
import drawpyo
import csv
import math

# Parse the input file. Returns a list of dictionaries (one dictionary per host)
def parse_input(file = "nmap_results.csv"):
    hosts = []
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
     
        # Define column headers (in case you need them for processing or reference)
        """
        headers = [
            "host", "hostname", "hostname_type", "protocol", "port",
            "name", "state", "product", "extrainfo", "reason",
            "version", "conf", "cpe"
        ]
        """
        headers = ["host","protocol","port","name","state","product","extrainfo","reason","version","conf"]

        # Parse each line and print or process the fields
        for row in reader:
            # Ensure the row has the correct number of fields
            if len(row) == len(headers):
                # Create a dictionary for easier field access (optional)
                entry = dict(zip(headers, row))
                hosts.append(entry)

    return hosts

# Do the draw.
def draw_network(hosts):
    ####################################
    ############ SETUP #################
    ####################################
    custom_library = drawpyo.diagram.import_shape_database(
        file_name='os.toml'
    )

    file = drawpyo.File()
    file.file_path = os.getcwd()
    file.file_name = 'network_diagram.drawio'

    text = drawpyo.diagram.text_format.TextFormat(
        fontColor='#000000',
        fontFamily='Helvetica',
        fontSize=12,
        align='center',
        direction='horizontal',
        labelPosition='center',
        # labelBackgroundColor='#ff2d00',
        verticalAlign='bottom',
        spacingBottom=-35
    )

    page = drawpyo.Page(
        file=file,
        width=1100,
        height=850
    )

    ############################
    ########### DRAW ###########
    ############################

    """
    we want to arrange the hosts in a pretty equal way
    prefer going longer vertically when possible because there's prob lots of subnets
    1 host: 1 row
    2 hosts: 2 rows (1 column)
    3 hosts: 2 rows (2 columns)
    4 hosts: 2 rows (2 columns)
    5 hosts: 2 rows (3 columns)
    6 hosts: 2 rows (3 columns)
    7 hosts: 3 rows (3 columns)
    8 hosts: 3 rows (3 columns)
    9 hosts: 3 rows (3 columns)
    10 hosts: 4 rows (3 columns)
    11 hosts: 4 rows (3 columns)
    """
    hosts_count = len(hosts)
    rows = 4
    columns = math.ceil(hosts_count / rows)

    items = []
    for host in hosts:
        item = drawpyo.diagram.object_from_library(
            library=custom_library,
            obj_name='windows',
            text_format=text,
            value=f'{host[host]}', #\n for new line
            page=page,
            width=100,
            height=50
        )
        items.append(item)

    ############################
    ########### FIN ############
    ############################
    # must create parent container after icons in order to preserve position
    parent_container = drawpyo.diagram.Object(
        page=page,
        value='Main Subnet',
        autosize_margin=50,
    )
    parent_container.apply_style_string(
        "whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;"
    )
    row_index, col_index = 0, 0
    for index,item in enumerate(items,start=1):
        col_index += 1
        if col_index > columns:
            col_index = 0
            row_index += 1
        parent_container.add_object(item)
        item.position_rel_to_parent = ((col_index * 50), (row_index * 50))
        # 4 items: (30, 0) (150, 0) (30, 100) (150, 100)
    parent_container.resize_to_children()
    #parent_container.position = (50, 65)
    parent_container.position = (0, 0)

    file.write()

def main():
    hosts = parse_input()
    draw_network(hosts)

main()