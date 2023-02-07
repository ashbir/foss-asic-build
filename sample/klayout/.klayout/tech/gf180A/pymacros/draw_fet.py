# Copyright 2022 GlobalFoundries PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

########################################################################################################################
## FET Pcells Generators for Klayout of GF180MCU
########################################################################################################################

from math import ceil, floor
import numpy as np

import gdsfactory as gf
from gdsfactory.types import Float2, LayerSpec
from .via_generator import via_generator, via_stack
from .layers_def import layer


@gf.cell
def alter_interdig(
    sd_diff,
    pc1,
    pc2,
    poly_con,
    sd_diff_intr,
    l_gate=0.15,
    inter_sd_l=0.15,
    nf=1,
    pat="",
) -> gf.Component:
    """Returns interdigitation polygons of gate with alterating poly contacts

    Args :
        sd_diff : source/drain diffusion rectangle
        pc1 : first poly contact array
        pc2 : second poly contact array
        poly_con : componenet of poly contact
        sd_diff_inter : inter source/drain diffusion rectangle
        l_gate : gate length
        inter_sd_l : inter diffusion length
        nf : number of fingers
        pat : string of the required pattern
    """

    c_inst = gf.Component()

    m2_spacing = 0.28
    via_size = (0.26, 0.26)
    via_enc = (0.06, 0.06)
    via_spacing = (0.26, 0.26)
    con_comp_enc = 0.07

    pat_o = []
    pat_e = []

    for i in range(int(nf)):
        if i % 2 == 0:
            pat_e.append(pat[i])
        else:
            pat_o.append(pat[i])

    nt_o = []
    [nt_o.append(x) for x in pat_o if x not in nt_o]

    nt_e = []
    [nt_e.append(x) for x in pat_e if x not in nt_e]

    nl_b = len(nt_e)
    nl_u = len(nt_o)

    m2_y = via_size[1] + 2 * via_enc[1]
    m2 = gf.components.rectangle(
        size=(sd_diff.xmax - sd_diff.xmin, m2_y), layer=layer["metal2"],
    )

    m2_arrb = c_inst.add_array(
        component=m2, columns=1, rows=nl_b, spacing=(0, -m2_y - m2_spacing),
    )
    m2_arrb.movey(pc1.ymin - m2_spacing - m2_y)

    m2_arru = c_inst.add_array(
        component=m2, columns=1, rows=nl_u, spacing=(0, m2_y + m2_spacing),
    )
    m2_arru.movey(pc2.ymax + m2_spacing)

    for i in range(nl_u):
        for j in range(floor(nf / 2)):
            if pat_o[j] == nt_o[i]:
                m1 = c_inst.add_ref(
                    gf.components.rectangle(
                        size=(
                            poly_con.xmax - poly_con.xmin,
                            ((pc2.ymax + (i + 1) * (m2_spacing + m2_y)) - pc2.ymin),
                        ),
                        layer=layer["metal1"],
                    )
                )
                m1.xmin = (
                    sd_diff_intr.xmin
                    + con_comp_enc / 2
                    + (2 * j + 1) * (l_gate + inter_sd_l)
                )
                m1.ymin = pc2.ymin

                via1_dr = via_generator(
                    x_range=(m1.xmin, m1.xmax),
                    y_range=(
                        m2_arru.ymin + i * (m2_y + m2_spacing),
                        m2_arru.ymin + i * (m2_y + m2_spacing) + m2_y,
                    ),
                    via_enclosure=via_enc,
                    via_layer=layer["via1"],
                    via_size=via_size,
                    via_spacing=via_spacing,
                )
                via1 = c_inst.add_ref(via1_dr)
                c_inst.add_label(
                    f"{pat_o[j]}",
                    position=(
                        (via1.xmax + via1.xmin) / 2,
                        (via1.ymax + via1.ymin) / 2,
                    ),
                    layer=layer["metal1_label"],
                )

    for i in range(nl_b):
        for j in range(ceil(nf / 2)):
            if pat_e[j] == nt_e[i]:

                m1 = c_inst.add_ref(
                    gf.components.rectangle(
                        size=(
                            poly_con.xmax - poly_con.xmin,
                            ((pc1.ymax + (i + 1) * (m2_spacing + m2_y)) - pc1.ymin),
                        ),
                        layer=layer["metal1"],
                    )
                )
                m1.xmin = (
                    sd_diff_intr.xmin
                    + con_comp_enc / 2
                    + (2 * j) * (l_gate + inter_sd_l)
                )
                m1.ymin = -(m1.ymax - m1.ymin) + (pc1.ymax)
                # m1.move(((sd_l- ((poly_con.xmax - poly_con.xmin - l)/2) + (2*j)*(l+inter_sd_l)), -(m1.ymax - m1.ymin) + (pc1.ymax-0.06)))
                via1_dr = via_generator(
                    x_range=(m1.xmin, m1.xmax),
                    y_range=(
                        m2_arrb.ymax - i * (m2_spacing + m2_y) - m2_y,
                        m2_arrb.ymax - i * (m2_spacing + m2_y),
                    ),
                    via_enclosure=via_enc,
                    via_layer=layer["via1"],
                    via_size=via_size,
                    via_spacing=via_spacing,
                )
                via1 = c_inst.add_ref(via1_dr)
                c_inst.add_label(
                    f"{pat_e[j]}",
                    position=(
                        (via1.xmax + via1.xmin) / 2,
                        (via1.ymax + via1.ymin) / 2,
                    ),
                    layer=layer["metal1_label"],
                )

    m3_x = via_size[0] + 2 * via_enc[0]
    m3_spacing = m2_spacing

    for i in range(nl_b):
        for j in range(nl_u):
            if nt_e[i] == nt_o[j]:

                m2_join_b = c_inst.add_ref(
                    gf.components.rectangle(
                        size=(m2_y + (i + 1) * (m3_spacing + m3_x), m2_y,),
                        layer=layer["metal2"],
                    ).move(
                        (
                            m2_arrb.xmin - (m2_y + (i + 1) * (m3_spacing + m3_x)),
                            m2_arrb.ymax - i * (m2_spacing + m2_y) - m2_y,
                        )
                    )
                )
                m2_join_u = c_inst.add_ref(
                    gf.components.rectangle(
                        size=(m2_y + (i + 1) * (m3_spacing + m3_x), m2_y,),
                        layer=layer["metal2"],
                    ).move(
                        (
                            m2_arru.xmin - (m2_y + (i + 1) * (m3_spacing + m3_x)),
                            m2_arru.ymin + j * (m2_spacing + m2_y),
                        )
                    )
                )
                m3 = c_inst.add_ref(
                    gf.components.rectangle(
                        size=(m3_x, m2_join_u.ymax - m2_join_b.ymin,),
                        layer=layer["metal1"],
                    )
                )
                m3.move((m2_join_b.xmin, m2_join_b.ymin))
                via2_dr = via_generator(
                    x_range=(m3.xmin, m3.xmax),
                    y_range=(m2_join_b.ymin, m2_join_b.ymax),
                    via_enclosure=via_enc,
                    via_size=via_size,
                    via_layer=layer["via1"],
                    via_spacing=via_spacing,
                )
                c_inst.add_array(
                    component=via2_dr,
                    columns=1,
                    rows=2,
                    spacing=(0, m2_join_u.ymin - m2_join_b.ymin,),
                )  # via2_draw
    return c_inst


