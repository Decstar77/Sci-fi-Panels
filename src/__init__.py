# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
bl_info = {
    "name" : "Sci-fi_Panel_Generator",
    "author" : "Declan Richard Porter",
    "description" : "Generates quick sci-fi panels",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "View3D > Add > Mesh",
    "wiki_url": "",
    "tracker_url": "",
    "warning" : "",
    "support": "COMMUNITY",
    "category" : "Add Mesh"
}

from .Sci_fi_panels import * 


class Addon_Properties(bpy.types.PropertyGroup):

    a_insetAmount = bpy.props.FloatProperty(name="Inset amount", default=0.03, min =0.01, max = 0.3, description="Distance to be inset by, generally smaller = better")
    a_insetDiscard = bpy.props.FloatProperty(name="Inset discard threshhold", default=0, min =0, max = 0.3, description= "Discards faces for inseting and extruding if the area falls below value") 
    a_extrudeAmount = bpy.props.FloatProperty(name="Extrude length", default= 0.1, min =0, max = 0.3, description= "Extruded length of inseted faces")
    
    a_iterations =  bpy.props.IntProperty(name="Iterations", default=3, min = 0, max = 10, description="Number of attempts to cut the mesh")
    a_areaKill = bpy.props.FloatProperty(name="AreaKill threshhold", default= 0.1, min = 0, max = 0.3, description= "Attempts to merge faces together if the area falls below value")
    a_longedgeBias = bpy.props.FloatProperty(name="Long edge bias", default= 0.75, min = 0, max = 1, description= "Favours subdividing longer edges")

    s_insetAmount = bpy.props.FloatProperty(name="Inset amount", default=0.03, min =0.01, max = 0.3, description="Distance to be inset by, generally smaller = better")
    s_insetDiscard = bpy.props.FloatProperty(name="Inset discard threshhold", default=0, min =0, max = 0.3, description= "Discards faces for inseting and extruding if the area falls below value")
    s_extrudeAmount = bpy.props.FloatProperty(name="Extrude length", default= 0.1, min =0, max = 0.3, description= "Extruded length of inseted faces")

    s_bevelAmount_min = bpy.props.FloatProperty(name="Bevel min", default= 0.1, min = 0, max = 0.3, description="Beveled length of non-boundary vertices")
    s_bevelAmount_max = bpy.props.FloatProperty(name="Bevel max", default= 0.15, min = 0, max = 0.3, description="Beveled length of non-boundary vertices")
    s_maxX = bpy.props.IntProperty(name="Max X cuts", default=3, min = 1, max = 10, description="The max number of cuts possible. Ie random number between 1 and max")
    s_maxY = bpy.props.IntProperty(name="Max Y cuts", default=3, min = 1, max = 10, description="The max number of cuts possible. Ie random number between 1 and max")


class OBJECT_OT_Square(bpy.types.Operator):
    bl_idname = "object.square"
    bl_label = "Generate square"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #SqaureAlogrithm(1, 10, 1, 10)
        scene = context.scene.addon_Properties
        SqaureAlogrithm(1,scene.s_maxX, 1, scene.s_maxY, scene.s_insetAmount, scene.s_insetDiscard, scene.s_bevelAmount_min, scene.s_bevelAmount_max, scene.s_extrudeAmount)
        return {'FINISHED'}

class OBJECT_OT_Abstract(bpy.types.Operator):
    bl_idname = "object.abstract"
    bl_label = "Generate abstract"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #SqaureAlogrithm(1, 10, 1, 10)
        scene = context.scene.addon_Properties
        AbstractAlgorithm(scene.a_iterations, scene.a_areaKill, scene.a_insetAmount, scene.a_insetDiscard, scene.a_extrudeAmount, scene.a_longedgeBias)
        return {'FINISHED'}

class TEST_PT_PANEL(bpy.types.Panel):
    bl_idname = "object_PT_Panel"
    bl_label = "Panels"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Panel Generator"
    

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        # You can set the property values that should be used when the user
        # presses the button in the UI.
    
        layout = self.layout
        scn = context.scene.addon_Properties

        s_box = layout.box()
        s_box.label(text="Square Algorithm")
        s_op = s_box.operator("object.square")
        s_box.prop(scn, 's_insetAmount')
        s_box.prop(scn, 's_insetDiscard')
        s_box.prop(scn, 's_extrudeAmount')
        s_box.prop(scn, 's_maxX')
        s_box.prop(scn, 's_maxY')
        s_box.prop(scn, 's_bevelAmount_min')
        s_box.prop(scn, 's_bevelAmount_max')

        a_box = layout.box()
        a_box.label(text="Abstract Algorithm")
        a_op = a_box.operator("object.abstract")
        a_box.prop(scn, "a_insetAmount")
        a_box.prop(scn, "a_insetDiscard")
        a_box.prop(scn, "a_extrudeAmount")
        a_box.prop(scn, "a_iterations")
        a_box.prop(scn, "a_areaKill")
        a_box.prop(scn, "a_longedgeBias")

        #props = self.layout.operator('object.property_example')
        #props.my_bool = True
        #props.my_string = "Shouldn't that be 47?"

        # You can set 


def register():
    bpy.utils.register_class(OBJECT_OT_Square)
    bpy.utils.register_class(OBJECT_OT_Abstract)
    bpy.utils.register_class(TEST_PT_PANEL)    
    bpy.utils.register_class(Addon_Properties)
    
    bpy.types.Scene.addon_Properties = bpy.props.PointerProperty(type=Addon_Properties)
    #auto_load.register()
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Square)
    bpy.utils.unregister_class(OBJECT_OT_Abstract)
    bpy.utils.unregister_class(TEST_PT_PANEL)
    bpy.utils.unregister_class(Addon_Properties)
    del bpy.types.Scene.addon_Properties
    #auto_load.unregister()
