{
    "name": "School management ",
    "version": "1.0",
    "category": "Management/Management",
    "summary": "School Management",
    "author": "BizzAppDev",
    "description": """
This module contains all the common features of School Management.
    """,
    "depends": ["mail","sale"],
    "data": [
        "Data/seq.xml",
        "security/ir.model.access.csv",
        "views/inherit_desc.xml",
        "views/school_student_view.xml",
        "views/school_menu.xml",
        "wizard/demo_wizard_view.xml",
    ],
    "license": "LGPL-3",
}