@gf.cell
def interdigit(
    sd_diff,
    pc1,
    pc2,
    poly_con,
    sd_diff_intr,
    l_gate: float = 0.15,
    inter_sd_l: float = 0.23,
    sd_l: float = 0.15,
    nf=1,
    patt=[""],
    gate_con_pos="top",
) -> gf.Component:
    """Returns interdigitation related polygons

    Args :
        sd_diff : source/drain diffusion rectangle
        pc1 : first poly contact array
        pc2 : second poly contact array
        poly_con : componenet of poly contact
        sd_diff_inter : inter source/drain diffusion rectangle
        l_gate : gate length
        inter_sd_l : inter diffusion length
        nf : number of fingers
        pat : string of the required pattern
        gate_con_pos : position of gate contact
    """
    c_inst = gf.Component()

    if nf == len(patt):
        pat = list(patt)
        nt = (
            []
        )  # list to store the symbols of transistors and thier number nt(number of transistors)
        [nt.append(x) for x in pat if x not in nt]
        nl = int(len(nt))

        m2_spacing = 0.28
        via_size = (0.26, 0.26)
        via_enc = (0.06, 0.06)
        via_spacing = (0.26, 0.26)

        m2_y = via_size[1] + 2 * via_enc[1]
        m2 = gf.components.rectangle(
            size=(sd_diff.xmax - sd_diff.xmin, m2_y), layer=layer["metal2"]
        )

        if gate_con_pos == "alternating":
            c_inst.add_ref(
                alter_interdig(
                    sd_diff=sd_diff,
                    pc1=pc1,
                    pc2=pc2,
                    poly_con=poly_con,
                    sd_diff_intr=sd_diff_intr,
                    l_gate=l_gate,
                    inter_sd_l=inter_sd_l,
                    nf=nf,
                    pat=pat,
                )
            )

        elif gate_con_pos == "top":

            m2_arr = c_inst.add_array(
                component=m2,
                columns=1,
                rows=nl,
                spacing=(0, m2.ymax - m2.ymin + m2_spacing),
            )
            m2_arr.movey(pc2.ymax + m2_spacing)

            for i in range(nl):
                for j in range(int(nf)):
                    if pat[j] == nt[i]:
                        m1 = c_inst.add_ref(
                            gf.components.rectangle(
                                size=(
                                    poly_con.xmax - poly_con.xmin,
                                    (
                                        (pc2.ymax + (i + 1) * (m2_spacing + m2_y))
                                        - ((1 - j % 2) * pc1.ymin)
                                        - (j % 2) * pc2.ymin
                                    ),
                                ),
                                layer=layer["metal1"],
                            )
                        )
                        m1.move(
                            (
                                (
                                    sd_l
                                    - ((poly_con.xmax - poly_con.xmin - l_gate) / 2)
                                    + j * (l_gate + inter_sd_l)
                                ),
                                (1 - j % 2) * (pc1.ymin + 0.06)
                                + (j % 2) * (pc2.ymin + 0.06),
                            )
                        )
                        via1_dr = via_generator(
                            x_range=(m1.xmin, m1.xmax),
                            y_range=(
                                m2_arr.ymin + i * (m2_spacing + m2_y),
                                m2_arr.ymin + i * (m2_spacing + m2_y) + m2_y,
                            ),
                            via_enclosure=via_enc,
                            via_layer=layer["via1"],
                            via_size=via_size,
                            via_spacing=via_spacing,
                        )
                        via1 = c_inst.add_ref(via1_dr)
                        c_inst.add_label(
                            f"{pat[j]}",
                            position=(
                                (via1.xmax + via1.xmin) / 2,
                                (via1.ymax + via1.ymin) / 2,
                            ),
                            layer=layer["metal1_label"],
                        )

        elif gate_con_pos == "bottom":

            m2_arr = c_inst.add_array(
                component=m2, columns=1, rows=nl, spacing=(0, -m2_y - m2_spacing),
            )
            m2_arr.movey(pc2.ymin - m2_spacing - m2_y)

            for i in range(nl):
                for j in range(int(nf)):
                    if pat[j] == nt[i]:

                        m1 = c_inst.add_ref(
                            gf.components.rectangle(
                                size=(
                                    poly_con.xmax - poly_con.xmin,
                                    (
                                        (pc1.ymax + (i + 1) * (m2_spacing + m2_y))
                                        - (j % 2) * pc1.ymin
                                        - (1 - j % 2) * pc2.ymin
                                    ),
                                ),
                                layer=layer["metal1"],
                            )
                        )
                        m1.move(
                            (
                                (
                                    sd_l
                                    - ((poly_con.xmax - poly_con.xmin - l_gate) / 2)
                                    + j * (l_gate + inter_sd_l)
                                ),
                                -(m1.ymax - m1.ymin)
                                + (1 - j % 2) * (pc1.ymax - 0.06)
                                + (j % 2) * (pc2.ymax - 0.06),
                            )
                        )
                        via1_dr = via_generator(
                            x_range=(m1.xmin, m1.xmax),
                            y_range=(
                                m2_arr.ymax - i * (m2_spacing + m2_y) - m2_y,
                                m2_arr.ymax - i * (m2_spacing + m2_y),
                            ),
                            via_enclosure=via_enc,
                            via_layer=layer["via1"],
                            via_size=via_size,
                            via_spacing=via_spacing,
                        )
                        via1 = c_inst.add_ref(via1_dr)
                        c_inst.add_label(
                            f"{pat[j]}",
                            position=(
                                (via1.xmax + via1.xmin) / 2,
                                (via1.ymax + via1.ymin) / 2,
                            ),
                            layer=layer["metal1_label"],
                        )

    return c_inst


@gf.cell
def hv_gen(
    c_inst, volt: str = "3.3V", dg_encx: float = 0.1, dg_ency: float = 0.1
) -> gf.Component:
    """Returns high volatge related polygons

    Args :
        c_inst : dualgate enclosed componenet
        volt : operating voltage
        dg_encx : dualgate enclosure in x_direction
        dg_ency : dualgate enclosure in y_direction
    """

    c = gf.Component()

    if volt == "5V" or volt == "6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(c_inst.size[0] + (2 * dg_encx), c_inst.size[1] + (2 * dg_ency),),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = c_inst.xmin - dg_encx
        dg.ymin = c_inst.ymin - dg_ency

        if volt == "5V":
            v5x = c.add_ref(
                gf.components.rectangle(
                    size=(dg.size[0], dg.size[1]), layer=layer["v5_xtor"]
                )
            )
            v5x.xmin = dg.xmin
            v5x.ymin = dg.ymin

    return c


