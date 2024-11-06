import os
import drawpyo

custom_library = drawpyo.diagram.import_shape_database(
    file_name='os.toml'
)

file = drawpyo.File()
file.file_path = os.getcwd()
file.file_name = 'yuh.drawio'

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

item = drawpyo.diagram.object_from_library(
    library=custom_library,
    obj_name='windows',
    text_format=text,
    value='ball up top\n192.168.254.251',
    page=page,
    width=100,
    height=50
)

item2 = drawpyo.diagram.object_from_library(
    library=custom_library,
    obj_name='windows',
    text_format=text,
    value='chat is this real\n192.168.254.252',
    page=page,
    width=100,
    height=50
)

item3 = drawpyo.diagram.object_from_library(
    library=custom_library,
    obj_name='windows',
    text_format=text,
    value='jiving media\n192.168.254.253',
    page=page,
    width=100,
    height=50
)

item4 = drawpyo.diagram.object_from_library(
    library=custom_library,
    obj_name='fedora',
    text_format=text,
    value='roboto mono\n192.168.254.100',
    page=page,
    width=100,
    height=50
)

# must create parent container after icons in order to preserve position
parent_container = drawpyo.diagram.Object(
    page=page,
    value='bunger subnet',
    autosize_margin=50,
)
parent_container.apply_style_string(
    "whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;"
)
parent_container.add_object(item)
parent_container.add_object(item2)
parent_container.add_object(item3)
parent_container.add_object(item4)
item.position_rel_to_parent = (30, 0)
item2.position_rel_to_parent = (150, 0)
item3.position_rel_to_parent = (30, 100)
item4.position_rel_to_parent = (150, 100)
parent_container.resize_to_children()
parent_container.position = (50, 65)

# subnet text box test
ip_subnet = drawpyo.diagram.Object(
    value="192.168.254.128/25",
    text_format=drawpyo.diagram.text_format.TextFormat(
        fontColor='#000000',
        fontFamily='Helvetica',
        fontSize=12,
        align='left',
        direction='horizontal',
        labelPosition='center',
        verticalAlign='bottom',
        spacing=0
    ),
    page=page,
    width=110,
    height=15,
    position=(50,50),
    opacity=0
)

file.write()