import os
import drawpyo

# Misc stuff that only needs to run once at the beginning
def draw_network():
    ####################################
    ############ SETUP #################
    ####################################
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

    ############################
    ########### DRAW ###########
    ############################

    items = []

    ############################
    ########### FIN ############
    ############################
    # must create parent container after icons in order to preserve position
    parent_container = drawpyo.diagram.Object(
        page=page,
        value='bunger subnet',
        autosize_margin=50,
    )
    parent_container.apply_style_string(
        "whiteSpace=wrap;fontSize=12;fontStyle=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;"
    )
    for index,item in enumerate(items,start=1):
        parent_container.add_object(item)
        item.position_rel_to_parent = (50 + (1 * 50), 0)
        # 4 items: (30, 0) (150, 0) (30, 100) (150, 100)
    parent_container.resize_to_children()
    parent_container.position = (50, 65)

    file.write()

def main():


main()