@gf.cell
def bulk_gr_gen(
    c_inst,
    comp_spacing: float = 0.1,
    poly2_comp_spacing: float = 0.1,
    volt: str = "3.3V",
    grw: float = 0.36,
    l_d: float = 0.1,
    implant_layer: LayerSpec = layer["pplus"],
) -> gf.Component():
    """Returns guardring

    Args :
        c_inst : componenet enclosed by guardring
        comp_spacing : spacing between comp polygons
        poly2_comp_spacing : spacing between comp and poly2 polygons
        volt : operating voltage
        grw : guardring width
        l_d : total diffusion length
        implant_layer : layer of comp implant (nplus,pplus)
    """

    c = gf.Component()

    comp_pp_enc: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07
    dg_enc_cmp = 0.24

    c_temp = gf.Component("temp_store")
    rect_bulk_in = c_temp.add_ref(
        gf.components.rectangle(
            size=(
                (c_inst.xmax - c_inst.xmin) + 2 * comp_spacing,
                (c_inst.ymax - c_inst.ymin) + 2 * poly2_comp_spacing,
            ),
            layer=layer["comp"],
        )
    )
    rect_bulk_in.move((c_inst.xmin - comp_spacing, c_inst.ymin - poly2_comp_spacing))
    rect_bulk_out = c_temp.add_ref(
        gf.components.rectangle(
            size=(
                (rect_bulk_in.xmax - rect_bulk_in.xmin) + 2 * grw,
                (rect_bulk_in.ymax - rect_bulk_in.ymin) + 2 * grw,
            ),
            layer=layer["comp"],
        )
    )
    rect_bulk_out.move((rect_bulk_in.xmin - grw, rect_bulk_in.ymin - grw))
    B = c.add_ref(
        gf.geometry.boolean(
            A=rect_bulk_out, B=rect_bulk_in, operation="A-B", layer=layer["comp"],
        )
    )

    psdm_in = c_temp.add_ref(
        gf.components.rectangle(
            size=(
                (rect_bulk_in.xmax - rect_bulk_in.xmin) - 2 * comp_pp_enc,
                (rect_bulk_in.ymax - rect_bulk_in.ymin) - 2 * comp_pp_enc,
            ),
            layer=layer["pplus"],
        )
    )
    psdm_in.move((rect_bulk_in.xmin + comp_pp_enc, rect_bulk_in.ymin + comp_pp_enc))
    psdm_out = c_temp.add_ref(
        gf.components.rectangle(
            size=(
                (rect_bulk_out.xmax - rect_bulk_out.xmin) + 2 * comp_pp_enc,
                (rect_bulk_out.ymax - rect_bulk_out.ymin) + 2 * comp_pp_enc,
            ),
            layer=layer["pplus"],
        )
    )
    psdm_out.move((rect_bulk_out.xmin - comp_pp_enc, rect_bulk_out.ymin - comp_pp_enc,))
    c.add_ref(
        gf.geometry.boolean(A=psdm_out, B=psdm_in, operation="A-B", layer=implant_layer)
    )  # implant_draw(pplus or nplus)

    # generating contacts

    c.add_ref(
        via_generator(
            x_range=(rect_bulk_in.xmin + con_size, rect_bulk_in.xmax - con_size,),
            y_range=(rect_bulk_out.ymin, rect_bulk_in.ymin),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # bottom contact

    c.add_ref(
        via_generator(
            x_range=(rect_bulk_in.xmin + con_size, rect_bulk_in.xmax - con_size,),
            y_range=(rect_bulk_in.ymax, rect_bulk_out.ymax),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # upper contact

    c.add_ref(
        via_generator(
            x_range=(rect_bulk_out.xmin, rect_bulk_in.xmin),
            y_range=(rect_bulk_in.ymin + con_size, rect_bulk_in.ymax - con_size,),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # right contact

    c.add_ref(
        via_generator(
            x_range=(rect_bulk_in.xmax, rect_bulk_out.xmax),
            y_range=(rect_bulk_in.ymin + con_size, rect_bulk_in.ymax - con_size,),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # left contact

    comp_m1_in = c_temp.add_ref(
        gf.components.rectangle(
            size=(
                (l_d) + 2 * comp_spacing,
                (c_inst.ymax - c_inst.ymin) + 2 * poly2_comp_spacing,
            ),
            layer=layer["metal1"],
        )
    )
    comp_m1_in.move((-comp_spacing, c_inst.ymin - poly2_comp_spacing))
    comp_m1_out = c_temp.add_ref(
        gf.components.rectangle(
            size=(
                (rect_bulk_in.xmax - rect_bulk_in.xmin) + 2 * grw,
                (rect_bulk_in.ymax - rect_bulk_in.ymin) + 2 * grw,
            ),
            layer=layer["metal1"],
        )
    )
    comp_m1_out.move((rect_bulk_in.xmin - grw, rect_bulk_in.ymin - grw))
    c.add_ref(
        gf.geometry.boolean(
            A=rect_bulk_out, B=rect_bulk_in, operation="A-B", layer=layer["metal1"],
        )
    )  # metal1_gaurdring

    c.add_ref(hv_gen(c_inst=B, volt=volt, dg_encx=dg_enc_cmp, dg_ency=dg_enc_cmp))

    return c


@gf.cell
def pcmpgr_gen(dn_rect, grw: float = 0.36) -> gf.Component:
    """Return deepnwell guardring

    Args :
        dn_rect : deepnwell polygon
        grw : guardring width
    """

    c = gf.Component()

    comp_pp_enc: float = 0.16
    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07
    pcmpgr_enc_dn = 2.5

    c_temp_gr = gf.Component("temp_store guard ring")
    rect_pcmpgr_in = c_temp_gr.add_ref(
        gf.components.rectangle(
            size=(
                (dn_rect.xmax - dn_rect.xmin) + 2 * pcmpgr_enc_dn,
                (dn_rect.ymax - dn_rect.ymin) + 2 * pcmpgr_enc_dn,
            ),
            layer=layer["comp"],
        )
    )
    rect_pcmpgr_in.move((dn_rect.xmin - pcmpgr_enc_dn, dn_rect.ymin - pcmpgr_enc_dn))
    rect_pcmpgr_out = c_temp_gr.add_ref(
        gf.components.rectangle(
            size=(
                (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * grw,
                (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * grw,
            ),
            layer=layer["comp"],
        )
    )
    rect_pcmpgr_out.move((rect_pcmpgr_in.xmin - grw, rect_pcmpgr_in.ymin - grw))
    c.add_ref(
        gf.geometry.boolean(
            A=rect_pcmpgr_out, B=rect_pcmpgr_in, operation="A-B", layer=layer["comp"],
        )
    )  # guardring bulk

    psdm_in = c_temp_gr.add_ref(
        gf.components.rectangle(
            size=(
                (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) - 2 * comp_pp_enc,
                (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) - 2 * comp_pp_enc,
            ),
            layer=layer["pplus"],
        )
    )
    psdm_in.move(
        (rect_pcmpgr_in.xmin + comp_pp_enc, rect_pcmpgr_in.ymin + comp_pp_enc,)
    )
    psdm_out = c_temp_gr.add_ref(
        gf.components.rectangle(
            size=(
                (rect_pcmpgr_out.xmax - rect_pcmpgr_out.xmin) + 2 * comp_pp_enc,
                (rect_pcmpgr_out.ymax - rect_pcmpgr_out.ymin) + 2 * comp_pp_enc,
            ),
            layer=layer["pplus"],
        )
    )
    psdm_out.move(
        (rect_pcmpgr_out.xmin - comp_pp_enc, rect_pcmpgr_out.ymin - comp_pp_enc,)
    )
    c.add_ref(
        gf.geometry.boolean(
            A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
        )
    )  # pplus_draw

    # generating contacts

    c.add_ref(
        via_generator(
            x_range=(rect_pcmpgr_in.xmin + con_size, rect_pcmpgr_in.xmax - con_size,),
            y_range=(rect_pcmpgr_out.ymin, rect_pcmpgr_in.ymin),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # bottom contact

    c.add_ref(
        via_generator(
            x_range=(rect_pcmpgr_in.xmin + con_size, rect_pcmpgr_in.xmax - con_size,),
            y_range=(rect_pcmpgr_in.ymax, rect_pcmpgr_out.ymax),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # upper contact

    c.add_ref(
        via_generator(
            x_range=(rect_pcmpgr_out.xmin, rect_pcmpgr_in.xmin),
            y_range=(rect_pcmpgr_in.ymin + con_size, rect_pcmpgr_in.ymax - con_size,),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # right contact

    c.add_ref(
        via_generator(
            x_range=(rect_pcmpgr_in.xmax, rect_pcmpgr_out.xmax),
            y_range=(rect_pcmpgr_in.ymin + con_size, rect_pcmpgr_in.ymax - con_size,),
            via_enclosure=(con_comp_enc, con_comp_enc),
            via_layer=layer["contact"],
            via_size=(con_size, con_size),
            via_spacing=(con_sp, con_sp),
        )
    )  # left contact

    comp_m1_in = c_temp_gr.add_ref(
        gf.components.rectangle(
            size=(rect_pcmpgr_in.size[0], rect_pcmpgr_in.size[1]),
            layer=layer["metal1"],
        )
    )

    comp_m1_out = c_temp_gr.add_ref(
        gf.components.rectangle(
            size=((comp_m1_in.size[0]) + 2 * grw, (comp_m1_in.size[1]) + 2 * grw,),
            layer=layer["metal1"],
        )
    )
    comp_m1_out.move((rect_pcmpgr_in.xmin - grw, rect_pcmpgr_in.ymin - grw))
    c.add_ref(
        gf.geometry.boolean(
            A=rect_pcmpgr_out, B=rect_pcmpgr_in, operation="A-B", layer=layer["metal1"],
        )
    )  # metal1 guardring

    return c


@gf.cell
def nfet_deep_nwell(
    deepnwell: bool = 0,
    pcmpgr: bool = 0,
    inst_size: Float2 = (0.1, 0.1),
    inst_xmin: float = 0.1,
    inst_ymin: float = 0.1,
    grw: float = 0.36,
) -> gf.Component:
    """Return nfet deepnwell

    Args :
        deepnwell : boolean of having deepnwell
        pcmpgr : boolean of having deepnwell guardring
        inst_size : deepnwell enclosed size
        inst_xmin : deepnwell enclosed xmin
        inst_ymin : deepnwell enclosed ymin
        grw : guardring width
    """

    c = gf.Component()

    dn_enc_lvpwell = 2.5
    lvpwell_enc_ncmp = 0.43

    if deepnwell == 1:

        lvp_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    inst_size[0] + (2 * lvpwell_enc_ncmp),
                    inst_size[1] + (2 * lvpwell_enc_ncmp),
                ),
                layer=layer["lvpwell"],
            )
        )

        lvp_rect.xmin = inst_xmin - lvpwell_enc_ncmp
        lvp_rect.ymin = inst_ymin - lvpwell_enc_ncmp

        dn_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    lvp_rect.size[0] + (2 * dn_enc_lvpwell),
                    lvp_rect.size[1] + (2 * dn_enc_lvpwell),
                ),
                layer=layer["dnwell"],
            )
        )

        dn_rect.xmin = lvp_rect.xmin - dn_enc_lvpwell
        dn_rect.ymin = lvp_rect.ymin - dn_enc_lvpwell

        if pcmpgr == 1:
            c.add_ref(pcmpgr_gen(dn_rect=dn_rect, grw=grw))

    return c


# @gf.cell
def draw_nfet(
    layout,
    l_gate: float = 0.28,
    w_gate: float = 0.22,
    sd_con_col: int = 1,
    inter_sd_l: float = 0.24,
    nf: int = 1,
    grw: float = 0.22,
    volt: str = "3.3V",
    bulk="None",
    con_bet_fin: int = 1,
    gate_con_pos="alternating",
    interdig: int = 0,
    patt="",
    deepnwell: int = 0,
    pcmpgr: int = 0,
) -> gf.Component:

    """
    Retern nfet

    Args:
        layout : layout object
        l : Float of gate length
        w : Float of gate width
        sd_l : Float of source and drain diffusion length
        inter_sd_l : Float of source and drain diffusion length between fingers
        nf : integer of number of fingers
        M : integer of number of multipliers
        grw : gaurd ring width when enabled
        type : string of the device type
        bulk : String of bulk connection type (None, Bulk Tie, Guard Ring)
        con_bet_fin : boolean of having contacts for diffusion between fingers
        gate_con_pos : string of choosing the gate contact position (bottom, top, alternating )

    """
    # used layers and dimensions

    end_cap: float = 0.22
    if volt == "3.3V":
        comp_spacing: float = 0.28
    else:
        comp_spacing: float = 0.36

    gate_np_enc: float = 0.23
    comp_np_enc: float = 0.16
    comp_pp_enc: float = 0.16
    poly2_spacing: float = 0.24
    pc_ext: float = 0.04

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07
    con_pl_enc = 0.07
    dg_enc_cmp = 0.24
    dg_enc_poly = 0.4

    sd_l_con = (
        ((sd_con_col) * con_size) + ((sd_con_col - 1) * con_sp) + 2 * con_comp_enc
    )
    sd_l = sd_l_con

    # gds components to store a single instance and the generated device
    c = gf.Component("sky_nfet_dev")

    c_inst = gf.Component("dev_temp")

    # generating sd diffusion

    if interdig == 1 and nf > 1 and nf != len(patt) and patt != "":
        nf = len(patt)

    l_d = (
        nf * l_gate + (nf - 1) * inter_sd_l + 2 * (con_comp_enc)
    )  # diffution total length
    rect_d_intr = gf.components.rectangle(size=(l_d, w_gate), layer=layer["comp"])
    sd_diff_intr = c_inst.add_ref(rect_d_intr)

    #     # generatin sd contacts

    if w_gate <= con_size + 2 * con_comp_enc:
        cmpc_y = con_comp_enc + con_size + con_comp_enc

    else:
        cmpc_y = w_gate

    cmpc_size = (sd_l_con, cmpc_y)

    sd_diff = c_inst.add_array(
        component=gf.components.rectangle(size=cmpc_size, layer=layer["comp"]),
        rows=1,
        columns=2,
        spacing=(cmpc_size[0] + sd_diff_intr.size[0], 0),
    )

    sd_diff.xmin = sd_diff_intr.xmin - cmpc_size[0]
    sd_diff.ymin = sd_diff_intr.ymin - (sd_diff.size[1] - sd_diff_intr.size[1]) / 2

    sd_con = via_stack(
        x_range=(sd_diff.xmin, sd_diff_intr.xmin),
        y_range=(sd_diff.ymin, sd_diff.ymax),
        base_layer=layer["comp"],
        metal_level=1,
    )
    c_inst.add_array(
        component=sd_con,
        columns=2,
        rows=1,
        spacing=(sd_l + nf * l_gate + (nf - 1) * inter_sd_l + 2 * (con_comp_enc), 0,),
    )

    if con_bet_fin == 1 and nf > 1:
        inter_sd_con = via_stack(
            x_range=(
                sd_diff_intr.xmin + con_comp_enc + l_gate,
                sd_diff_intr.xmin + con_comp_enc + l_gate + inter_sd_l,
            ),
            y_range=(0, w_gate),
            base_layer=layer["comp"],
            metal_level=1,
        )
        c_inst.add_array(
            component=inter_sd_con,
            columns=nf - 1,
            rows=1,
            spacing=(l_gate + inter_sd_l, 0),
        )

    # generating poly

    if l_gate <= con_size + 2 * con_pl_enc:
        pc_x = con_pl_enc + con_size + con_pl_enc

    else:
        pc_x = l_gate

    pc_size = (pc_x, con_pl_enc + con_size + con_pl_enc)

    c_pc = gf.Component("poly con")

    rect_pc = c_pc.add_ref(gf.components.rectangle(size=pc_size, layer=layer["poly2"]))

    poly_con = via_stack(
        x_range=(rect_pc.xmin, rect_pc.xmax),
        y_range=(rect_pc.ymin, rect_pc.ymax),
        base_layer=layer["poly2"],
        metal_level=1,
        li_enc_dir="H",
    )
    c_pc.add_ref(poly_con)

    if nf == 1:
        poly = c_inst.add_ref(
            gf.components.rectangle(
                size=(l_gate, w_gate + 2 * end_cap), layer=layer["poly2"]
            )
        )
        poly.xmin = sd_diff_intr.xmin + con_comp_enc
        poly.ymin = sd_diff_intr.ymin - end_cap

        if gate_con_pos == "bottom":
            mv = 0
            nr = 1
        elif gate_con_pos == "top":
            mv = pc_size[1] + w_gate + 2 * end_cap
            nr = 1
        else:
            mv = 0
            nr = 2

        pc = c_inst.add_array(
            component=c_pc,
            rows=nr,
            columns=1,
            spacing=(0, pc_size[1] + w_gate + 2 * end_cap),
        )
        pc.move((poly.xmin - ((pc_x - l_gate) / 2), -pc_size[1] - end_cap + mv))

    else:

        w_p1 = end_cap + w_gate + end_cap  # poly total width

        if inter_sd_l < (poly2_spacing + 2 * pc_ext):

            if gate_con_pos == "alternating":
                w_p1 += 0.2
                w_p2 = w_p1
                e_c = 0.2
            else:
                w_p2 = w_p1 + con_pl_enc + con_size + con_pl_enc + poly2_spacing + 0.1
                e_c = 0

            if gate_con_pos == "bottom":
                p_mv = -end_cap - (w_p2 - w_p1)
            else:
                p_mv = -end_cap

        else:

            w_p2 = w_p1
            p_mv = -end_cap
            e_c = 0

        rect_p1 = gf.components.rectangle(size=(l_gate, w_p1), layer=layer["poly2"])
        rect_p2 = gf.components.rectangle(size=(l_gate, w_p2), layer=layer["poly2"])
        poly1 = c_inst.add_array(
            rect_p1,
            rows=1,
            columns=ceil(nf / 2),
            spacing=[2 * (inter_sd_l + l_gate), 0],
        )
        poly1.xmin = sd_diff_intr.xmin + con_comp_enc
        poly1.ymin = sd_diff_intr.ymin - end_cap - e_c

        poly2 = c_inst.add_array(
            rect_p2,
            rows=1,
            columns=floor(nf / 2),
            spacing=[2 * (inter_sd_l + l_gate), 0],
        )
        poly2.xmin = poly1.xmin + l_gate + inter_sd_l
        poly2.ymin = p_mv

        # generating poly contacts setups

        if gate_con_pos == "bottom":
            mv_1 = 0
            mv_2 = -(w_p2 - w_p1)
        elif gate_con_pos == "top":
            mv_1 = pc_size[1] + w_p1
            mv_2 = pc_size[1] + w_p2
        else:
            mv_1 = -e_c
            mv_2 = pc_size[1] + w_p2

        nc1 = ceil(nf / 2)
        nc2 = floor(nf / 2)

        pc_spacing = 2 * (inter_sd_l + l_gate)

        # generating poly contacts

        pc1 = c_inst.add_array(
            component=c_pc, rows=1, columns=nc1, spacing=(pc_spacing, 0)
        )
        pc1.move((poly1.xmin - ((pc_x - l_gate) / 2), -pc_size[1] - end_cap + mv_1))

        pc2 = c_inst.add_array(
            component=c_pc, rows=1, columns=nc2, spacing=(pc_spacing, 0)
        )
        pc2.move(
            (
                poly1.xmin - ((pc_x - l_gate) / 2) + (inter_sd_l + l_gate),
                -pc_size[1] - end_cap + mv_2,
            )
        )

        if interdig == 1:
            c.add_ref(
                interdigit(
                    sd_diff=sd_diff,
                    pc1=pc1,
                    pc2=pc2,
                    poly_con=poly_con,
                    sd_diff_intr=sd_diff_intr,
                    l_gate=l_gate,
                    inter_sd_l=inter_sd_l,
                    sd_l=sd_l,
                    nf=nf,
                    patt=patt,
                    gate_con_pos=gate_con_pos,
                )
            )

    # generating bulk
    if bulk == "None":
        nplus = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_diff.size[0] + 2 * comp_np_enc, w_gate + 2 * gate_np_enc),
                layer=layer["nplus"],
            )
        )
        nplus.xmin = sd_diff.xmin - comp_np_enc
        nplus.ymin = sd_diff_intr.ymin - gate_np_enc

    elif bulk == "Bulk Tie":
        rect_bulk = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_l + con_sp, sd_diff.size[1]), layer=layer["comp"]
            )
        )
        rect_bulk.xmin = sd_diff.xmax
        rect_bulk.ymin = sd_diff.ymin
        nsdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(
                    sd_diff.xmax - sd_diff.xmin + comp_np_enc,
                    w_gate + 2 * gate_np_enc,
                ),
                layer=layer["nplus"],
            )
        )
        nsdm.xmin = sd_diff.xmin - comp_np_enc
        nsdm.ymin = sd_diff_intr.ymin - gate_np_enc
        psdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(
                    rect_bulk.xmax - rect_bulk.xmin + comp_pp_enc,
                    w_gate + 2 * comp_pp_enc,
                ),
                layer=layer["pplus"],
            )
        )
        psdm.connect("e1", destination=nsdm.ports["e3"])

        bulk_con = via_stack(
            x_range=(rect_bulk.xmin + 0.1, rect_bulk.xmax - 0.1),
            y_range=(rect_bulk.ymin, rect_bulk.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
        c_inst.add_ref(bulk_con)

    if bulk == "Guard Ring":

        nsdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_diff.size[0] + 2 * comp_np_enc, w_gate + 2 * gate_np_enc),
                layer=layer["nplus"],
            )
        )
        nsdm.xmin = sd_diff.xmin - comp_np_enc
        nsdm.ymin = sd_diff_intr.ymin - gate_np_enc
        c.add_ref(c_inst)

        b_gr = c.add_ref(
            bulk_gr_gen(
                c_inst=c_inst,
                comp_spacing=comp_spacing,
                poly2_comp_spacing=comp_spacing,
                volt=volt,
                grw=grw,
                l_d=l_d,
                implant_layer=layer["pplus"],
            )
        )

        psdm_polys = b_gr.get_polygons(by_spec=layer["pplus"])

        psdm_xmin = np.min(psdm_polys[0][:, 0])
        psdm_ymin = np.min(psdm_polys[0][:, 1])
        psdm_xmax = np.max(psdm_polys[0][:, 0])
        psdm_ymax = np.max(psdm_polys[0][:, 1])

        inst_size = (psdm_xmax - psdm_xmin, psdm_ymax - psdm_ymin)
        inst_xmin = psdm_xmin
        inst_ymin = psdm_ymin

    # if bulk != "Guard Ring":
    else:
        c.add_ref(c_inst)

        inst_size = (c_inst.size[0], c_inst.size[1])
        inst_xmin = c_inst.xmin
        inst_ymin = c_inst.ymin

        c.add_ref(
            hv_gen(c_inst=c_inst, volt=volt, dg_encx=dg_enc_cmp, dg_ency=dg_enc_poly)
        )

    c.add_ref(
        nfet_deep_nwell(
            deepnwell=deepnwell,
            pcmpgr=pcmpgr,
            inst_size=inst_size,
            inst_xmin=inst_xmin,
            inst_ymin=inst_ymin,
            grw=grw,
        )
    )

    # creating layout and cell in klayout
    c.write_gds("nfet_temp.gds")
    layout.read("nfet_temp.gds")
    cell_name = "sky_nfet_dev"

    return layout.cell(cell_name)
    # return c


@gf.cell
def pfet_deep_nwell(
    deepnwell: bool = 0,
    pcmpgr: bool = 0,
    enc_size: Float2 = (0.1, 0.1),
    enc_xmin: float = 0.1,
    enc_ymin: float = 0.1,
    nw_enc_pcmp: float = 0.1,
    grw: float = 0.36,
) -> gf.Component:
    """Returns pfet well related polygons

    Args :
        deepnwell : boolaen of having deepnwell
        pcmpgr : boolean of having deepnwell guardring
        enc_size : enclosed size
        enc_xmin : enclosed xmin
        enc_ymin : enclosed ymin
        nw_enc_pcmp : nwell enclosure of pcomp
        grw : guardring width
    """

    c = gf.Component()

    dnwell_enc_pcmp = 1.1

    if deepnwell == 1:
        dn_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    enc_size[0] + (2 * dnwell_enc_pcmp),
                    enc_size[1] + (2 * dnwell_enc_pcmp),
                ),
                layer=layer["dnwell"],
            )
        )

        dn_rect.xmin = enc_xmin - dnwell_enc_pcmp
        dn_rect.ymin = enc_ymin - dnwell_enc_pcmp

        if pcmpgr == 1:
            c.add_ref(pcmpgr_gen(dn_rect=dn_rect, grw=grw))

    else:

        # nwell generation
        nw = c.add_ref(
            gf.components.rectangle(
                size=(
                    enc_size[0] + (2 * nw_enc_pcmp),
                    enc_size[1] + (2 * nw_enc_pcmp),
                ),
                layer=layer["nwell"],
            )
        )
        nw.xmin = enc_xmin - nw_enc_pcmp
        nw.ymin = enc_ymin - nw_enc_pcmp

    return c


# @gf.cell
def draw_pfet(
    layout,
    l_gate: float = 0.28,
    w_gate: float = 0.22,
    sd_con_col: int = 1,
    inter_sd_l: float = 0.24,
    nf: int = 1,
    grw: float = 0.22,
    volt: str = "3.3V",
    bulk="None",
    con_bet_fin: int = 1,
    gate_con_pos="alternating",
    interdig: int = 0,
    patt="",
    deepnwell: int = 0,
    pcmpgr: int = 0,
) -> gf.Component:

    """
    Retern pfet

    Args:
        layout : layout object
        l : Float of gate length
        w : Float of gate width
        sd_l : Float of source and drain diffusion length
        inter_sd_l : Float of source and drain diffusion length between fingers
        nf : integer of number of fingers
        M : integer of number of multipliers
        grw : gaurd ring width when enabled
        type : string of the device type
        bulk : String of bulk connection type (None, Bulk Tie, Guard Ring)
        con_bet_fin : boolean of having contacts for diffusion between fingers
        gate_con_pos : string of choosing the gate contact position (bottom, top, alternating )

    """
    # used layers and dimensions

    end_cap: float = 0.22
    if volt == "3.3V":
        comp_spacing: float = 0.28
        nw_enc_pcmp = 0.43
    else:
        comp_spacing: float = 0.36
        nw_enc_pcmp = 0.6

    gate_pp_enc: float = 0.23
    comp_np_enc: float = 0.16
    comp_pp_enc: float = 0.16
    poly2_spacing: float = 0.24
    pc_ext: float = 0.04

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07
    con_pl_enc = 0.07
    dg_enc_cmp = 0.24
    dg_enc_poly = 0.4

    sd_l_con = (
        ((sd_con_col) * con_size) + ((sd_con_col - 1) * con_sp) + 2 * con_comp_enc
    )
    sd_l = sd_l_con

    # gds components to store a single instance and the generated device
    c = gf.Component("sky_pfet_dev")

    c_inst = gf.Component("dev_temp")

    # generating sd diffusion

    if interdig == 1 and nf > 1 and nf != len(patt) and patt != "":
        nf = len(patt)

    l_d = (
        nf * l_gate + (nf - 1) * inter_sd_l + 2 * (con_comp_enc)
    )  # diffution total length
    rect_d_intr = gf.components.rectangle(size=(l_d, w_gate), layer=layer["comp"])
    sd_diff_intr = c_inst.add_ref(rect_d_intr)

    # generatin sd contacts

    if w_gate <= con_size + 2 * con_comp_enc:
        cmpc_y = con_comp_enc + con_size + con_comp_enc

    else:
        cmpc_y = w_gate

    cmpc_size = (sd_l_con, cmpc_y)

    sd_diff = c_inst.add_array(
        component=gf.components.rectangle(size=cmpc_size, layer=layer["comp"]),
        rows=1,
        columns=2,
        spacing=(cmpc_size[0] + sd_diff_intr.size[0], 0),
    )

    sd_diff.xmin = sd_diff_intr.xmin - cmpc_size[0]
    sd_diff.ymin = sd_diff_intr.ymin - (sd_diff.size[1] - sd_diff_intr.size[1]) / 2

    sd_con = via_stack(
        x_range=(sd_diff.xmin, sd_diff_intr.xmin),
        y_range=(sd_diff.ymin, sd_diff.ymax),
        base_layer=layer["comp"],
        metal_level=1,
    )
    c_inst.add_array(
        component=sd_con,
        columns=2,
        rows=1,
        spacing=(sd_l + nf * l_gate + (nf - 1) * inter_sd_l + 2 * (con_comp_enc), 0,),
    )

    if con_bet_fin == 1 and nf > 1:
        inter_sd_con = via_stack(
            x_range=(
                sd_diff_intr.xmin + con_comp_enc + l_gate,
                sd_diff_intr.xmin + con_comp_enc + l_gate + inter_sd_l,
            ),
            y_range=(0, w_gate),
            base_layer=layer["comp"],
            metal_level=1,
        )
        c_inst.add_array(
            component=inter_sd_con,
            columns=nf - 1,
            rows=1,
            spacing=(l_gate + inter_sd_l, 0),
        )

    # generating poly

    if l_gate <= con_size + 2 * con_pl_enc:
        pc_x = con_pl_enc + con_size + con_pl_enc

    else:
        pc_x = l_gate

    pc_size = (pc_x, con_pl_enc + con_size + con_pl_enc)

    c_pc = gf.Component("poly con")

    rect_pc = c_pc.add_ref(gf.components.rectangle(size=pc_size, layer=layer["poly2"]))

    poly_con = via_stack(
        x_range=(rect_pc.xmin, rect_pc.xmax),
        y_range=(rect_pc.ymin, rect_pc.ymax),
        base_layer=layer["poly2"],
        metal_level=1,
        li_enc_dir="H",
    )
    c_pc.add_ref(poly_con)

    if nf == 1:
        poly = c_inst.add_ref(
            gf.components.rectangle(
                size=(l_gate, w_gate + 2 * end_cap), layer=layer["poly2"]
            )
        )
        poly.xmin = sd_diff_intr.xmin + con_comp_enc
        poly.ymin = sd_diff_intr.ymin - end_cap

        if gate_con_pos == "bottom":
            mv = 0
            nr = 1
        elif gate_con_pos == "top":
            mv = pc_size[1] + w_gate + 2 * end_cap
            nr = 1
        else:
            mv = 0
            nr = 2

        pc = c_inst.add_array(
            component=c_pc,
            rows=nr,
            columns=1,
            spacing=(0, pc_size[1] + w_gate + 2 * end_cap),
        )
        pc.move((poly.xmin - ((pc_x - l_gate) / 2), -pc_size[1] - end_cap + mv))

    else:

        w_p1 = end_cap + w_gate + end_cap  # poly total width

        if inter_sd_l < (poly2_spacing + 2 * pc_ext):

            if gate_con_pos == "alternating":
                w_p1 += 0.2
                w_p2 = w_p1
                e_c = 0.2
            else:
                w_p2 = w_p1 + con_pl_enc + con_size + con_pl_enc + poly2_spacing + 0.1
                e_c = 0

            if gate_con_pos == "bottom":
                p_mv = -end_cap - (w_p2 - w_p1)
            else:
                p_mv = -end_cap

        else:

            w_p2 = w_p1
            p_mv = -end_cap
            e_c = 0

        rect_p1 = gf.components.rectangle(size=(l_gate, w_p1), layer=layer["poly2"])
        rect_p2 = gf.components.rectangle(size=(l_gate, w_p2), layer=layer["poly2"])
        poly1 = c_inst.add_array(
            rect_p1,
            rows=1,
            columns=ceil(nf / 2),
            spacing=[2 * (inter_sd_l + l_gate), 0],
        )
        poly1.xmin = sd_diff_intr.xmin + con_comp_enc
        poly1.ymin = sd_diff_intr.ymin - end_cap - e_c

        poly2 = c_inst.add_array(
            rect_p2,
            rows=1,
            columns=floor(nf / 2),
            spacing=[2 * (inter_sd_l + l_gate), 0],
        )
        poly2.xmin = poly1.xmin + l_gate + inter_sd_l
        poly2.ymin = p_mv

        # generating poly contacts setups

        if gate_con_pos == "bottom":
            mv_1 = 0
            mv_2 = -(w_p2 - w_p1)
        elif gate_con_pos == "top":
            mv_1 = pc_size[1] + w_p1
            mv_2 = pc_size[1] + w_p2
        else:
            mv_1 = -e_c
            mv_2 = pc_size[1] + w_p2

        nc1 = ceil(nf / 2)
        nc2 = floor(nf / 2)

        pc_spacing = 2 * (inter_sd_l + l_gate)

        # generating poly contacts

        pc1 = c_inst.add_array(
            component=c_pc, rows=1, columns=nc1, spacing=(pc_spacing, 0)
        )
        pc1.move((poly1.xmin - ((pc_x - l_gate) / 2), -pc_size[1] - end_cap + mv_1))

        pc2 = c_inst.add_array(
            component=c_pc, rows=1, columns=nc2, spacing=(pc_spacing, 0)
        )
        pc2.move(
            (
                poly1.xmin - ((pc_x - l_gate) / 2) + (inter_sd_l + l_gate),
                -pc_size[1] - end_cap + mv_2,
            )
        )

        if interdig == 1:
            c.add_ref(
                interdigit(
                    sd_diff=sd_diff,
                    pc1=pc1,
                    pc2=pc2,
                    poly_con=poly_con,
                    sd_diff_intr=sd_diff_intr,
                    l_gate=l_gate,
                    inter_sd_l=inter_sd_l,
                    sd_l=sd_l,
                    nf=nf,
                    patt=patt,
                    gate_con_pos=gate_con_pos,
                )
            )

    # generating bulk
    if bulk == "None":
        pplus = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_diff.size[0] + 2 * comp_pp_enc, w_gate + 2 * gate_pp_enc),
                layer=layer["pplus"],
            )
        )
        pplus.xmin = sd_diff.xmin - comp_pp_enc
        pplus.ymin = sd_diff_intr.ymin - gate_pp_enc

        c.add_ref(c_inst)

        # deep nwell and nwell generation

        c.add_ref(
            pfet_deep_nwell(
                deepnwell=deepnwell,
                pcmpgr=pcmpgr,
                enc_size=(sd_diff.size[0], sd_diff.size[1]),
                enc_xmin=sd_diff.xmin,
                enc_ymin=sd_diff.ymin,
                nw_enc_pcmp=nw_enc_pcmp,
                grw=grw,
            )
        )

        # dualgate generation

        c.add_ref(
            hv_gen(c_inst=c_inst, volt=volt, dg_encx=dg_enc_cmp, dg_ency=dg_enc_poly)
        )

    elif bulk == "Bulk Tie":
        rect_bulk = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_l + con_sp, sd_diff.size[1]), layer=layer["comp"]
            )
        )
        rect_bulk.xmin = sd_diff.xmax
        rect_bulk.ymin = sd_diff.ymin
        psdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(
                    sd_diff.xmax - sd_diff.xmin + comp_pp_enc,
                    w_gate + 2 * gate_pp_enc,
                ),
                layer=layer["pplus"],
            )
        )
        psdm.xmin = sd_diff.xmin - comp_pp_enc
        psdm.ymin = sd_diff_intr.ymin - gate_pp_enc
        nsdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(
                    rect_bulk.xmax - rect_bulk.xmin + comp_np_enc,
                    w_gate + 2 * comp_np_enc,
                ),
                layer=layer["nplus"],
            )
        )
        nsdm.connect("e1", destination=psdm.ports["e3"])

        bulk_con = via_stack(
            x_range=(rect_bulk.xmin + 0.1, rect_bulk.xmax - 0.1),
            y_range=(rect_bulk.ymin, rect_bulk.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
        c_inst.add_ref(bulk_con)

        c.add_ref(c_inst)

        # deep nwell generation

        c.add_ref(
            pfet_deep_nwell(
                deepnwell=deepnwell,
                pcmpgr=pcmpgr,
                enc_size=(sd_diff.size[0] + rect_bulk.size[0], sd_diff.size[1]),
                enc_xmin=sd_diff.xmin,
                enc_ymin=sd_diff.ymin,
                nw_enc_pcmp=nw_enc_pcmp,
                grw=grw,
            )
        )

        # dualgate generation
        c.add_ref(
            hv_gen(c_inst=c_inst, volt=volt, dg_encx=dg_enc_cmp, dg_ency=dg_enc_poly)
        )

    elif bulk == "Guard Ring":

        psdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_diff.size[0] + 2 * comp_np_enc, w_gate + 2 * gate_pp_enc),
                layer=layer["pplus"],
            )
        )
        psdm.xmin = sd_diff.xmin - comp_pp_enc
        psdm.ymin = sd_diff_intr.ymin - gate_pp_enc
        c.add_ref(c_inst)

        b_gr = c.add_ref(
            bulk_gr_gen(
                c_inst=c_inst,
                comp_spacing=comp_spacing,
                poly2_comp_spacing=comp_spacing,
                volt=volt,
                grw=grw,
                l_d=l_d,
                implant_layer=layer["nplus"],
            )
        )  # bulk guardring

        B_polys = b_gr.get_polygons(by_spec=layer["comp"])

        B_xmin = np.min(B_polys[0][:, 0])
        B_ymin = np.min(B_polys[0][:, 1])
        B_xmax = np.max(B_polys[0][:, 0])
        B_ymax = np.max(B_polys[0][:, 1])

        #   deep nwell generation

        c.add_ref(
            pfet_deep_nwell(
                deepnwell=deepnwell,
                pcmpgr=pcmpgr,
                enc_size=(B_xmax - B_xmin, B_ymax - B_ymin),
                enc_xmin=B_xmin,
                enc_ymin=B_ymin,
                nw_enc_pcmp=nw_enc_pcmp,
                grw=grw,
            )
        )

    # creating layout and cell in klayout
    c.write_gds("pfet_temp.gds")
    layout.read("pfet_temp.gds")
    cell_name = "sky_pfet_dev"

    return layout.cell(cell_name)


def draw_nfet_06v0_nvt(
    layout,
    l_gate: float = 1.8,
    w_gate: float = 0.8,
    sd_con_col: int = 1,
    inter_sd_l: float = 0.24,
    nf: int = 1,
    grw: float = 0.22,
    bulk="None",
    con_bet_fin: int = 1,
    gate_con_pos="alternating",
    interdig: int = 0,
    patt="",
) -> gf.Component:

    """
    Usage:-
     used to draw Native NFET 6V transistor by specifying parameters
    Arguments:-
     layout : Object of layout
     l      : Float of gate length
     w      : Float of gate width
     ld     : Float of diffusion length
     nf     : Integer of number of fingers
     grw    : Float of guard ring width [If enabled]
     bulk   : String of bulk connection type [None, Bulk Tie, Guard Ring]
    """

    # used layers and dimensions

    end_cap: float = 0.22

    comp_spacing: float = 0.36
    poly2_comp_spacing: float = 0.3

    gate_np_enc: float = 0.23
    comp_np_enc: float = 0.16
    comp_pp_enc: float = 0.16
    poly2_spacing: float = 0.24
    pc_ext: float = 0.04

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07
    con_pl_enc = 0.07
    dg_enc_cmp = 0.24
    dg_enc_poly = 0.4

    sd_l_con = (
        ((sd_con_col) * con_size) + ((sd_con_col - 1) * con_sp) + 2 * con_comp_enc
    )
    sd_l = sd_l_con

    # gds components to store a single instance and the generated device
    c = gf.Component("sky_nfet_nvt_dev")

    c_inst = gf.Component("dev_temp")

    # generating sd diffusion

    if interdig == 1 and nf > 1 and nf != len(patt) and patt != "":
        nf = len(patt)

    l_d = (
        nf * l_gate + (nf - 1) * inter_sd_l + 2 * (con_comp_enc)
    )  # diffution total length
    rect_d_intr = gf.components.rectangle(size=(l_d, w_gate), layer=layer["comp"])
    sd_diff_intr = c_inst.add_ref(rect_d_intr)

    # generatin sd contacts

    if w_gate <= con_size + 2 * con_comp_enc:
        cmpc_y = con_comp_enc + con_size + con_comp_enc

    else:
        cmpc_y = w_gate

    cmpc_size = (sd_l_con, cmpc_y)

    sd_diff = c_inst.add_array(
        component=gf.components.rectangle(size=cmpc_size, layer=layer["comp"]),
        rows=1,
        columns=2,
        spacing=(cmpc_size[0] + sd_diff_intr.size[0], 0),
    )

    sd_diff.xmin = sd_diff_intr.xmin - cmpc_size[0]
    sd_diff.ymin = sd_diff_intr.ymin - (sd_diff.size[1] - sd_diff_intr.size[1]) / 2

    sd_con = via_stack(
        x_range=(sd_diff.xmin, sd_diff_intr.xmin),
        y_range=(sd_diff.ymin, sd_diff.ymax),
        base_layer=layer["comp"],
        metal_level=1,
    )
    c_inst.add_array(
        component=sd_con,
        columns=2,
        rows=1,
        spacing=(sd_l + nf * l_gate + (nf - 1) * inter_sd_l + 2 * (con_comp_enc), 0,),
    )

    if con_bet_fin == 1 and nf > 1:
        inter_sd_con = via_stack(
            x_range=(
                sd_diff_intr.xmin + con_comp_enc + l_gate,
                sd_diff_intr.xmin + con_comp_enc + l_gate + inter_sd_l,
            ),
            y_range=(0, w_gate),
            base_layer=layer["comp"],
            metal_level=1,
        )
        c_inst.add_array(
            component=inter_sd_con,
            columns=nf - 1,
            rows=1,
            spacing=(l_gate + inter_sd_l, 0),
        )

    # generating poly

    if l_gate <= con_size + 2 * con_pl_enc:
        pc_x = con_pl_enc + con_size + con_pl_enc

    else:
        pc_x = l_gate

    pc_size = (pc_x, con_pl_enc + con_size + con_pl_enc)

    c_pc = gf.Component("poly con")

    rect_pc = c_pc.add_ref(gf.components.rectangle(size=pc_size, layer=layer["poly2"]))

    poly_con = via_stack(
        x_range=(rect_pc.xmin, rect_pc.xmax),
        y_range=(rect_pc.ymin, rect_pc.ymax),
        base_layer=layer["poly2"],
        metal_level=1,
        li_enc_dir="H",
    )
    c_pc.add_ref(poly_con)

    if nf == 1:
        poly = c_inst.add_ref(
            gf.components.rectangle(
                size=(l_gate, w_gate + 2 * end_cap), layer=layer["poly2"]
            )
        )
        poly.xmin = sd_diff_intr.xmin + con_comp_enc
        poly.ymin = sd_diff_intr.ymin - end_cap

        if gate_con_pos == "bottom":
            mv = 0
            nr = 1
        elif gate_con_pos == "top":
            mv = pc_size[1] + w_gate + 2 * end_cap
            nr = 1
        else:
            mv = 0
            nr = 2

        pc = c_inst.add_array(
            component=c_pc,
            rows=nr,
            columns=1,
            spacing=(0, pc_size[1] + w_gate + 2 * end_cap),
        )
        pc.move((poly.xmin - ((pc_x - l_gate) / 2), -pc_size[1] - end_cap + mv))

    else:

        w_p1 = end_cap + w_gate + end_cap  # poly total width

        if inter_sd_l < (poly2_spacing + 2 * pc_ext):

            if gate_con_pos == "alternating":
                w_p1 += 0.2
                w_p2 = w_p1
                e_c = 0.2
            else:
                w_p2 = w_p1 + con_pl_enc + con_size + con_pl_enc + poly2_spacing + 0.1
                e_c = 0

            if gate_con_pos == "bottom":
                p_mv = -end_cap - (w_p2 - w_p1)
            else:
                p_mv = -end_cap

        else:

            w_p2 = w_p1
            p_mv = -end_cap
            e_c = 0

        rect_p1 = gf.components.rectangle(size=(l_gate, w_p1), layer=layer["poly2"])
        rect_p2 = gf.components.rectangle(size=(l_gate, w_p2), layer=layer["poly2"])
        poly1 = c_inst.add_array(
            rect_p1,
            rows=1,
            columns=ceil(nf / 2),
            spacing=[2 * (inter_sd_l + l_gate), 0],
        )
        poly1.xmin = sd_diff_intr.xmin + con_comp_enc
        poly1.ymin = sd_diff_intr.ymin - end_cap - e_c

        poly2 = c_inst.add_array(
            rect_p2,
            rows=1,
            columns=floor(nf / 2),
            spacing=[2 * (inter_sd_l + l_gate), 0],
        )
        poly2.xmin = poly1.xmin + l_gate + inter_sd_l
        poly2.ymin = p_mv

        # generating poly contacts setups

        if gate_con_pos == "bottom":
            mv_1 = 0
            mv_2 = -(w_p2 - w_p1)
        elif gate_con_pos == "top":
            mv_1 = pc_size[1] + w_p1
            mv_2 = pc_size[1] + w_p2
        else:
            mv_1 = -e_c
            mv_2 = pc_size[1] + w_p2

        nc1 = ceil(nf / 2)
        nc2 = floor(nf / 2)

        pc_spacing = 2 * (inter_sd_l + l_gate)

        # generating poly contacts

        pc1 = c_inst.add_array(
            component=c_pc, rows=1, columns=nc1, spacing=(pc_spacing, 0)
        )
        pc1.move((poly1.xmin - ((pc_x - l_gate) / 2), -pc_size[1] - end_cap + mv_1))

        pc2 = c_inst.add_array(
            component=c_pc, rows=1, columns=nc2, spacing=(pc_spacing, 0)
        )
        pc2.move(
            (
                poly1.xmin - ((pc_x - l_gate) / 2) + (inter_sd_l + l_gate),
                -pc_size[1] - end_cap + mv_2,
            )
        )

        if interdig == 1:
            c.add_ref(
                interdigit(
                    sd_diff=sd_diff,
                    pc1=pc1,
                    pc2=pc2,
                    poly_con=poly_con,
                    sd_diff_intr=sd_diff_intr,
                    l_gate=l_gate,
                    inter_sd_l=inter_sd_l,
                    sd_l=sd_l,
                    nf=nf,
                    patt=patt,
                    gate_con_pos=gate_con_pos,
                )
            )

    # generating bulk
    if bulk == "None":
        nplus = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_diff.size[0] + 2 * comp_np_enc, w_gate + 2 * gate_np_enc),
                layer=layer["nplus"],
            )
        )
        nplus.xmin = sd_diff.xmin - comp_np_enc
        nplus.ymin = sd_diff_intr.ymin - gate_np_enc

    elif bulk == "Bulk Tie":
        rect_bulk = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_l + con_sp, sd_diff.size[1]), layer=layer["comp"]
            )
        )
        rect_bulk.xmin = sd_diff.xmax
        rect_bulk.ymin = sd_diff.ymin
        nsdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(
                    sd_diff.xmax - sd_diff.xmin + comp_np_enc,
                    w_gate + 2 * gate_np_enc,
                ),
                layer=layer["nplus"],
            )
        )
        nsdm.xmin = sd_diff.xmin - comp_np_enc
        nsdm.ymin = sd_diff_intr.ymin - gate_np_enc
        psdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(
                    rect_bulk.xmax - rect_bulk.xmin + comp_pp_enc,
                    w_gate + 2 * comp_pp_enc,
                ),
                layer=layer["pplus"],
            )
        )
        psdm.connect("e1", destination=nsdm.ports["e3"])

        bulk_con = via_stack(
            x_range=(rect_bulk.xmin + 0.1, rect_bulk.xmax - 0.1),
            y_range=(rect_bulk.ymin, rect_bulk.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
        c_inst.add_ref(bulk_con)

    elif bulk == "Guard Ring":

        nsdm = c_inst.add_ref(
            gf.components.rectangle(
                size=(sd_diff.size[0] + 2 * comp_np_enc, w_gate + 2 * gate_np_enc),
                layer=layer["nplus"],
            )
        )
        nsdm.xmin = sd_diff.xmin - comp_np_enc
        nsdm.ymin = sd_diff_intr.ymin - gate_np_enc
        c.add_ref(c_inst)

        c_temp = gf.Component("temp_store")
        rect_bulk_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (c_inst.xmax - c_inst.xmin) + 2 * comp_spacing,
                    (c_inst.ymax - c_inst.ymin) + 2 * poly2_comp_spacing,
                ),
                layer=layer["comp"],
            )
        )
        rect_bulk_in.move(
            (c_inst.xmin - comp_spacing, c_inst.ymin - poly2_comp_spacing)
        )
        rect_bulk_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_bulk_in.xmax - rect_bulk_in.xmin) + 2 * grw,
                    (rect_bulk_in.ymax - rect_bulk_in.ymin) + 2 * grw,
                ),
                layer=layer["comp"],
            )
        )
        rect_bulk_out.move((rect_bulk_in.xmin - grw, rect_bulk_in.ymin - grw))
        B = c.add_ref(
            gf.geometry.boolean(
                A=rect_bulk_out, B=rect_bulk_in, operation="A-B", layer=layer["comp"],
            )
        )

        psdm_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_bulk_in.xmax - rect_bulk_in.xmin) - 2 * comp_pp_enc,
                    (rect_bulk_in.ymax - rect_bulk_in.ymin) - 2 * comp_pp_enc,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.move((rect_bulk_in.xmin + comp_pp_enc, rect_bulk_in.ymin + comp_pp_enc))
        psdm_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_bulk_out.xmax - rect_bulk_out.xmin) + 2 * comp_pp_enc,
                    (rect_bulk_out.ymax - rect_bulk_out.ymin) + 2 * comp_pp_enc,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.move(
            (rect_bulk_out.xmin - comp_pp_enc, rect_bulk_out.ymin - comp_pp_enc,)
        )
        psdm = c.add_ref(
            gf.geometry.boolean(
                A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"]
            )
        )

        # generating contacts

        c.add_ref(
            via_generator(
                x_range=(rect_bulk_in.xmin + con_size, rect_bulk_in.xmax - con_size,),
                y_range=(rect_bulk_out.ymin, rect_bulk_in.ymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(rect_bulk_in.xmin + con_size, rect_bulk_in.xmax - con_size,),
                y_range=(rect_bulk_in.ymax, rect_bulk_out.ymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        c.add_ref(
            via_generator(
                x_range=(rect_bulk_out.xmin, rect_bulk_in.xmin),
                y_range=(rect_bulk_in.ymin + con_size, rect_bulk_in.ymax - con_size,),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        c.add_ref(
            via_generator(
                x_range=(rect_bulk_in.xmax, rect_bulk_out.xmax),
                y_range=(rect_bulk_in.ymin + con_size, rect_bulk_in.ymax - con_size,),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        comp_m1_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (l_d) + 2 * comp_spacing,
                    (c_inst.ymax - c_inst.ymin) + 2 * poly2_comp_spacing,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_in.move((-comp_spacing, c_inst.ymin - poly2_comp_spacing))
        comp_m1_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_bulk_in.xmax - rect_bulk_in.xmin) + 2 * grw,
                    (rect_bulk_in.ymax - rect_bulk_in.ymin) + 2 * grw,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.move((rect_bulk_in.xmin - grw, rect_bulk_in.ymin - grw))
        c.add_ref(
            gf.geometry.boolean(
                A=rect_bulk_out, B=rect_bulk_in, operation="A-B", layer=layer["metal1"],
            )
        )  # guardring metal1

        dg = c.add_ref(
            gf.components.rectangle(
                size=(B.size[0] + (2 * dg_enc_cmp), B.size[1] + (2 * dg_enc_cmp),),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = B.xmin - dg_enc_cmp
        dg.ymin = B.ymin - dg_enc_cmp

    if bulk != "Guard Ring":
        c.add_ref(c_inst)

        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    c_inst.size[0] + (2 * dg_enc_cmp),
                    c_inst.size[1] + (2 * dg_enc_poly),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = c_inst.xmin - dg_enc_cmp
        dg.ymin = c_inst.ymin - dg_enc_poly

    # generating native layer
    nat = c.add_ref(
        gf.components.rectangle(size=(dg.size[0], dg.size[1]), layer=layer["nat"])
    )

    nat.xmin = dg.xmin
    nat.ymin = dg.ymin

    # creating layout and cell in klayout

    c.write_gds("nfet_nvt_temp.gds")
    layout.read("nfet_nvt_temp.gds")
    cell_name = "sky_nfet_nvt_dev"

    return layout.cell(cell_name)


#     # return c

if __name__ == "__main__":
    c = draw_nfet(nf=3, con_bet_fin=0, bulk="Guard Ring")
    c.show()